notes_on_scraping
=================

## TODO
- [X] credentials
- [X] extract place_data
- [X] update paths
- [X] make scraper bash-workable
- [X] extract place coordinates
- [X] overal architecture
- [ ] additional search_checker

- [ ] quit key
- [ ] to Mongo database (?)


## INSTRUCTION
Few steps to stat scraping 4sqr

1. clone this repo to your computer
2. create a developer account here (your aim is to get **client secret** and **client id**): [4square dev](https://developer.foursquare.com/)
3. Save your credentials into repo/scraper/credentials.json
4. Untrack your credentials file by doing this from repository folder: git update-index --assume-unchanged scraper/credentials.json
5. Create **SQUARE** alias to repository. Path to credentials then should beSQUARE + 'scraper/credentials.json'.
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

