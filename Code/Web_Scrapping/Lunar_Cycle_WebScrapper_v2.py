import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

class LunarCalendar(scrapy.Spider):
    name = "lunar"
    lunar = pd.DataFrame()

    def start_requests(self):
        urls = [
            'https://www.timeanddate.com/moon/phases/usa/atlanta?year=2009',
            'https://www.timeanddate.com/moon/phases/usa/atlanta?year=2010',
            'https://www.timeanddate.com/moon/phases/usa/atlanta?year=2011',
            'https://www.timeanddate.com/moon/phases/usa/atlanta?year=2012',
            'https://www.timeanddate.com/moon/phases/usa/atlanta?year=2013',
            'https://www.timeanddate.com/moon/phases/usa/atlanta?year=2014',
            'https://www.timeanddate.com/moon/phases/usa/atlanta?year=2015',
            'https://www.timeanddate.com/moon/phases/usa/atlanta?year=2016',
            'https://www.timeanddate.com/moon/phases/usa/atlanta?year=2017',
            'https://www.timeanddate.com/moon/phases/usa/atlanta?year=2018',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        lunar = pd.DataFrame()
        counter = 0
        k=0
        country=response.url.split('/')[-2]
        city=response.url.split('/')[-1].split('?')[0]

        for i in response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()').extract():
            counter=counter+1

        for j in range(0,int(counter/10)):
            lunar=lunar.append(pd.DataFrame(data=[response.url.split('=')[-1],
                response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()')[k].extract(),
                response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()')[k+1].extract(),
                response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()')[k+3].extract(),
                response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()')[k+5].extract(),
                response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()')[k+7].extract(),
                response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()')[k+9].extract()
                ]).transpose(),sort=True)
            k=k+10
        lunar.columns=['Year','Lunation','New Moon','First Quarter','Full Moon','Third Quarter','Duration']
        lunar=lunar.reset_index(drop=True)
        self.lunar=self.lunar.append(lunar,sort=True)
        self.lunar=self.lunar.sort_values(by=['Lunation'])
        self.lunar=self.lunar.reset_index(drop=True)
        self.lunar=self.lunar.loc[:,['Year','Lunation','Full Moon']]
        file_path='C:/Users/dhars/Documents/GL_ML/Capstone/Crime_Rate_Prediction_And_Lunar_Cycle/Code/Web_Scrapping/Lunar_Cycle_2009_2018.csv'
        self.lunar.to_csv(path_or_buf=file_path,index_label=['SL'])