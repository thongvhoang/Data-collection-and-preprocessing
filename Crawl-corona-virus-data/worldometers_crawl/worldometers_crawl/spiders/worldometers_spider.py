# Scrape information from a website
# Collect corona infection information in countries: Indonesia and Philippines

import scrapy #from scrapy import Spider
import numpy as np
from .process_corona_data import process_data #https://blog.teko.vn/2019/02/01/bay-import-trong-python/
import pandas as pd


class WorldometersSpider(scrapy.Spider): # from scrapy import Spider -> Spider
    name = "worldometers" # Define name of Spider

    def start_requests(self):

        #   urls: List of urls are scrapped by Spider. Spider downloads all of urls's data.
        urls = [
            'https://www.worldometers.info/coronavirus/country/indonesia/',
            # 'https://www.worldometers.info/coronavirus/country/philippines/',
        ]
        
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'coronavirus-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        
        total_cases_data = response.xpath("//div//script[@type='text/javascript']")[2].get() # Don't use "" in @atribute=''
        daily_newcases_data = response.xpath("//div//script[@type='text/javascript']")[3].get() 
        daily_newdeaths_data = response.xpath("//div//script[@type='text/javascript']")[6].get()
        new_cases_and_new_recovered_data = response.xpath("//div//script[@type='text/javascript']")[7].get()
        titles_data = response.xpath("//h3").getall()
        
        # f = open('total-cases-data-%s.txt'%page ,'w')
        # f.write(total_cases_data)
        # f.close()

        # f = open('daily-newdeaths-data-%s.txt'%page ,'w')
        # f.write(daily_newdeaths_data)
        # f.close()

        # f = open('new-cases-and-new-recovered-data-%s.txt'%page ,'w')
        # f.write(new_cases_and_new_recovered_data)
        # f.close()

        
        #crimes_rates = {"year":titles_data,"Population":[179323175,182992000,185771000,188483000,191141000],"Total":[3384200,3488000,3752200,4109500,4564600],"Violent":[288460,289390,301510,316970,364220]}
        dataset = pd.DataFrame(data=process_data(total_cases_data).getDate(), columns=['Date'])
        dataset['Country'] = page.title()
        dataset['Total cases'] = process_data(total_cases_data).getNumberData()
        dataset['Daily new deaths'] =  process_data(daily_newdeaths_data).getNumberData()
        dataset['Daily new cases'] = process_data(daily_newcases_data).getNumberData()
        dataset['Daily new recoveries'] = process_data(new_cases_and_new_recovered_data).getNumberData()
        # print(dataset)
        dataset.to_csv('coronavirus.csv',encoding='utf-8', index=False)
