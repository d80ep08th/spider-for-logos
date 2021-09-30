import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exporters import CsvItemExporter
import csv

file = open('websites.csv')
csvreader = csv.reader(file)
rows = []

for row in csvreader:
    rows.append(row)
    
urls = []
for row in rows:
    new_row = "".join(row)
    urls.append(new_row)
    
https = 'https://www.'
domains = [https + url for url in urls]




class logo_crawl(scrapy.Spider):
    name = "logo_links"
    start_urls = domains

    def parse(self, response):
        LOGO = response.xpath('//*[@*[contains(., "logo")]]')
        FAVICO = response.xpath('//*[@*[contains(., "favico")]]')
        LOGO_SRC = LOGO.xpath('@src')
        FAVICO_HREF = FAVICO.xpath('@href')
        
        for logo in LOGO_SRC.extract():
            yield {
                'domain_name': response.url,
                'logo_link': logo,
                'favico': FAVICO_HREF.extract()
            }

#put all the logo urls in the file LOGO.csv
process = CrawlerProcess(settings = {
#    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    "FEEDS": {
            "newly_crawled_01.csv": {
            "format": "csv",
            'encoding': 'utf8',
            'overwrite': True
            },
    },
    "LOG_LEVEL": "INFO"
})

process.crawl(logo_crawl)

process.start() # the script will block here until all crawling jobs are finished

