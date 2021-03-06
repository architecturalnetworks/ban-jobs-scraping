# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.project import data_path
from scraper.crawl import is_in_aws


class ProxiesSpider(scrapy.Spider):
    name = 'proxies'
    allowed_domains = ['free-proxy-list.net']
    start_urls = ['http://free-proxy-list.net/']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'rotating_proxies.middlewares.RotatingProxyMiddleware': None,
        }
    }

    def parse(self, response):
        # get all proxies and their ports
        proxy_table = response.css('table#proxylisttable')
        proxy_table_rows = proxy_table.xpath(
            './/tr')[1:]  # remove table header
        filename = 'proxies.txt'
        if is_in_aws():
            mydata_path = "/tmp/"+filename
        else:
            mydata_path = data_path(filename)

        with open(mydata_path, 'w') as fout:
            for row in proxy_table_rows:
                ip = row.xpath('./td[1]/text()').extract_first()
                port = row.xpath('./td[2]/text()').extract_first()
                if ip and port:
                    proxy = ':'.join([ip, port])
                    print(proxy)
                    fout.write(proxy)
                    fout.write('\n')
        fout.close()
