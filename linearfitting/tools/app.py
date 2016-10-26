#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Copyright (C) yanghongshun@gmail.com

import csv
import os
import sys
import getopt
import ConfigParser
import random
from scipy import stats


def readCsvDataFromFile(startLine,spliter,csvPath,quiet=0):
	
	data = []
	
	if quiet==0:
		print "reading file: " + csvPath 
	
	if not os.path.isfile(csvPath):
		print "file not exist!"
		sys.exit()
		
	csvfile=csv.reader(open(csvPath, 'r'),delimiter=spliter)
	
	if quiet==0:
		print "storing data"
	
	for line in csvfile:
			data.append(line)
	
	if startLine != '':
		for i in range(startLine):
			#print i
			del data[0]

	return data

def saveCsvDataToFile(title,data,file_path,fmt=''):
	
	print "saving data to file :"+ file_path
	
	if os.path.isfile(file_path):
		os.remove(file_path)
	
	file_handle = open(file_path,'wb')
	if fmt=='':
		csv_writer = csv.writer(file_handle)##delimiter=' ',
	else:
		csv_writer = csv.writer(file_handle,fmt)##delimiter=' ',
	if len(title) >0 :
		csv_writer.writerow(title)
	csv_writer.writerows(data)
	
	file_handle.close()
	
	print "saved ok"


def caclR(startline,spliter,xysum,startcol,need,file_path,quiet):
	data=readCsvDataFromFile(startline,spliter,file_path,quiet)
	
	##need
	##保留的行
	needRowLists = need.split(",")
	
	#print needRowLists
	needList = []
	for n in range(len(needRowLists)):
		needList.append(int(needRowLists[n]))
		print data[int(needRowLists[n])]
	
	#print data
	xylist=range(len(data))
	
	x=[]
	y=[]
	for i in range(len(data)):
		x.append(float(data[i][startcol]))
		y.append(float(data[i][startcol+1]))
	
	if xysum>len(xylist):
		print len(xylist)
		print 'xysum is big than data'
		sys.exit() 
	
	
		
	xyslice = random.sample(xylist, xysum)
	#print xyslice
	#从xyslice中检查获取的元素index是否包含need
	xyslice_isnot_need = []
	xyslice_is_need = []
	delnum=0
	for s in xyslice:
		if s not in needList:
			xyslice_isnot_need.append(s)
		else:
			xyslice_is_need.append(s)
			

	delnum = len(needList)-len(xyslice_is_need)
	for d in range(delnum):
		xyslice_isnot_need.pop()
	#合并xyslice_isnot_need 和 needlist
	xyslice_isnot_need.extend(needList)
	
	xyslice=[]
	xyslice.extend(xyslice_isnot_need)
	#print xyslice		
	
	xv=[x[i] for i in xyslice]
	yv=[y[j] for j in xyslice]
	
	xy=[data[k] for k in xyslice]
	
	#print xy
	#print xv
	#print yv
	
	gradient, intercept, r_value, p_value, std_err = stats.linregress(xv,yv)	
	
	#print "Count(X,Y):",len(xv)
	#print "R^2:",r_value**2

	print 'P:',p_value	
	print 'R:',r_value
	
	#if r_value<0:
		#sys.exit(2)
	#if p_value<0:
		#sys.exit(2)

	res=[r_value**2,xy,r_value]
	
	return res
	

###main
def main(argv):

	DIR_RESULT = './../result/'

	#-i
	input_file_path = ''
	xysum = 0
	r=0
	startcol=1
	startrow =1
	operation=1
	rvalue=1
	
	need = ''##1,2,10
	
	try:
		opts, args = getopt.getopt(argv,"hi:s:r:c:t:o:x:n:",["input_file=","xysum=","rr=","startcol=",'title=','operation=','rvalue=','need='])
	except getopt.GetoptError:
		print 'please -h see help'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'hello linear fitting'
			print '-i input file to be used'
			print '-s (x,y) need to be used by line'
			print '-c first column need to be used (start 0)'
			print '-t input file has title or no,also start row'
			print '-o 1 表示rr的值大于-r 传递的值'
			print '-x 1 表示r的值大于0'
			print '-n 保留哪些行，用逗号分隔ps:减1'
			print './app.py -i ../data/0505/2.csv -s 40(need x,y nums) -o 1(1:>rr;0:<rr) -r 0.5( rr) -x 1(1:r>0;0:r<0) -n 3,5 -c 1(start cols)  -t(start rows) 1'
			sys.exit()
		elif opt in ("-i","--input_file"):
			input_file_path = arg
		elif opt in ("-s","--xysum"):
			xysum = int(arg)
		elif opt in ("-r","--rr"):
			r=float(arg)
		elif opt in ("-c","--startcol"):
			startcol=int(arg)
		elif opt in ("-t","--title"):
			startrow = int(arg)
		elif opt in ("-o","--operation"):
			operation=int(arg)
		elif opt in ("-x","--rvalue"):
			rvalue=int(arg)
		elif opt in ("-n","--need"):
			need=arg

	if cmp(input_file_path,'')!=0:		
		input_file_basename=os.path.basename(input_file_path)
		#print input_file_basename
		input_file_dirname=os.path.split(os.path.dirname(input_file_path))
		#print input_file_dirname
		output_file_dirname = DIR_RESULT+input_file_dirname[1]
		#print	output_file_dirname
		if os.path.exists(output_file_dirname)==False:
			#mkdir dir result
			os.mkdir(output_file_dirname)
		
		

		
		i=0
		if operation ==1:
			while True:
				i=i+1
				result=caclR(startrow,',',xysum,startcol,need,input_file_path,1)
				print '计算次数:',i,'当前R^2:',result[0],'当前R:',result[2]
				if rvalue ==1:	
					if result[2]>0:##r>0
						if result[0]>=r:
							break
				elif rvalue==0:
					if result[2]<0:##r<0
						if result[0]>=r:
							break
		elif operation==0:
			while True:
				i=i+1
				result=caclR(startrow,',',xysum,startcol,need,input_file_path,1)
				print '计算次数:',i,'当前R^2:',result[0],'当前R:',result[2]
				if rvalue ==1:
					if result[2]>0:##r>0
						if result[0]<r:
							break
				elif rvalue ==0:
					if result[2]<0:##r<0
						if result[0]<r:
							break
		if startrow>0:
			data=readCsvDataFromFile(0,',',input_file_path)
			titleRows=data[0:startrow]
		else:
			titleRows=[]
		file_result_R_name='rr_'+str(result[0])+'_count_'+str(xysum)+'_'+input_file_basename
		output_file_R_path = output_file_dirname+'/'+file_result_R_name
		saveCsvDataToFile(titleRows,result[1],output_file_R_path)
			


###app

if __name__=='__main__':
	if len(sys.argv) <=1:
		print "please use option -h"
	else :
		main(sys.argv[1:])
