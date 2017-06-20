START SCRAPING ON SERVER
========================

- Go to server (ssh ...)
- use `ssh compute`
- create ssh key and add it to your github account help
- go to the folder of your desire and  `git clone git@github.com:Casyfill/Square_cities.git`
- go to scraper  and untrack credentials: `git update-index --assume-unchanged scrapercredentials.json`
- fill inn the actual credentials
- now start scraper and choose credentials and a place to scrape: `python 4sqr_code.py`
- when it starts, press `cntrl-z`, then write `bg`  || Better: use screen or tmux
- to check it's status: `ps ux | grep "4sq"`
- for now, you have to check all processes either through `ps ux | grep "4sq"` or checking logs (grep also recommended)
