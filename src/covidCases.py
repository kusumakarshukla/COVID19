import requests
import configparser
from logger import Logger
class CovidCases:
	def __init__(self):
		self.config=configparser.ConfigParser()
		self.config.read('config//config.ini')
		self.log=Logger()
		self.log.info("Logger Initialized")

		
	def latest_cases(self):
		response = request.get(config['latest']['url']).text
		self.log.info(response)

		

