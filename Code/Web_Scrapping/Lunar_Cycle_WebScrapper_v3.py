import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

class LunarCalendar(scrapy.Spider):
	name="lunar"
	lunar=pd.DataFrame()
	city='city'
	country='country'
	start_yr=1900
	end_yr=1900
	base_url='https://www.timeanddate.com/moon/phases/'
	delim1='/'
	delim2='?year='
	urls=[]

	def start_requests(self):
		print ("This program will scrap the web page www.timeanddate.com for lunar cycle data based on the given city, country and year")
		print ("City: ")
		self.city=input().lower()
		print("Country: ")
		self.country=input().lower()
		print ("Starting Year: ")
		self.start_yr=int(input())
		print ("Ending Year: ")
		self.end_yr=int(input())

		self.urls.append(self.base_url + self.country + self.delim1 + self.city + self.delim2 + str(self.start_yr-1))

		for i in range(0,(self.end_yr+1-self.start_yr)):
			self.urls.append(self.base_url + self.country + self.delim1 + self.city + self.delim2 + str(self.start_yr+i))
		for url in self.urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		counter = 0
		k=0
		country=response.url.split('/')[-2]
		city=response.url.split('/')[-1].split('?')[0]
		lunar = pd.DataFrame()
		for i in response.xpath('//*[@class="tb-sm zebra fw tb-hover"]//tbody//tr//text()').extract():
			counter=counter+1
		
		#print(response.url.split('=')[-1],":",counter)
		
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

		lunar.columns=['Year','Lunation','New_Moon','First_Quarter','Full_Moon','Third_Quarter','Duration']
		lunar=lunar.reset_index(drop=True)

		self.lunar=self.lunar.append(lunar,sort=True)
		self.lunar=self.lunar.sort_values(by=['Lunation','Year'])
		self.lunar=self.lunar.reset_index(drop=True)
		self.lunar=self.lunar.loc[:,['Year','Lunation','Full_Moon']]
		file_path='C:/Users/dhars/Documents/GL_ML/Capstone/Crime_Rate_Prediction_And_Lunar_Cycle/Code/Web_Scrapping/Lunar_Cycle_'+str(self.start_yr)+'_'+str(self.end_yr)+'.csv'
		self.lunar.to_csv(path_or_buf=file_path,index_label=['SL'])