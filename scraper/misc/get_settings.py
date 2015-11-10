#!/usr/bin/env python
#-*- coding: utf-8 -*-
import json
from os import listdir
import sys

def getCredentials(mainPath):
    '''get credentials. DEPRICATED: now we have to chose them from list (if there are more than one'''
    with open(mainPath + '/credentials.json') as data_file:
        credentials = json.load(data_file)
        return (credentials['data']['CLIENT_SECRET'], credentials['data']['CLIENT_ID'])

def chooseCredentials(mainPath):
    '''gives you chance to choose credentials'''

    creds = [ x for x in listdir(mainPath) if 'credent' in x]

    if len(creds)>1:
        for i, v in enumerate(creds):
            print i+1,'. ', v

    index = int(raw_input('\n\nselect credentials to use:'))-1

    with open(mainPath + '/' + creds[index]) as data_file:
        credentials = json.load(data_file)
        if credentials['data']['CLIENT_SECRET']=="MY_CLIENT_SECRET":
            print '\n\noh dear, you forgot to save your REAL credentials in that file.'
            sys.exit()

        return (credentials['data']['CLIENT_SECRET'], credentials['data']['CLIENT_ID'], creds[index])

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
