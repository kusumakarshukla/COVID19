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
    Output(component_id='toggle-switch-output', component_property='children'),
    [Input(component_id='my-toggle-switch', component_property='on')])
def alter_toggle(rural):
    ob=CovidCases()
    tests=ob.facilities()
    child=[]
    if rural==True:
        tests.sort_values('ruralHospitals',inplace=True)
        x=tests.state[:20]
        y=tests.ruralHospitals[:20]
        print(x)
        print(y)
        fig = go.Figure(data=[
        go.Bar(name='Top 20 Hospital Counts', x=x, y=y)]
        ,layout= go.Layout(
            
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
        child.append(html.H3("Top 20 States with highest Bed counts in Rural Areas"))
        child.append(dcc.Graph(figure=fig))
        tests.sort_values('ruralBeds',inplace=True)
        
        x=tests.state[:20]
        y=tests.ruralBeds[:20]
        print(x)
        print(y)
        fig = go.Figure(data=[
        go.Bar(name='Top 20 Bed Counts', x=x, y=y)]
        ,layout= go.Layout(
            
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
        child.append(html.H3("Top 20 States with highest  Bed counts in Rural Areas"))
        child.append(dcc.Graph(figure=fig))
    else:
        tests.sort_values('urbanHospitals',inplace=True)
        x=tests.state[:20]
        y=tests.urbanHospitals[:20]
        fig = go.Figure(data=[
        go.Bar(name='Top 20 Urban Hospitals', x=x, y=y)]
        ,layout= go.Layout(
            
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
        child.append(html.H3("Top 20 States with highest Hospital Counts in Urban Areas"))
        child.append(dcc.Graph(figure=fig))
        tests.sort_values('urbanBeds',inplace=True)
        x=tests.state[:20]
        y=tests.urbanBeds[:20]
        fig = go.Figure(data=[
        go.Bar(name='Top 20 States with highest  Bed counts in Urban Areas', x=x, y=y)]
        ,layout= go.Layout(
            
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
        child.append(html.H3("Top 20 States with highest  Bed counts in Urban Areas"))
        child.append(dcc.Graph(figure=fig))

    return child

        











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

def tab2_data():
    print(" In tab2 function")
    ob=CovidCases()
    test_data=ob.testing()
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
    x=test_data.day.to_list()
    
    y1=test_data.totalSamplesTested.to_list()
    y2=test_data.totalIndividualsTested.to_list()
    y3=test_data.totalPositiveCases.to_list()
    fig.add_trace(go.Scatter(x=x, y=y1,
                    mode='lines',
                    name='Total Samples Tested'))
    fig.add_trace(go.Scatter(x=x, y=y2,
                    mode='lines',
                    name='Total Individuals Tested'))
    fig.add_trace(go.Scatter(x=x, y=y3,
                    mode='lines',
                    name='Total Positive Cases'))
    fig.update_traces(marker=dict(size=1,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  )
            
        
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
            
            margin={'l': 40, 'b': 70, 't': 10, 'r': 10},
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
                tickangle = 90,
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
    fig.update_xaxes(
        tickangle = 30,
        title_text = "States",
        title_font = {"size": 20},
        title_standoff = 25)
        
    
    return html.Div(id='dark-theme-container',children=[daq.DarkThemeProvider(theme=theme),
        html.H3(children='Latest Covid-19 Cases'),

        
        html.Div([
            html.Table([
                html.Tr(
                    [html.Td(html.H3('Total')),html.Td(html.H3('Overall Confirmed')),html.Td(html.H3('Overall Discharged')),html.Td(html.H3('Overall Deaths'))]

                ),
                html.Tr(
                    [html.Td(daq.LEDDisplay(
            value=summary['total'],
             color="#00ff00",
			backgroundColor="#23262e",
            id='darktheme-daq-leddisplay',
            className='dark-theme-control',
            size=40
            
        )),html.Td(daq.LEDDisplay(
            value=summary['confirmedCasesIndian'],
             color="#00ff00",
			backgroundColor="#23262e",
            id='darktheme-daq-leddisplay',
            className='dark-theme-control',
            size=40
            
        )),html.Td(daq.LEDDisplay(
            value=summary['discharged'],
             color="#00ff00",
			backgroundColor="#23262e",
            id='darktheme-daq-leddisplay',
            className='dark-theme-control',
            size=40
            
        )),html.Td(html.Td(daq.LEDDisplay(
            value=summary['deaths'],
             color="#00ff00",
			backgroundColor="#23262e",
            id='darktheme-daq-leddisplay',
            className='dark-theme-control',
            size=40
            
        )))]

                )])
                
            
        ]),
        html.H3("Latest  COVID-19 Cases across Indian States"),
        dcc.Graph(
            id='example-graph',
            figure=fig,
    ),
    html.H3("Record of Cases"),
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
    html.Div(children=[html.H3("Trends Year Till Date"),html.Div(children=[
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
theme =  {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div(tab1_data())
    elif tab == 'tab-2':
        print("ptessed tab2")
        return html.Div([dcc.Graph(figure=
             tab2_data())])
    elif tab=='tab-3':
        return html.Div(children=[
            html.Br(),
        daq.DarkThemeProvider(theme=theme, children=[
            html.Div([
                daq.BooleanSwitch(
                id='my-toggle-switch',
                label="Rural or Urban",
               
                on=True ),
                html.Div(id='toggle-switch-output')
                    ])] )])



    
app.layout =html.Div([
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Cases', value='tab-1'),
        dcc.Tab(label='Testing', value='tab-2'),
        dcc.Tab(label='Facilities', value='tab-3')
    ]),
    html.Div(id='tabs-example-content')])
app.config['suppress_callback_exceptions'] = True
app.config.suppress_callback_exceptions = True

if __name__=='__main__':
    app.run_server(debug=True)


