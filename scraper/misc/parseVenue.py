#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time,sys

def genCategory(cat, catArrays):
	if cat==None:
		return None
	else:
		for c in catArrays.keys():
			if cat in catArrays[c]:
				return c

def parseVenue(full_venue, catArrays, tileID, place):
	
	try:
		createdAt = time.gmtime(full_venue["createdAt"])
	except:
		createdAt = 0

	try:
		c= full_venue['categories'][0]['name']
	except:
		c = 'None'

	if 'price' in full_venue.keys():
		price = str(full_venue['price']['tier'])
	else:
		price = '-1'

	if 'rating' in full_venue.keys():
		rating = str(full_venue['rating'])
	else:
		rating = '-1'

	if "tags" in full_venue.keys():
		tags = ';'.join(full_venue['keys'])
	else:
		tags = ''

	if 'description' in full_venue.keys():
		description = full_venue['description']
	else:
		description = ''




	venueDict = { 'genCategory': genCategory(c,catArrays),
		'category': c.encode('utf-8'),
		'name': full_venue['name'].encode('utf-8'),
	 	'lon': full_venue['location']['lng'],
	 	'lat': full_venue['location']['lat'],
	 	'checkIns': full_venue['stats']['checkinsCount'],
	 	'tips': full_venue['stats']['tipCount'],
	 	'users': full_venue['stats']['usersCount'],
	 	'createdAt': time.strftime("%Y.%m.%d ", createdAt),
	 	'tileID': tileID,
	 	'ID':full_venue['id'].encode('utf-8'),
	 	'place':place.encode('utf-8'),
	 	'time':time.strftime("%Y.%m.%d %H:%M:%S "),
	 	'verified': str(full_venue['verified']),
	 	'price': price,
	 	'rating': rating,
	 	'tags': tags.encode('utf-8'),
	 	'photoCount': str(full_venue['photos']['count']),
	 	'description': description.encode('utf-8')
	 	}

	return venueDict

