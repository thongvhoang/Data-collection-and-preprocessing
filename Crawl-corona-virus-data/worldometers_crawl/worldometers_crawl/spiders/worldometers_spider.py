# Scrape information from a website
# Collect corona infection information in countries: Indonesia and Philippines

import scrapy #from scrapy import Spider
import numpy as np
from .process_corona_data import process_data #https://blog.teko.vn/2019/02/01/bay-import-trong-python/
import pandas as pd
from influxdb import InfluxDBClient
from time import time


class WorldometersSpider(scrapy.Spider): # from scrapy import Spider -> Spider
    name = "worldometers" # Define name of Spider
        
    def start_requests(self):

        #   urls: List of urls are scrapped by Spider. Spider downloads all of urls's data.
        urls = [
            'https://www.worldometers.info/coronavirus/country/indonesia/',
            'https://www.worldometers.info/coronavirus/country/philippines/',
        ]
        
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        
        page = response.url.split("/")[-2]
        filename = 'coronavirus-%s.html' % page
        db = InfluxDBClient("localhost", 8086)
        db.switch_database("worldometers")



        total_cases_data = response.xpath("//div//script[@type='text/javascript']")[2].get() # Don't use "" in @atribute=''
        daily_newcases_data = response.xpath("//div//script[@type='text/javascript']")[3].get() 
        daily_newdeaths_data = response.xpath("//div//script[@type='text/javascript']")[6].get()
        new_cases_and_new_recovered_data = response.xpath("//div//script[@type='text/javascript']")[7].get()
        titles_data = response.xpath("//h3").getall()
        
        dataset_list = {"Date":process_data(total_cases_data).getDate(),
                        "Country": [page.title() for i in range(len(process_data(total_cases_data).getDate()))],
                        "Total cases": process_data(total_cases_data).getNumberData(),
                        "Daily new deaths": process_data(daily_newdeaths_data).getNumberData(),
                        "Daily new recoveries": process_data(new_cases_and_new_recovered_data).getNumberData()}
        dataset = pd.DataFrame(data=dataset_list)
        dataset.index = [i+1 for i in range(len(dataset))]
        # dataset.to_csv('coronavirus.csv',encoding='utf-8', index=False)
        yield dataset
    def Res():
        dataset = pd.DataFrame()
        for data in parse(self,response):
            dataset.append(data)
        print(dataset)