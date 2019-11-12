import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

class LunarCalendar(scrapy.Spider):
    name = "lunar"

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
        table_header = response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//thead//text()').extract()
        row=response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()').extract()
        counter=0
        k=0
        l=0
        for i in response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()').extract():
            counter=counter+1

        for j in range(0,int(counter/10)):
            yield {
                'Year':response.url.split('=')[-1],
                'Lunation':response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()')[l].extract(),
                'New Moon':response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()')[l+1].extract(),
                'First Quarter':response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()')[l+3].extract(),
                'Full Moon':response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()')[l+5].extract(),
                'Third Quarter':response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()')[l+7].extract(),
                'Duration':response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()')[l+9].extract()
            }
            lunar=lunar.append(pd.DataFrame(data=[response.url.split('=')[-1],
                response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()')[l].extract(),
                response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()')[l+1].extract(),
                response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()')[l+3].extract(),
                response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()')[l+5].extract(),
                response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()')[l+7].extract(),
                response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()')[l+9].extract()
                ]).transpose())
            l=l+10
        lunar.columns=['Year','Lunation','New Moon','First Quarter','Full Moon','Third Quarter','Duration']
        lunar=lunar.reset_index(drop=True)
        file_path='C:/Users/dhars/Documents/GL_ML/Capstone/Crime_Rate_Prediction_And_Lunar_Cycle/Code/Web_Scrapping/lunar_'+response.url.split('=')[-1]+'.csv'
        lunar.to_csv(path_or_buf=file_path,index_label=['SL'])