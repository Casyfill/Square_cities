#!/usr/bin/env python
# -*- coding: utf-8 -*-

def matrix(swBound,neBound, boundID): 
	vert, gor = 2,2
	swBound =[float(x) for x in swBound.split(',')]
	neBound =[float(x) for x in neBound.split(',')]
	r = []

	
 	verDelta = (neBound[0]-swBound[0])/vert
	gorDelta = (neBound[1]-swBound[1])/gor

	for i in xrange(vert):
		for j in xrange(gor):
			s = str((swBound[0]+ i*verDelta))
			w = str((swBound[1]+ j*gorDelta)) 

			n=str((swBound[0]+ (i+1)*verDelta))
			e=str((swBound[1]+ (j+1)*gorDelta))

			sw = s + ',' + w
			ne = n + ',' + e
			ll =str((float(n) + float(s))/2) + ',' + str((float(e) + float(w))/2)

			tileID = boundID + '_' + str(i) + str(j)

			r.append({'sw':sw, 'ne':ne, 'name':tileID, 'll':ll})
	return r



# print list(matrix('0,0','2,4','I'))

def multiMatrix(swBound, neBound, boundID, number):
	

	swBound =[float(x) for x in swBound.split(',')]
	neBound =[float(x) for x in neBound.split(',')]

	verDelta = (neBound[0]-swBound[0])/number
	gorDelta = (neBound[1]-swBound[1])/number

	for i in xrange(number):
		for j in xrange(number):
			s = str((swBound[0]+ i*verDelta))
			w = str((swBound[1]+ j*gorDelta)) 

			n=str((swBound[0]+ (i+1)*verDelta))
			e=str((swBound[1]+ (j+1)*gorDelta))

			sw = s + ',' + w
			ne = n + ',' + e
			ll =str((float(n) + float(s))/2) + ',' + str((float(e) + float(w))/2)

			tileID = boundID + '_' + str(i) + str(j)

			r.append({'sw':sw, 'ne':ne, 'name':tileID, 'll':ll})
	return r



