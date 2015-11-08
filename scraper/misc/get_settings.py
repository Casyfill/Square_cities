#!/usr/bin/env python
#-*- coding: utf-8 -*-
import json

def getCredentials(mainPath):
    # credentials
    with open(mainPath + '/credentials.json') as data_file:
        credentials = json.load(data_file)
        return (credentials['data']['CLIENT_SECRET'], credentials['data']['CLIENT_ID'])


def getPlaces(mainPath):
    '''looks for places in json and gives you
       an array of name:coord_bound pairs'''

    with open(mainPath + '/places.json') as data_file:
        return json.load(data_file)


def askForPlace(mainPath):
    '''ask user to choose a place to scrape
       from the provided list'''

    places = getPlaces(mainPath)  # get list of places

    print
    for i, place in enumerate(places['data'].keys()):
        print '%i. %s' % (i+1, place)
    print '''\nPlease, select place to collect from the list\nbelow by entering index (1, for example), or "q" to exit:'''
    while True:
        index = raw_input('Answer:')
        if index == 'q':
            print 'exiting'
            break
        else:
            try:
                ix = int(index) -1
                if ix > len(places['data'].keys()):
                    print 'incorrect index, try one more time'
                else:
                    print places['data'].keys()[ix], 'chosen.'
                    name = places['data'].keys()[ix]
                    data = places['data'][name]
                    data['name'] = name
                    return data

            except Exception, e:
                print str(e)