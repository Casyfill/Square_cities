START SCRAPING ON SERVER
========================

- Go to server (ssh ...)
- use `ssh compute`
- create ssh key and add it to your github account help
- go to the folder of your desire and git clone git@github.com:Casyfill/Square_cities.git
- go to scraper  and untrack credentials: `git update-index --assume-unchanged scrapercredentials.json`
- now start scraper and choose credentials and a place to scrape
- when it starts, press `cntrl-z`, then write `bg`
- to check it's status: `ps ux | grep "4sq"`
- for now, you have to check all processes either through `ps ux | grep "4sq"` or checking logs (grep also recommended)
