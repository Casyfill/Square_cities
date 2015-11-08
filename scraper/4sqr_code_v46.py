#!/usr/bin/env python
# -*- coding: utf-8 -*-

### scraping venues from FOURSQUARE API
### as data for the research. 

### foundation project, Applied Data science
### CUSP 2015-16
### PHilipp Kats, casyfill@gmail.com

### scraper is based on previous version, 
### used for projects in ITMO, Saint Petersburg, 2014
### and Senseable city lab, Strelka Institute, 2012

# TODOS
# [X] credentials
# [X] paths
# [X] extract place_research
# [X] overal architecture
# [ ] recheck suspecious
# [ ] logger


# import requests,time,json
import sys
import csv
import time
import json
import os

from misc.matrix import matrix
from misc.boundChecker import checkVsBound, checkArrayVsBound

from misc import parseVenue
from misc import frsqrRequests

# sys.path.append(modulePath)
SQUARE = os.getenv('PWD')


def getCredentials():
    # credentials
    with open(SQUARE + '/credentials.json') as data_file:
        credentials = json.load(data_file)
        return (credentials['data']['CLIENT_SECRET'], credentials['data']['CLIENT_ID'])


def getPlaces():
    '''looks for places in json and gives you
       an array of name:coord_bound pairs'''

    with open(SQUARE + '/places.json') as data_file:
        return json.load(data_file)


def askForPlace():
    '''ask user to choose a place to scrape
       from the provided list'''

    places = getPlaces()  # get list of places

    print
    for i, place in enumerate(places['data'].keys()):
        print '%i. %s' % (i, place)
    print '''\nPlease, select place to collect from the list\nbelow by entering index (1, for example), or "q" to exit:'''
    while True:
        index = raw_input('Answer:')
        if index == 'q':
            print 'exiting'
            break
        else:
            try:
                ix = int(index)
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


def scraping(CLIENT_ID, CLIENT_SECRET, place, sleepTime=20):
  '''main scraping engine. everythin is in here'''
  
  headers = ['genCategory',   # csv headers (params)
             'category',
             'name',
             'lon',
             'lat',
             'checkIns',
             'tips',
             'users',
             'createdAt',
             'tileID',
             'ID',
             'query',
             'time',
             'verified',
             'price',
             'rating',
             'tags',
             'photoCount',
             'description']

  with open(SQUARE.replace('/scraper', '/') + 'data/%s.csv' % place['name'], 'w') as csvfile:
    '''non-stop writing''' ## actually this is bad approach, need to change this
        
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(headers)

    # First list of requests
    newTileArray = [{'sw': place['swBound'],
                     'ne': place['neBound'], 'name': '0'}]
    # list of categories
    catArrays = frsqrRequests.generateCatArray( CLIENT_SECRET, CLIENT_ID) 

    #VARIABLES
    level = 0  # detalisation level
    spreads = 1  # amount of queries required
    read = 0  # amount of queries accomplished
    totalVenues = 0  # total venuse collected

    while len(newTileArray) > 0:  # while there is some queries in line
      tileArray = newTileArray  # list of tiles to search
      newTileArray = []  # empty the list for next itteration
      level += 1 ## level of precision (smaller and smaller area)

      ## TO LOG
      print 'level %d reached: %d requests, %d venues so far!' % (level, 
                                                                  len(tileArray), 
                                                                  totalVenues)
            
      for tile in tileArray:
        # actual work
        try:
          ask = frsqrRequests.VenueSearch(
          tile['sw'], tile['ne'], CLIENT_ID, CLIENT_SECRET)

          # check status
          if ask['meta']['code'] != 200:  # if status is bad
            if ask['meta']['errorType'] == 'geocode_too_big':
                    
              # add detailed tile_matrix to next level list
              newTileArray += matrix(tile['sw'], tile['ne'], tile['name'])
              # TO LOGGER
              print tile['name'], ':', read, '/', spreads, ' too big, detailed!'
              spreads += 3
                  
              # ПОЧЕМУ-ТО ДО ЭТОГО МЕСТА НЕ ДОХОДИТ :-(((
            else:
              # not the geocode_too_big issue
              print tile['name'], ':', ask['meta']['errorType']
              newTileArray.append(tile)
                
          else: # if everything is good
            p = checkArrayVsBound(tile['sw'], tile['ne'], ask[u"response"][u"venues"])
            
            if len(p) >= 50:  
              # looks like a limit, need detalied matrix to the next list
              newTileArray += matrix(tile['sw'],tile['ne'], tile['name'])
              # TO LOGGER
              print tile['name'], ':', read, '/', spreads, ' detailed!'
              spreads += 3
            elif len(p) == 0:  # if answer is empty
              read += 1
              # TO LOGGER
              print tile['name'], ':', read, '/', spreads, 'zone empty'
            else:  
              # if answe is not empty
              read += 1
              ### HERE NEED TO ADD CHECKER
              print tile['name'], ':', read, '/', spreads, 'saved: %d venues' % (len(p))

              # save venues
              for venue in p:
                ID = venue['id']

                # get details on venue
                full_venue = frsqrRequests.getCompleteDetails( 
                      ID, CLIENT_ID, CLIENT_SECRET, sleepTime)
                v = parseVenue.parseVenue(
                      full_venue, catArrays, tile['name'], place['name'])
                      
                # SAVING DATA
                writer.writerow([v[key] for key in headers])
                totalVenues += len(p) 
                      
                time.sleep(sleepTime) # TIME TO SLEEP. DON'T MAKE SERVER ANGRY !!!

        except Exception, e:
          print str(e)
          print tile['name'], ':', read, '/', spreads, 'error while asking!'
          newTileArray.append(tile)
          time.sleep(sleepTime * 5)

      print 'scraping %s done!, venues: %d' % (place['name'], totalVenues)


def main():
    '''main scraping function'''

    # getting attributes
    CLIENT_SECRET, CLIENT_ID = getCredentials()
    place = askForPlace()
    # print place
    print '\n\n\n'
    scraping(CLIENT_ID, CLIENT_SECRET, place, sleepTime=20)


if __name__ == '__main__':
    main()
