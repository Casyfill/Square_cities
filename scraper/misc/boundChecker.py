#!/usr/bin/env python
# -*- coding: utf-8 -*-

def checkVsBound(sw,ne, lat, lon):
	s,w =[float(x.strip()) for x in sw.split(',')]
	n,e =[float(x.strip()) for x in ne.split(',')]
	return (n>=lat >=s) and (e >= lon >=w)


def checkArrayVsBound(sw,ne, array):
	return [x for x in array if checkVsBound(sw,ne, x['location']['lat'],x['location']['lng'])]



# swBound = '33.329980, -103.567494'
# neBound = '37.384914, -94.111012'

# l = [{'location':{'lat':0, 'lon':1}},
# 	 {'location':{'lat':34, 'lon':-96}},
# 	 {'location':{'lat':35, 'lon':-97}},
# 	 {'location':{'lat':1, 'lon':0}}
# 	]

# print checkArrayVsBound(swBound,neBound,l)

