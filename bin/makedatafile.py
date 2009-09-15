#!/usr/bin/env python
#
# Insert Grinder Log Files to MySQL
# Author: Soo Hwan Park (suwanny@gmail.com)
# Date: 08/26/2009
#

import sys, os, glob
import MySQLdb
import yaml
from dbconfig import DBConfig

DATA_ROOT="/home/spark2007/AppBenchmark/logs/"
dbconf = yaml.load(file('dbconfig.yaml', 'r'))

DEBUG = False

def main(argv):
  if len(argv) < 4 :
    print "usage: makedatafile.py test_id agent_id sample_index"
    print "example: ./makedatafile.py 20090801_guestbook_hbase bulls 0"
    sys.exit(0) 
  pass
  
  test_id = argv[1]
  test_info = test_id.split('_')
  if len(test_info) < 3:
    print "you have wrong test_id format, it should be 'date_app_db'"
    sys.exit(0)
  test_date, test_app, test_db = test_info
  print test_date, test_app, test_db
  agent_id = argv[2]
  sample_index = argv[3]

  filename = DATA_ROOT + "data_appscale-" + sample_index + ".log"
  
  db = MySQLdb.connect(host=dbconf.HOST, user=dbconf.USER, passwd=dbconf.PASS, db=dbconf.DATABASE)
  cursor = db.cursor()

  select = "SELECT * FROM %s WHERE agent='%s' and sample=%s ORDER BY start;" % (test_id, agent_id, sample_index)
  cursor.execute(select)

  datafile = open(filename, "w")
  result = cursor.fetchall()
  for record in result:
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

