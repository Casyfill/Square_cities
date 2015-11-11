#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pandas as pd
import sys


def diff(path1, path2):
	'''show difference between two csv'''
	
	name1 = path1.split('/')[-1]
	name2 = path2.split('/')[-1]

	df1 = pd.read_csv(path1)
	df2 = pd.read_csv(path2)
	
	print '%s : %d rows' % (name1, len(df1))
	print '%s : %d rows' % (name2, len(df2))

	ID1 = df1.ID.tolist()
	ID2 = df2.ID.tolist()

	diff1 = [x for x in ID1 if x not in ID2]
	diff2 = [x for x in ID2 if x not in ID1]

	print '\n\n\n%s: unique rows: %d' % (name1, len(diff1))
	print '\n\n\n%s: unique rows: %d' % (name2, len(diff2))
	
	# call for action
	print '\n\n\n1.show diff 1\n2. show diff 2\n3.quit'

	while True:
		try:
			a = int(raw_input('print chose further action, please'))
			if a not in (1,2,3):
				print 'incorrect. try one more time'
			else:
				if a==3: 
					print 'bye! Thanks for the fish!'
					return
				elif a==1:
					print df1[df1.ID.isin(ID1)].head(10)
				elif a==2:
					print df2[df2.ID.isin(ID2)].head(10)


		except:
			print 'incorrect. try one more time'

		

if __name__ == '__main__':
	diff(sys.argv[1],sys.argv[1])