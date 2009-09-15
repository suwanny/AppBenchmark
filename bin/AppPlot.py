#!/usr/bin/env python
# 
# A Chart Plot Utility for AppScale 
# Author: Soo Hwan Park (suwanny@gmail.com)
# Date: 08/03/2009 
#
import sys, os
from xlwt import Workbook

DEBUG = False

class BMData:
	attributes_ = [
		"thread",				# thread id  
		"run", 					# run id 
		"test",					# test id  
		"start", 				# start_time
		"elapsed", 			# elapsed time
		"errors", 			# errors 
		"code", 				# HTTP response code
		"length", 			# HTTP response length 
		"error", 				# HTTP response error
		"resolve", 			# time to resolve host
		"establish", 		# time to establish connection 
		"firstbyte",		# time to first byte 
	] 

	def __init__(self, tokens):
		self.thread 		= tokens[0]
		self.run 				= tokens[1]
		self.test 			= tokens[2]
		self.start 			= tokens[3]
		self.elapsed 		= tokens[4]
		self.errors 		= tokens[5]
		self.code 			= tokens[6]
		self.length 		= tokens[7]
		self.error 			= tokens[8]
		self.resolve 		= tokens[9]
		self.establish 	= tokens[10]
		self.firstbyte 	= tokens[11]

	def __cmp__(self, other):
		return cmp(self.t_start, other.t_start)

class ResponseTime:
	def __init__(self, id, elapsed, rtime):
		self.id = id
		self.elapsed = elapsed
		self.rtime = rtime 

class TimeInterval:
	def __init__(self, id):
		self.id = id
		self.transactions = 0
		self.response = []

	def add(self, rtime ):
		self.transactions += 1
		self.response.append(rtime)

	def getAvg(self):
		sum = 0
		for data in self.response:
			sum += int(data)
		return sum / self.transactions

TIME_INTERVAL = 5

class TestResult:
	def __init__(self, name, testDict):
		self.name = name
		self.results = testDict
		self.perSecondResult = {}
		self.test_ids = testDict.keys()
		self.test_ids.sort()
		self.completed_count = len(self.results[self.test_ids[0]])
		for key in self.results.keys(): 
			self.completed_count = min(self.completed_count, len(self.results[key]))
		#self.columns = len(self.results)

		starttime = self.results[self.test_ids[0]][0].start
		persecond = self.perSecondResult
		self.max_second = 0;

		for i in range(self.completed_count):
			for id in self.test_ids: 
				record = self.results[id][i]; 
				elapsed = (int(record.start) - int(starttime))/1000
				elapsed = ( elapsed/TIME_INTERVAL ) * TIME_INTERVAL
				self.max_second = max(self.max_second, elapsed)
				key = id + "-" + str(elapsed)
				if persecond.has_key(key):
					persecond[key].add(record.elapsed)
				else: 
					persecond[key] = TimeInterval(id)
					persecond[key].add(record.elapsed)
	
	def print_responseTime_csv_all(self):
		print "Test Name: %s" % (self.name) 
		print "run", 
		for id in self.test_ids:
			print "%s\t" % id, 
		print ""
		
		results = self.results
		for row in range(self.completed_count):
			print (row + 1), 
			for id in self.test_ids:
				print	"%s\t" % results[id][row].elapsed, 			
			print ""	

	def print_responseTime_xls_all(self):
		book = Workbook()
		sheet1 = book.add_sheet(self.name)
		title = "Test Name: %s" % (self.name)
		sheet1.write(0,0,title)
		column = 1
		for id in self.test_ids:
			sheet1.write(1, column, "TEST" + id)
			column += 1

		results = self.results
		rows = range(self.completed_count)
		for row in rows:
			sheet1.write(row + 2, 0, row+1 )
			column = 1
			for id in self.test_ids:
				sheet1.write(row + 2, column, int(results[id][row].elapsed))
				column += 1	

		book.save(self.name + ".xls")

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
		rows = range(self.max_second /TIME_INTERVAL )

		for row in rows:
			sheet1.write(row + 2, 0, row*TIME_INTERVAL )
			sheet2.write(row + 2, 0, row*TIME_INTERVAL )
			column = 1
			for id in self.test_ids:
				key = id + "-" + str(row*TIME_INTERVAL)
				if results.has_key(key):
					result = results[key]
					sheet1.write(row + 2, column, result.getAvg()) 
					sheet2.write(row + 2, column, result.transactions) 
				column += 1
		"""
		for key in results.keys():
			print key
		"""

		book.save(self.name + "_bytime.xls")
		
def main(argv): 
	if len(argv) < 3 : 
		print "usage: AppPlot.py data_file name"
		sys.exit(0)

	filename = argv[1]
	print "data file:", filename
	data_file = open(filename)
	testDict = {}
	
	for line in data_file: 
		if DEBUG: print "line:", line,
		line.rstrip()
		tokens = line.split(",")
		if tokens[0] == "Thread": continue
		if DEBUG: print tokens
	
		data = BMData(tokens)	
		if testDict.has_key(data.test):
			testDict[data.test].append(data)
		else: 
			testDict[data.test] = [data]
	
	data_file.close()

	result = TestResult(argv[2], testDict)	
	#result.print_responseTime_CSV_all()
	result.print_responseTime_xls_all()
	result.print_responseTime_persecond()
	

if __name__ == "__main__":
	try: 
		main(sys.argv)	
	except: 
		raise
	
