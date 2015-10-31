notes_on_scraping
=================

Here will be a small instruction on data scraping.

1. As we need a lot of data, lets EACH create a 4sqr developer account here: [4square dev](https://developer.foursquare.com/)

2. I am going to refactor my scraper in one or two days, as it has some flaws (sometimes 4square returns ~4 venues in the dence areas, so I need to add re-checker on those suspecious returns. Also, I will add support for command-line start, remove all exposed pathes and some minor fixtures.

3. Please, let's agree that each of us will keep his credentials in the **credentials.json** file: it is a template for now, I will add it to .gitignore after this commit. Let's also agree on using **SQUARE** alias for our pathes, so **SQUARE** will be root folder of this repository. Path to credentials will be SQUARE + 'scraper/credentials.json' this way.