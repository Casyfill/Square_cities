#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import pandas as pd


def main(key, mypath):
	'''aggregate all csv files for place specfied 
	   (technically just a keword mentioned in all related csv files''' 
	   	

	onlyfiles = [ f for f in os.listdir(mypath) if (os.path.isfile(os.path.join(mypath,f)) and ('.csv' in f) and (key in f)) ]

	df = pd.concat([pd.read_csv(os.path.join(mypath,f)) for f in onlyfiles]).drop_duplicates(subset='ID')
	df.to_csv(os.path.join(mypath, key +'_all.csv'))
	print '%s rows total, Saved to '%len(df), os.path.join(mypath, key +'_all.csv')

		



if __name__ == '__main__':
	if len(sys.argv)>2:
		main(sys.argv[1], sys.argv[2])
	elif len(sys.argv)==2:
		p = os.getenv('PWD').replace('/tools','/data')
		main(sys.argv[1],p)
	else:
		print 'need kewName to filter files!'



