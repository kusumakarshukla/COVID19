import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from covidCases import CovidCases
import plotly.graph_objects as go
import dash_daq as daq
covid=CovidCases()
regions=covid.latest_cases()
summary=covid.summary()


external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
theme =  {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

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
app.layout = html.Div(id='dark-theme-container',children=[daq.DarkThemeProvider(theme=theme),
    html.H1(children='Latest Covid-19 Cases'),

    
    html.Div([
        html.Table([
            html.Tr(
                [html.Td(html.H4('Total')),html.Td(html.H4('Overall Confirmed')),html.Td(html.H4('Overall Discharged')),html.Td(html.H4('Overall Deaths'))]

            ),
            html.Tr(
                [html.Td(daq.LEDDisplay(
        value="3.14159",
        color=theme['primary'],
        id='darktheme-daq-leddisplay',
        className='dark-theme-control'
        
    )),html.Td(html.H4(summary['confirmedCasesIndian'])),html.Td(html.H4(summary['discharged'])),html.Td(html.H4(summary['deaths']))]

            )])
            
          
    ]),

    dcc.Graph(
        id='example-graph',
        figure=fig,
),
html.H1("Record of Cases"),
html.Div(children=[
dcc.Dropdown(
        id='demo-dropdown',
        options=covid.history_labels_regions(),
        value=covid.history_labels_regions()[0]['value']
    )])


])


if __name__ == '__main__':

    app.run_server(debug=True)
