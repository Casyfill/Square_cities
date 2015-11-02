#!/usr/bin/env python
# -*- coding: utf-8 -*-

############# TODOS
# [X] credentials
# [ ] paths
# [ ] extract place_research
# [ ] overal architecture
# [ ] 

#  two modes: server (s) and local (l)
mode = 's'  # 'l'


#TODO: need to rewrite that
pathes = {'l': {'modulePath': "/Users/casy/Dropbox (RN&IA'N)/Projects/Kats/Afisha/4sqr_scrape/code/misc/",
                'resultPath': "/Users/casy/Dropbox (RN&IA'N)/Projects/Kats/Afisha/4sqr_scrape/data/"},
          's': {'modulePath': "/root/4sqr_scraper/code/misc",
                'resultPath': "/root/4sqr_scraper/data/"}}

modulePath, resultPath = pathes[mode]['modulePath'], pathes[mode]['resultPath']

# import requests,time,json
import sys
import csv
import time
import json
import os
# sys.path.append(modulePath)
SQUARE = os.genenv('SQUARE')

with open(SQUARE + 'scraper/credentials.json') as data_file:    
    credentials = json.load(data_file)

CLIENT_SECRET = credentials['data']['CLIENT_SECRET']
CLIENT_ID     = credentials['data']['CLIENT_ID']


from matrix import matrix
from boundChecker import checkVsBound, checkArrayVsBound

import parseVenue
import frsqrRequests

# placeDict
placeDict = {'name': 'Oklahoma',
			 'swBound' : '33.329980, -103.567494',
			 'neBound' : '37.384914, -94.111012'
			}

sleepTime = 20
place = placeDict['name']
swBound = placeDict['swBound']
neBound = placeDict['neBound']
#TODO change path
resultPath += (place + '.csv')


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
           'place',
           'time',
           'verified',
           'price',
           'rating',
           'tags',
           'photoCount',
           'description']


with open(resultPath, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(headers)

    # First list of requests
    newTileArray = [{'sw': swBound, 'ne': neBound, 'name': '0'}]
    catArrays = frsqrRequests.generateCatArray(
        CLIENT_SECRET, CLIENT_ID)  # list of categories

    level = 0  # уровень детализации
    spreads = 1  # количество необходимых запростов
    read = 0  # количество результативных запросов

    totalVenues = 0  # счетчик собранных мест

    while len(newTileArray) > 0:

        tileArray = newTileArray  # рабочий список
        newTileArray = []  # обнуляем список для следующей итерации
        level += 1
        print 'level %d reached: %d requests, %d venues so far!' % (level, len(tileArray), totalVenues)

        for tile in tileArray:

            try:
                ask = frsqrRequests.VenueSearch(
                    tile['sw'], tile['ne'], CLIENT_ID, CLIENT_SECRET)

                # проверка статусов
                if ask['meta']['code'] != 200:  # если ответ не нормальный

                    if ask['meta']['errorType'] == 'geocode_too_big':
                        # добавляем детализированную матрицу к листу следующего
                        # уровня
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

                    if len(p) >= 50:  # если запросов 50, то, скорее всего, включен лимит, нужна детализация
                        # добавляем детализированную матрицу к листу следующего
                        # уровня
                        newTileArray += matrix(tile['sw'],
                                               tile['ne'], tile['name'])
                        print tile['name'], ':', read, '/', spreads, ' detailed!'
                        spreads += 3

                    elif len(p) == 0:  # если ответ путой
                        read += 1
                        print tile['name'], ':', read, '/', spreads, 'zone empty'
                    else:  # если ответ не пустой
                        read += 1
                        print tile['name'], ':', read, '/', spreads, 'saved: %d venues' % (len(p))

                        for venue in p:
                            ID = venue['id']
                            # Получаю полные данные по Venue
                            full_venue = frsqrRequests.getCompleteDetails(
                                ID, CLIENT_ID, CLIENT_SECRET, sleepTime)
                            v = parseVenue.parseVenue(
                                full_venue, catArrays, tile['name'], place)
                            writer.writerow([v[key] for key in headers])

                        totalVenues += len(p)

                time.sleep(sleepTime)
            except Exception, e:
                print str(e)
                print tile['name'], ':', read, '/', spreads, 'error while asking!'
                newTileArray.append(tile)
                time.sleep(sleepTime * 5)

    print 'scraping %s done!, venues: %d' % (place, totalVenues)
