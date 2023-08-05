# scrapyx-scraperapi-proxy

Scraper API middleware for Scrapy (http://scrapy.org/)
=======================================================

Processes Scrapy requests a man in the middle proxy service using https://www.scraperapi.com


Required
--------

    python version >= 3.6


Install
--------

Checkout the source and run

    python setup.py install

Or

    pip install scrapyx-scraperapi-proxy
    

settings.py
-----------

    # Activate the middleware
    SCRAPERAPI_ENABLED = True
    
    # The API key 
    SCRAPERAPI_KEY='your API key'

    # JS Redering 
    SCRAPERAPI_RENDER = False

    # Premium account
    SCRAPERAPI_PREMIUM = False

    # Geographic Location
    SCRAPERAPI_COUNTRY_CODE = '' # 'US', 'UK', ...

    DOWNLOADER_MIDDLEWARES = {
        'scrapyx_scraperapi.ScraperApiProxyMiddleware': 610,
    }


