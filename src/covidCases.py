import requests
import configparser
from logger import Logger
import pandas as pd
class CovidCases:
	def __init__(self):
		self.config=configparser.ConfigParser()
		self.config.read('../conf/config.ini')
		self.log=Logger('covid_cases')
		self.log.info("Logger Initialized")

		
	def latest_cases(self):
		response = requests.get(self.config['latest']['url']).text
		self.log.info(response)
		print(response)
		df=pd.read_json(response)
		df['type']=df.index
		df.reset_index(drop=True,inplace=True)
		self.log.info('Columns are {0}'.format(str(df.columns)))
		regional=df[df['type']=='regional']['data']
		list1=regional.tolist()[0]

		return list1
	def summary(self):
		response = requests.get(self.config['latest']['url']).text
		self.log.info(response)
		print(response)
		df=pd.read_json(response)
		df['type']=df.index
		df.reset_index(drop=True,inplace=True)
		self.log.info('Columns are {0}'.format(str(df.columns)))
		regional=df[df['type']=='summary']['data']
		list1=regional.tolist()[0]
		self.log.info("Returning Summary :{0}".format(str(list1)))
		return list1



		
