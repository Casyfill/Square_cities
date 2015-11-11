#!/usr/bin/env python
# -*- coding: utf-8 -*-

### scraping venues from FOURSQUARE API
### as data for the research. 

### foundation project, Applied Data science
### CUSP 2015-16
### PHilipp Kats, casyfill@gmail.com

# import requests,time,json
import sys
import csv
import time
import json
import os
import logging
import datetime
import pandas as pd

from misc.matrix import matrix
from misc.boundChecker import checkVsBound, checkArrayVsBound

from misc import parseVenue
from misc import frsqrRequests
from misc import get_settings

# sys.path.append(modulePath)
PWD = os.getenv('PWD')

class SystemLog(object):
    def __init__(self, name=None):
        self.logger = logging.getLogger(name)

    def write(self, msg, level=logging.INFO):
        self.logger.log(level, msg)

    def flush(self):
        for handler in self.logger.handlers:
            handler.flush()

sys.stderr = SystemLog('stderr')


def config_logger():
    logging.basicConfig(filename = './logs/'  + datetime.datetime.now().strftime('%b_%d_%y_%H_%M') + '.out', filemode = 'a', format = '%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level = logging.DEBUG)

def save_start_status(mainPath, credentials, place):
  '''general scraper log'''
  timestamp = datetime.datetime.now().strftime('%b_%d_%y_%H_%M')

  slog = pd.read_csv(mainPath +'/status.csv')  
  
  slog= slog.append(pd.Series({'timestamp': timestamp,
                   'credentials':credentials,
                   'place':place,
                   'status':'start'}), ignore_index=1)
    
  slog.to_csv(PWD +'/status.csv', index=0)

  return timestamp 


def save_end_status(mainPath, credentials,place,timestamp):
  print "%s finished! cred=%s" %(place, credentials) 
  slog = pd.read_csv(mainPath +'/status.csv')
  slog.status[(slog.place==place) & (slog.credentials==credentials) & (slog.timestamp==timestamp)] = 'finished'
  slog.to_csv(PWD +'/status.csv', index=0)


def detail_condition(n, tile):
  '''decide if result is suspecious enough to detail
  subject of change'''
  def condition(n, tile):
    nlim = 32  #n of venues not smaller than
    limV = 0.0073 # tile is smaller than
    limG = 0.0126 # tile is smaller than
    
    s,w =[float(x.strip()) for x in tile['sw'].split(',')]
    n,e =[float(x.strip()) for x in tile['ne'].split(',')]
    
    dCond = (n-s)<limV or (e-w)<limG
    return not(n>=nlim or dCond)


  answer = n>=50 or condition(n, tile)
  return answer


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

  with open(PWD.replace('/scraper', '/') + 'data/%s.csv' % place['name'], 'w') as csvfile:
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
    logging.info( 'level %d reached: %d requests, %d venues so far!' % (level, 
                                                                len(tileArray), 
                                                                totalVenues))
            
    for tile in tileArray:
      # actual work
      try:
        ask = frsqrRequests.VenueSearch(
        tile['sw'], tile['ne'], CLIENT_ID, CLIENT_SECRET)

        # check status
        if ask['meta']['code'] != 200:  # if status is bad
          if ask['meta']['errorType'] == 'geocode_too_big':
            
            logging.info( str(tile['name']) + ':' + str(read) + '/' + str(spreads) +  ' too big, detailed!')# TO LOGGER        
            # add detailed tile_matrix to next level list
            newTileArray += matrix(tile['sw'], tile['ne'], tile['name'])
            spreads += 3
                  
            # ПОЧЕМУ-ТО ДО ЭТОГО МЕСТА НЕ ДОХОДИТ :-(((
          else:
            # not the geocode_too_big issue
            logging.info( str(tile['name']) + ':' + str(ask['meta']['errorType']))
            newTileArray.append(tile)
                
        else: # if everything is good
          p = checkArrayVsBound(tile['sw'], tile['ne'], ask[u"response"][u"venues"])
            
          if detail_condition(len(p), tile):
            # looks like a limit, need detalied matrix to the next list
            logging.info( str(tile['name']) + ':' + str(read) + '/'+  str(spreads) + ' detailed!')# TO LOGGER
            newTileArray += matrix(tile['sw'],tile['ne'], tile['name'])
            
            spreads += 3


          elif len(p) == 0:  # if answer is empty
            read += 1
            # TO LOGGER
            logging.info( str(tile['name']) + ':' + str(read) + '/' + str(spreads) + 'zone empty')


          else:  # if answe is not empty
            read += 1
            ### HERE NEED TO ADD CHECKER
            logging.info( str(tile['name']) + ':' + str(read) + str('/') + str(spreads) + str( 'saved: %d venues' % (len(p))))
            
            with open(PWD.replace('/scraper', '/data/%s.csv' % place['name']), 'a') as csvfile:     
                writer = csv.writer(csvfile, delimiter=',',
                                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
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
        logging.info( str(e))
        logging.info( str(tile['name']) + ':' + str(read) + '/' + str(spreads) + 'error while asking!')
        newTileArray.append(tile)
        time.sleep(sleepTime * 5)

  logging.info( 'scraping %s done!, venues: %d' % (place['name'], totalVenues))


def main():
    '''main scraping function'''
    config_logger()

    # getting attributes
    
    CLIENT_SECRET, CLIENT_ID, CREDENTIAL_FILE = get_settings.chooseCredentials(PWD)
    place, pName = get_settings.askForPlace(PWD)

    TIMESTAMP = save_start_status(PWD,CREDENTIAL_FILE, pName)

    logging.info("Using credentials from %s" % CREDENTIAL_FILE)
    logging.info("Getting data for %s" % place)
    
    scraping(CLIENT_ID, CLIENT_SECRET, place, sleepTime=20)
    save_end_status(PWD,CREDENTIAL_FILE, pName, TIMESTAMP)

if __name__ == '__main__':
    main()
