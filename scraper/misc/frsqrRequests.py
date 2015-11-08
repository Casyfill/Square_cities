#!/usr/bin/env python
# -*- coding: utf-8 -*-

# all documentation is here
# https://developer.foursquare.com/docs/venues/explore
import json, requests, time

def requestsCats(CLIENT_SECRET, CLIENT_ID):
	pl = {'client_id':CLIENT_ID,
			'client_secret':CLIENT_SECRET,
			'v':'20140723'
		}
	completeUrl = 'https://api.foursquare.com/v2/venues/categories'
	j = requests.get(completeUrl, params=pl)
	# print j.url
	if json.loads(j.text)['meta']["code"] == 200:
		return json.loads(j.text)["response"]["categories"]
	else:
		print 'error requesting categories from Foursquare, error code: ',json.loads(j.text)['meta']["code"]

def generateCatArray(CLIENT_SECRET, CLIENT_ID):

	#  gets json hierarchy of cats from 4sqr API
	data = requestsCats(CLIENT_SECRET, CLIENT_ID)
	
	cats = {}
	for x in data:
		cats[x['name']]=[x['name']]
		for y in x['categories']:
			cats[x['name']].append(y['name'])
			if 'categories' in y.keys() and len(y['categories'])>0:
				for z in y['categories']:
					cats[x['name']].append(z['name'])
	return cats
	# pprint.pprint(cats, indent=4)



def getCompleteDetails(id, CLIENT_ID,CLIENT_SECRET, sleepTime):
	'''returns detailed venue profile'''

	pl = {'client_id':CLIENT_ID,
			'client_secret':CLIENT_SECRET,
			'v':'20140723'
	}
	completeUrl = "https://api.foursquare.com/v2/venues/" + str(id)
	j = requests.get(completeUrl, params=pl)
	if json.loads(j.text)['meta']["code"] == 200:
		return json.loads(j.text)["response"]["venue"]
	else:
		print j.text
	time.sleep(sleepTime)


def VenueSearch(sw,ne,CLIENT_ID,CLIENT_SECRET):
	'''venue search, returns list of compact venues 
	for specific area'''
	
	baseUrl = "https://api.foursquare.com/v2/venues/search" #sw=%s&ne=%s&client_id=%s&client_secret=%s&intent=browse" % (sw, ne, CLIENT_ID, CLIENT_SECRET)
	payload = {'sw':sw,
				'ne':ne,
				'client_id':CLIENT_ID,
				'client_secret':CLIENT_SECRET,
				'intent':'browse',
				'v':'20151105',
				'limit':50,
				"m":'foursquare'
				}

	return json.loads(requests.get(baseUrl, params=payload).text)


# 'v':'20140723',
