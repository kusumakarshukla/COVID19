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
		df=pd.read_json(response)
		df['type']=df.index
		df.reset_index(drop=True,inplace=True)
		self.log.info('Columns are {0}'.format(str(df.columns)))
		regional=df[df['type']=='summary']['data']
		list1=regional.tolist()[0]
		self.log.info("Returning Summary :{0}".format(str(list1)))
		return list1

	def history(self):
		response = requests.get(self.config['history']['url']).text
		
		df=pd.read_json(response)
		df3=pd.DataFrame(df.data.to_dict())
		df3['type']=df3.index
		df3.columns=df3[df3.type=='day'].iloc[0]
		df3=df3.iloc[1:]
		return df3

	def history_labels_regions(self):
		region_history=self.history()
		states=[]
		for i in range(0,region_history.shape[1]-1):
			states.extend(pd.DataFrame(region_history.iloc[1][i])['loc'].to_list())
		states=sorted(list(set(states)))
		dictionary=[]	
		for state in states:
			dictionary.append({'label':state,'value':state})
		return dictionary


ob=CovidCases()
ob.history_labels_regions()




		
