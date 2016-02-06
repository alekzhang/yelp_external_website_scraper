# -*- coding: utf-8 -*-
from urlparse import urlparse,parse_qs
import scrapy
from yelp.items import YelpItem
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

class PharmacyEmailSpider(scrapy.Spider):
    name = "pharmacy_email"
    allowed_domains = ["yelp.com"]
    start_urls = (
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&ns=2',
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&start=10',
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&start=20',
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&start=30',
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&start=40',
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&start=50',
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&start=60',
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&start=70',
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&start=80',
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&start=90',
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&start=100',
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&start=110',
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&start=120',
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&start=130',
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&start=140',
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&start=150',
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&start=160',
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&start=170',
        'http://www.yelp.com/search?find_desc=pharmacies&find_loc=Amadora%2C+Portugal&start=180',
    )

    def parse(self, response):
      hxs = HtmlXPathSelector(response)
      businesses = hxs.select("//a[@class='biz-name']")
      for business in businesses:
        url = 'http://yelp.com{}'.format(''.join(business.select("@href").extract()))
        yield Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
      hxs = HtmlXPathSelector(response)
      item = YelpItem()
      website_div = hxs.select("//div[@class='biz-website']")
      yelp_redirect_url = website_div.select("a/@href").extract()
      # address_div = hxs.select("//address")
      # item['street_address'] = hxs.select("//address/span[itemprop='streetAddress']").extract()
      # item['postal_code'] = ""
      # item['city'] = ""
      if(yelp_redirect_url != []):
        site_parse = urlparse(''.join(yelp_redirect_url))
        site_qs = parse_qs(site_parse.query)
        site_url = site_qs['url']
        site = ''.join(site_url)
        item['external_website'] = site
        yield item