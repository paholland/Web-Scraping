# Web Scraping - Mission to Mars

### Objective: 
Build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page

Web Scraping in Jupyter Notebook (scrapes the most recent NASA news, scrapes the URL for the featured image, the latest weather from twitter, scrapes all 4 hemisphere umage urls, the Mars facts HTML table)

Flask App (has routes for loading the webpage and scraping the content, connect/fetches/inserts data to and from a mongoDB without error, returns a rendered template and passes it a variable of the scraped data; calls scrape method from and external python module)

Web (landing page loads even before scraping; index.html includes a button to the scrape route; uses jinja to load data from the variable passed by flask; uses bootstrap to style the webpage; facts talve renders correctly

### Tools used: Flask, BeautifulSoup, Mongo DB, 




