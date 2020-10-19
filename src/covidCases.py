import requests
import configparser
from logger import Logger
import pandas as pd
import dash_table
import json
class CovidCases:
	def __init__(self):
		self.config=configparser.ConfigParser()
		self.config.read('conf/config.ini')
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
		states2=json.dumps(states)
		with open("states.dat","w") as f:
			f.write(states2)
		

		dictionary=[]	
		for state in states:
			dictionary.append({'label':state,'value':state})
		dictionary.append({'label':'All','value':'All'})
		return dictionary
	def history_labels_dates(self):
		region_history=self.history()
		dates=region_history.columns
		dictionary=[]
		for date in dates:
			if date=='day':
				continue
			dictionary.append({'label':date,'value':date})
		
		return dictionary


	def return_history_graph(self):
		region_history=self.history()
		region_history['type']=region_history.index
		dictionary={}
		df1=region_history.transpose()
		for indexs in range(0,len(df1)):
				dd={}
				try:
					for day in df1.regional[indexs]:
						dd[day['loc']]={'Indian':day['confirmedCasesIndian'],'Deaths':day['deaths'],'Discharged':day['discharged'],'Confirmed':day['totalConfirmed']}
				except:
							break 
				dictionary[df1.index[indexs]]=dd	
		return dictionary


	def testing(self):
		res=requests.get('https://api.rootnet.in/covid19-in/stats/testing/history').text
		res=json.loads(res)
		testing=pd.DataFrame(res['data'])
		testing.fillna(0,inplace=True)
		return testing


	def return_history(self,state,date):
		region_history=self.history()
		states=[]
		
		
		if 'All' in state and type(state)!=list:

			states=json.loads(open("states.dat").read())

			state=['All']
		elif 'All' in state and type(state)==list:
			 states=json.loads(open("states.dat").read())


		elif type(state)==str:
			states.append(state)
		else:
			states=state

		df4=pd.DataFrame(region_history.loc['regional'][date])
		df5=df4[df4['loc'].isin(states)]
		df5=df5[['loc', 'confirmedCasesIndian', 'confirmedCasesForeign', 'discharged', 'deaths', 'totalConfirmed']]
		df5['Death_Percent']=round(df5['deaths']*100/df5['deaths'].sum(),2)
		df5.Death_Percent.fillna(0,inplace=True)
		df5.rename(columns={
			'loc':'State',
			'confirmedCasesIndian':'Indian',
			'confirmedCasesForeign':'Foreigner',
			'discharged':'Discharged',
			'deaths':'Deaths',
			'totalConfirmed':'Total Confirmed',
			
			},inplace=True)
		return dash_table.DataTable(
    		id='table',
    		columns=[{"name": i, "id": i} for i in df5.columns],
			sort_action="native",
        	sort_mode="multi",
    		data=df5.to_dict('records'),
			style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Date', 'Region']
    ],
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        },
			{
            'if': {
                'column_id': 'Death_Percent',
                'filter_query': '{Death_Percent} >= 0'
            },
            'backgroundColor': 'green',
			'color':'white'},{
            'if': {
                'column_id': 'Death_Percent',
                'filter_query': '{Death_Percent} > 10'
            },
            'backgroundColor': 'lime',
			'color':'white'},
				{
            'if': {
                'column_id': 'Death_Percent',
                'filter_query': '{Death_Percent} > 30'
            },
            'backgroundColor': 'orange',
			'color':'white'},
			{
            'if': {
                'column_id': 'Death_Percent',
                'filter_query': '{Death_Percent} >= 50'
            },
            'backgroundColor': 'red',
			'color':'white'},
		
			
	],       
    
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    },
	
			
			)










		
