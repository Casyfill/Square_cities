notes_on_scraping
=================
**scraping venues from FOURSQUARE API for the research purposes** 

##### foundation project, Applied Data science
##### CUSP 2015-16
##### PHilipp Kats, casyfill@gmail.com

##### scraper is based on previous version, 
##### used for projects in ITMO, Saint Petersburg, 2014
##### and Senseable city lab, Strelka Institute, 2012

#### version 5.00.00

we have semantic versioning: X.YY.ZZ 
where X - major step (project), 
YY - architecture or major feature,
ZZ - minor improvements

## TODOS
- [x] credentials
- [x] paths
- [x] extract place_research
- [x] overal architecture
- [x] checker_condition as a specific function
- [x] added main large cities to places
- [ ] add geodistance calc to checker (for now, calculate 	delta in coordinates)
- [ ] move all settings to settings.json
- [ ] logger
- [ ] gui stat_map drawer


## INSTRUCTION
Few steps to stat scraping 4sqr

1. clone this repo to your computer
2. create a developer account here (your aim is to get **client secret** and **client id**): [4square dev](https://developer.foursquare.com/)
3. Save your credentials into repo/scraper/credentials.json
4. Untrack your credentials file by doing this from repository folder: git update-index --assume-unchanged scraper/credentials.json
5. depricated: create "SQUARE" alias. Now I use "PWD" instead of "SQUARE"
6. Add all desired places (cities) to `scraper/places.json` file. Dont forget to check json validity!
7. Start scraper by sending 'python 4sqr_code_v46.py' bash command, and select place you want to scrape. All data will be saved in `data` folder. Be aware: for now script overwrite old version of same place data

## Attributes (those it can scrape for now)

- **genCategory** (one of 8 general categoris) 
- **category** (one of ~290 categories)
- **name**
- **lon**
- **lat**
- **checkIns** total
- **tips** counter
- **users** unique, total
- **createdAt** (creation date)
- **tileID** (I use tile query approach)
- **ID** (unique venue ID)
- **place** (?)
- **time** (?)
- **verified** (shows is venue account is managed by the place owner)
- **price** (average prices, if applicable)
- **rating** (average rating of the place)
- **tags** (place tag cloud)
- **photoCount** (number of photos for venue)
- **description** (textual place description)

