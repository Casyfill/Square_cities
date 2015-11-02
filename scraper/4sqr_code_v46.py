#!/usr/bin/env python
# -*- coding: utf-8 -*-

############# TODOS
# [X] credentials
# [X] paths
# [ ] extract place_research
# [ ] overal architecture
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


# credentials
with open(SQUARE + 'scraper/credentials.json') as data_file:    
    credentials = json.load(data_file)

CLIENT_SECRET = credentials['data']['CLIENT_SECRET']
CLIENT_ID     = credentials['data']['CLIENT_ID']


# path to functionality
modulePath = SQUARE + 'scraper/misc'
# path to data
resultPath = SQUARE + 'data/'


# placeDict
placeDict = {'name': 'Plum_Island',
			 'swBound' : '41.159147, -72.218754',
			 'neBound' : '41.196776, -72.154429'
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
