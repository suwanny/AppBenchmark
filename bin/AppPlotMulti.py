#!/usr/bin/env python
# 
# A Chart Plot Utility for AppScale 
# Author: Soo Hwan Park (suwanny@gmail.com)
# Date: 08/03/2009 
#
import sys, os
from numpy import *
from xlwt import Workbook

DEBUG = False
TIME_INTERVAL = 5

class BMData:
  attributes_ = [
    "thread",       # thread id  
    "run",          # run id 
    "test",         # test id  
    "start",        # start_time
    "elapsed",      # elapsed time
    "errors",       # errors 
    "code",         # HTTP response code
    "length",       # HTTP response length 
    "error",        # HTTP response error
    "resolve",      # time to resolve host
    "establish",    # time to establish connection 
    "firstbyte",    # time to first byte 
  ] 

  def __init__(self, tokens):
    self.thread     = tokens[0]
    self.run        = tokens[1]
    self.test       = tokens[2]
    self.start      = tokens[3]
    self.elapsed    = tokens[4]
    self.errors     = tokens[5]
    self.code       = tokens[6]
    self.length     = tokens[7]
    self.error      = tokens[8]
    self.resolve    = tokens[9]
    self.establish  = tokens[10]
    self.firstbyte  = tokens[11]

  def __cmp__(self, other):
    return cmp(self.t_start, other.t_start)

class TimeInterval:
  def __init__(self, id):
    self.id = id
    self.transactions = 0
    self.response = []

  def add(self, rtime ):
    self.transactions += 1
    self.response.append(rtime)

  def getAvg(self):
    if self.transactions == 0: return 0
    sum = 0
    for data in self.response:
      sum += int(data)
    return sum / self.transactions

class TestResult:
  def __init__(self, name):
    self.name = name
    self.perSecondResult = {}
    self.test_ids = []
    self.max_second = 0;

  def addDataDict(self, testDict):
    results = testDict
    self.test_ids = testDict.keys()
    self.test_ids.sort()
    completed_count = len(results[self.test_ids[0]])
    for key in results.keys(): 
      completed_count = min(completed_count, len(results[key]))

    starttime = results[self.test_ids[0]][0].start
    persecond = self.perSecondResult

    for i in range(completed_count):
      for id in self.test_ids: 
        record = results[id][i]; 
        elapsed = (int(record.start) - int(starttime))/1000
        #elapsed = (int(record.start) + int(record.elapsed) - int(starttime))/1000
        elapsed = ( elapsed/TIME_INTERVAL + 1) * TIME_INTERVAL
        self.max_second = max(self.max_second, elapsed)
        key = id + "-" + str(elapsed)
        if persecond.has_key(key):
          persecond[key].add(record.elapsed)
        else: 
          persecond[key] = TimeInterval(id)
          persecond[key].add(record.elapsed)
  
  def getTestIDs(self):
    return self.test_ids
  
  def getResult(self, id, elapsed):
    if self.perSecondResult.has_key(id + "-" + str(elapsed)):
      return self.perSecondResult[id + "-" + str(elapsed)]
    else:
      return TimeInterval(id)

  def getResults(self):
    return self.perSecondResult

  def getResultRows(self):
    return range(1, self.max_second /TIME_INTERVAL + 1)
  
  def print_responseTime_persecond(self):
    book = Workbook()
    sheet1 = book.add_sheet("response time")
    sheet2 = book.add_sheet("transactions")
    title = "Test Name: %s" % (self.name)
    sheet1.write(0,0,title)
    sheet2.write(0,0,title)
    column = 1
    for id in self.test_ids:  
      sheet1.write(1, column, "TEST" + id)
      sheet2.write(1, column, "TEST" + id)
      column += 1
    
    results = self.perSecondResult
    rows = range(1, self.max_second /TIME_INTERVAL + 1)

    for row in rows:
      sheet1.write(row + 1, 0, row*TIME_INTERVAL )
      sheet2.write(row + 1, 0, row*TIME_INTERVAL )
      column = 1
      for id in self.test_ids:
        key = id + "-" + str(row*TIME_INTERVAL)
        if results.has_key(key):
          result = results[key]
          sheet1.write(row + 1, column, result.getAvg()) 
          sheet2.write(row + 1, column, result.transactions) 
        column += 1
    
    book.save(self.name + "_bytime.xls")

def makeDataDict(filename):
  print "data file:", filename
  data_file = open(filename)
  newDict = {}

  for line in data_file:
    if DEBUG: print "line:", line,
    line.rstrip()
    tokens = line.split(",")
    if tokens[0] == "Thread": continue
    if DEBUG: print tokens

    data = BMData(tokens)
    status_code = int(data.code)
    if (status_code / 100) > 3: # only 4XX, 5XX, and 6XX are considered failure
      print "status code is not success:", status_code
      print "error line:", line
      continue
 
    if newDict.has_key(data.test):
      newDict[data.test].append(data)
    else:
      newDict[data.test] = [data]

  data_file.close()
  return newDict
  
    
def main(argv): 
  if len(argv) < 6 : 
    print "usage: AppPlotMulti.py stat_name dir_name dir_count file_name file_count"
    print "example: ./AppPlotMulti.py hbase gb_hbase 3 data_appscale-image 5"
    sys.exit(0)

  statistics_name = argv[1]
  dir_name = argv[2]
  dir_count = int(argv[3])
  file_name = argv[4]
  file_count = int(argv[5])
  
  dirnames = []
  for index in range(1, dir_count+1):
    dirnames.append(dir_name + "_" + str(index))

  results = []
  for index in range(file_count):
    result = TestResult(statistics_name + "-" + str(index))
    for dir in dirnames:
      filename = dir + "/" + file_name + "-" + str(index) + ".log"
      result.addDataDict(makeDataDict(filename))
    result.print_responseTime_persecond()
    results.append(result)

  tests = results[0].getTestIDs()
  rows = results[0].getResultRows()
  print tests
  #for row in rows: print row

  file_response = open("response.dat", "w")
  file_transactions = open("transactions.dat", "w")

  # time, test1, test1-std, test2, test2-std, ....

  file_response.write("#time\t")
  file_transactions.write("#time\t")
  for test in tests:
    file_response.write(test + "\t" + test + "-std\t")
    file_transactions.write(test + "\t" + test + "-std\t")
  file_response.write("\n")
  file_transactions.write("\n")

  for row in rows:
    elapsed = row*TIME_INTERVAL
    file_response.write(str(elapsed) + "\t")
    file_transactions.write(str(elapsed) + "\t")
    for test in tests:
      responses = []
      transactions = []
      for result in results:
        sample = result.getResult(test, elapsed)
        responses.append(sample.getAvg())
        transactions.append(sample.transactions)
     
      #print responses 
      mean_response = mean(responses)
      std_response = std(responses)

      #print transactions
      mean_transaction = mean(transactions)
      std_transaction = std(transactions)

      file_response.write(str(mean_response) + "\t" + str(std_response) + "\t")
      file_transactions.write(str(mean_transaction) + "\t" + str(std_transaction) + "\t")

    file_response.write("\n")
    file_transactions.write("\n")
  
  file_response.close()
  file_transactions.close()

  """
  for result in results:
    tests = result.getTestIDs()
    print tests
    persecond = result.getResults()
    keys = persecond.keys()
    print "length:", len(keys)
    #for key in keys: print key 
  """ 

  """
  result = TestResult(statistics_name)  
  result.addDataDict(makeDataDict(filenames[0]))
  result.print_responseTime_persecond()
  """

if __name__ == "__main__":
  try: 
    main(sys.argv)  
  except: 
    raise
  
