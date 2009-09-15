#!/usr/bin/env python
#
# Insert Grinder Log Files to MySQL
# Author: Soo Hwan Park (suwanny@gmail.com)
# Date: 08/26/2009
#
# usage: insert_datalog.py test_id agent_id sample_index
# ./insert_datalog.py 20090801_guestbook_hbase bulls 0

import sys, os, glob
import MySQLdb
import yaml

sys.path.append("home/spark2007/AppBenchmark/bin")
from dbconfig import DBConfig

config_file="/home/spark2007/AppBenchmark/bin/dbconfig.yaml"
DATA_ROOT="/home/spark2007/AppBenchmark/logs/"
dbconf = yaml.load(file(config_file, 'r'))

import logging
import logging.handlers
LOG_DIR = "/home/spark2007/AppBenchmark"
LOG_FILENAME = LOG_DIR + "/insert.log"
if not os.path.exists(LOG_DIR): os.mkdir(LOG_DIR,0777)
logger = logging.getLogger("AppBench")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(module)s:%(lineno)-4d %(message)s")
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10000000, backupCount=10)
handler.setFormatter(formatter)
logger.addHandler(handler)

DEBUG = False

def createTable(cursor, test_id):
  cursor.execute("SHOW TABLES")
  result = cursor.fetchall()
  tables = []
  for table in result:
    tables.append(table[0])
    logger.info(table[0])

  if test_id in tables: return 
  create = "CREATE TABLE " + test_id + dbconf.SCHEMA 
  logger.debug(create )
  try: 
    cursor.execute(create)
  except Exception, e:
    logger.debug("create table exception")

def insertData(cursor, table, agent, sample, line):
  columns = "agent, sample, thread, run, test, start, latency, errors, "
  columns += "res_code, res_len, res_err, resolve, establish, firstbyte"
  insert = "INSERT INTO %s (%s) VALUES ('%s', %s, %s)" % (table, columns, agent, sample, line)
  #logger.info(insert)
  cursor.execute(insert)
  logger.debug("insert data:"+line)

def main(argv):
  if len(argv) < 4 :
    print "usage: insert_datalog.py test_id agent_id sample_index"
    print "example: ./insert_datalog.py 20090801_guestbook_hbase bulls 0"
    sys.exit(0)

  test_id = argv[1]
  test_info = test_id.split('_')
  if len(test_info) < 3: 
    logger.info("you have wrong test_id format, it should be 'date_app_db'")
    sys.exit(0)
  test_date, test_app, test_db = test_info
  print test_date, test_app, test_db
  agent_id = argv[2]
  sample_index = argv[3]

  logger.info("test id:" + test_id )
  logger.info("agent id:" +  agent_id )
  logger.info("sample index:"+ sample_index)

  db = MySQLdb.connect(host=dbconf.HOST, user=dbconf.USER, passwd=dbconf.PASS, db=dbconf.DATABASE) 
  cursor = db.cursor()
  createTable(cursor, test_id) 

  path = DATA_ROOT + test_app + "/"
  logger.info(path)
  for infile in glob.glob( os.path.join(path, 'data*.log*') ): 
    logger.info("filename:" +  infile)
    file = open(infile)
    for i, line in enumerate(file): 
      if line.find("Thread") == 0: continue
      line = line.rstrip()
      #logger.info infile[infile.rindex('/')+1:], i, line 
      data = line.split(',')
      if len(data) != 12: continue;
      insertData(cursor, test_id, agent_id, sample_index, line)

  cmd1 = "mkdir -p %sbackup" % (path)
  cmd2 = "mv %s*.log* %sbackup" % (path, path)
  logger.info(cmd1)
  logger.info(cmd2)
  os.system(cmd1)
  os.system(cmd2)

  # make data file .. 
  #filename = DATA_ROOT + "data_appscale-" + sample_index + ".log"
  filename = "/tmp/" + "data_appscale-" + sample_index + ".log"
  select = "SELECT * FROM %s WHERE agent='%s' and sample=%s ORDER BY start;" % (test_id, agent_id, sample_index)
  cursor.execute(select)
  datafile = open(filename, "w")
  result = cursor.fetchall()
  for record in result:
    logger.debug("select %d %d %d" % (record[3], record[4], record[5]))
    raw_record = record[3:]
    for i, data in enumerate(raw_record):
      if i+1 < len(raw_record): datafile.write(str(data) + ",")
      else: datafile.write(str(data) + "\n")
  datafile.close()

if __name__ == "__main__":
  try:
    main(sys.argv)
  except:
    raise
