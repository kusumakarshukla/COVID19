import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from covidCases import CovidCases
import plotly.graph_objects as go
import dash_daq as daq
from dash.dependencies import Input, Output
import json
external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

@app.callback(
    Output(component_id='history_table', component_property='children'),
    [Input(component_id='region_option', component_property='value'),
    Input(component_id='date_option', component_property='value')
    ]
)
def update_output_div(state,date):
    ob=CovidCases()
    return ob.return_history(state,date)

@app.callback(
    Output(component_id='cases_graph', component_property='figure'),
    [Input(component_id='history_graph', component_property='value'),
    Input(component_id='region_graph', component_property='value'),
    ])

def update_case_graph(case,region):
    obj=CovidCases()
    dictionary=obj.return_history_graph()
    regions=[]
    fig = go.Figure(layout= go.Layout(
            
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            paper_bgcolor = '#000000',
			font= {
                    'color': 'white'
                },
            plot_bgcolor = '#000000',
            transition= {
                'duration': 100,
              
            },
            hovermode='closest',
            xaxis=dict(
        autorange=True,
        showgrid= False,
        ticks='',
        showticklabels=True
            ),
        yaxis=dict(
            showgrid=False,
            showticklabels=True
        )
            )
 
 
      )
    if 'All' in region and type(region)==str:
            regions=json.loads(open("states.dat").read())
    elif 'All' in region and type(region)==list:
            regions=json.loads(open("states.dat").read())
    elif type(region)==str:
        regions.append(region)
    else:
        regions=region



    x=[date for date in dictionary.keys()]
    print(regions)
    print("region is ",region)
    for region in regions:
        try:
            y=[]
            for death in dictionary.values():
                try:
                    if region in death:
                        y.append(death[region][case])
                    else:
                        y.append(0)
                except Exception as e:
                    pass
            print(len(x),len(y))
            fig.add_trace(go.Scatter(x=x, y=y,
                    mode='lines',
                    name=region))
            fig.update_traces(marker=dict(size=1,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  )
            
        except Exception as e:
            pass
            continue
    return fig
    
def tab1_data():
    theme =  {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
        }
    covid=CovidCases()
    regions=covid.latest_cases()
    summary=covid.summary()

    
    
    
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
        go.Bar(name='Discharged', x=df['States'], y=df['Discharged'])],layout= go.Layout(
            
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            paper_bgcolor = '#000000',
			font= {
                    'color': 'white'
                },
            plot_bgcolor = '#000000',
            transition= {
                'duration': 100,
              
            },
            hovermode='closest',
            xaxis=dict(
        autorange=True,
        showgrid= False,
        ticks='',
        showticklabels=True
            ),
        yaxis=dict(
            showgrid=False,
            showticklabels=True
        )
            )
 
 
      )
        
    
    return html.Div(id='dark-theme-container',children=[daq.DarkThemeProvider(theme=theme),
        html.H1(children='Latest Covid-19 Cases'),

        
        html.Div([
            html.Table([
                html.Tr(
                    [html.Td(html.H4('Total')),html.Td(html.H4('Overall Confirmed')),html.Td(html.H4('Overall Discharged')),html.Td(html.H4('Overall Deaths'))]

                ),
                html.Tr(
                    [html.Td(daq.LEDDisplay(
            value=summary['total'],
             color="#00ff00",
			backgroundColor="#23262e",
            id='darktheme-daq-leddisplay',
            className='dark-theme-control'
            
        )),html.Td(daq.LEDDisplay(
            value=summary['confirmedCasesIndian'],
             color="#00ff00",
			backgroundColor="#23262e",
            id='darktheme-daq-leddisplay',
            className='dark-theme-control'
            
        )),html.Td(daq.LEDDisplay(
            value=summary['discharged'],
             color="#00ff00",
			backgroundColor="#23262e",
            id='darktheme-daq-leddisplay',
            className='dark-theme-control'
            
        )),html.Td(html.Td(daq.LEDDisplay(
            value=summary['deaths'],
             color="#00ff00",
			backgroundColor="#23262e",
            id='darktheme-daq-leddisplay',
            className='dark-theme-control'
            
        )))]

                )])
                
            
        ]),

        dcc.Graph(
            id='example-graph',
            figure=fig,
    ),
    html.H1("Record of Cases"),
    html.Div(children=[
        html.Table(html.Tr([
            html.Td([html.H3("States"),
    dcc.Dropdown(
            id='region_option',
            options=covid.history_labels_regions(),
            value='All',
            multi=True
        )]),html.Td([html.H3("Date"),
    dcc.Dropdown(
            id='date_option',
            options=covid.history_labels_dates(),
            value=covid.history_labels_dates()[0]['value'],
            
        )]

        
        )]))


    ]),
    html.Div(children=[html.Div(id="history_table")]),
    html.Div(children=[html.H1("Trends Year Till Date"),html.Div(children=[
        html.Div(
        dcc.Dropdown(id="history_graph",
                        options=[{'label':'Deaths','value':'Deaths'},
                                {'label':'Confirmed','value':'Confirmed'},
                                {'label':'Discharged','value':'Discharged'}],
                        value='Deaths'
                                ),style={"width":"20%","display":"inline-block"})
        ,
        html.Div(
        dcc.Dropdown(id="region_graph",
                        options=covid.history_labels_regions(),
                        value='All',
                        multi=True
                                ),style={"width":"20%","display":"inline-block"}),
        
        dcc.Graph(id="cases_graph")],style={'width':'100%'})])

    ])


@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div(tab1_data())
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])


    
app.layout =html.Div([
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Tab one', value='tab-1'),
        dcc.Tab(label='Tab two', value='tab-2'),
    ]),
    html.Div(id='tabs-example-content')])
    app.config['suppress_callback_exceptions'] = True
    app.config.suppress_callback_exceptions = True
    return app



