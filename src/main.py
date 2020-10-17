import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from covidCases import CovidCases
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
covid=CovidCases()
regions=covid.latest_cases()
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


df = pd.DataFrame({
    "States": [i['loc'] for i in regions],
    "Confirmed Cases (Indian)": [i['confirmedCasesIndian'] for i in regions],
    "Confirmed Cases (Foreign)": [i['confirmedCasesForeign'] for i in regions],
    'Discharged'  :[i['discharged'] for i in regions],
    'Deaths':[i['deaths'] for i in regions],
})

fig = go.Figure(data=[
    go.Bar(name='Confirmed Cases-India', x=df['States'], y=df['Confirmed Cases (Indian)']),
    go.Bar(name='Confirmed Cases-Foreign', x=df['States'], y=df['Confirmed Cases (Foreign)']),
    go.Bar(name='Deaths', x=df['States'], y=df['Deaths']),
    go.Bar(name='Discharged', x=df['States'], y=df['Discharged'])
    
])
app.layout = html.Div(children=[
    html.H1(children='Latest COVID Cases'),

    html.Div(children='''
       
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
