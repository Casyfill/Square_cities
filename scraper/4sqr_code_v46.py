#!/usr/bin/env python
# -*- coding: utf-8 -*-

############# TODOS
# [X] credentials
# [X] paths
# [X] extract place_research
# [X] overal architecture
# [ ] recheck suspecious


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
SQUARE = os.getenv('SQUARE')

def getCredentials():
  # credentials
  with open(SQUARE + 'scraper/credentials.json') as data_file:    
      credentials = json.load(data_file)
      return (credentials['data']['CLIENT_SECRET'], credentials['data']['CLIENT_ID'])



def getPlaces():
  # placeDict
  with open(SQUARE + 'scraper/places.json') as data_file:    
      return json.load(data_file)

def askForPlace():
  places = getPlaces()

  print
  for i, place in enumerate(places['data'].keys()): print '%i. %s' % (i,place)
  print '''\nPlease, select place to collect from the list\nbelow by entering index (1, for example), or "q" to exit:'''
  while True:
    index = raw_input('Answer:')
    if index=='q': 
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
          data['name']=name
          return data
          
      except Exception, e:
        print str(e)




def scraping(CLIENT_ID, CLIENT_SECRET, place, sleepTime=20):
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


  with open(SQUARE + 'data/%s.csv' % place['name'] , 'w') as csvfile:
      writer = csv.writer(csvfile, delimiter=',',
                          quotechar='"', quoting=csv.QUOTE_MINIMAL)
      writer.writerow(headers)

      # First list of requests
      newTileArray = [{'sw': place['swBound'], 'ne': place['neBound'], 'name': '0'}]
      catArrays = frsqrRequests.generateCatArray(CLIENT_SECRET, CLIENT_ID)  # list of categories

      level = 0  # detalisation level
      spreads = 1  # amount of queries need
      read = 0  # amount of queries accomplished

      totalVenues = 0  # total venuse collected

      while len(newTileArray) > 0:

          tileArray = newTileArray  # list of tiles to search
          newTileArray = []  # empty the list for next itteration
          level += 1
          print 'level %d reached: %d requests, %d venues so far!' % (level, len(tileArray), totalVenues)

          for tile in tileArray:
              ask = frsqrRequests.VenueSearch(
                  tile['sw'], tile['ne'], CLIENT_ID, CLIENT_SECRET)

              # check status
              if ask['meta']['code'] != 200:  # if status is bad

                  if ask['meta']['errorType'] == 'geocode_too_big':
                      # add detailed tile_matrix to next level list

                      newTileArray += matrix(tile['sw'],
                                             tile['ne'], tile['name'])
                      print tile['name'], ':', read, '/', spreads, ' too big, detailed!'
                      spreads += 3

                  # ПОЧЕМУ-ТО ДО ЭТОГО МЕСТА НЕ ДОХОДИТ :-(((
                  else:
                      print tile['name'], ':', ask['meta']['errorType']
                      newTileArray.append(tile)

              else:

                  p = checkArrayVsBound(tile['sw'], tile['ne'], ask[
                                        u"response"][u"venues"])

                  if len(p) >= 50:  # looks like a limit, need detalied matrix to the next list
                      newTileArray += matrix(tile['sw'],
                                             tile['ne'], tile['name'])
                      print tile['name'], ':', read, '/', spreads, ' detailed!'
                      spreads += 3

                  elif len(p) == 0:  # if answer is empty
                      read += 1
                      print tile['name'], ':', read, '/', spreads, 'zone empty'
                  else:  # if answe is not empty
                      read += 1
                      print tile['name'], ':', read, '/', spreads, 'saved: %d venues' % (len(p))

                      # save venues
                      for venue in p:
                          ID = venue['id']
                          # get details on venue
                          full_venue = frsqrRequests.getCompleteDetails(
                              ID, CLIENT_ID, CLIENT_SECRET, sleepTime)
                          v = parseVenue.parseVenue(
                              full_venue, catArrays, tile['name'], place['name'])
                          writer.writerow([v[key] for key in headers])

                      totalVenues += len(p)

              time.sleep(sleepTime)
              # try:
                  
              # except Exception, e:
              #     print str(e)
              #     print tile['name'], ':', read, '/', spreads, 'error while asking!'
              #     newTileArray.append(tile)
              #     time.sleep(sleepTime * 5)

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
