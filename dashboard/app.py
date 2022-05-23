
from dash import Dash, html, dcc, Output, Input, State
import plotly
import plotly.express as px
import plotly.graph_objs as go
from collections import deque
import datetime
import sqlite3
import random
from datetime import datetime, timedelta
import pandas as pd


#--------Database query for historic wind data--->
try:
    conn = sqlite3.connect('weather.db')
            
except sqlite3.OperationalError as e:
            raise e
else:
    print('Connected!')
    curr = conn.cursor()
    curr.execute("SELECT * FROM wind_table")
    conn.commit()
    results = curr.fetchall()
   
    results  = results[:47]
#-------------------------------------------------^
#-------Query for current weather
curr.execute('SELECT * FROM current_temperature')
conn.commit()
current_weather = curr.fetchall()
current_weather = current_weather[:5]
#------Global Colors------------------------------->
curr.execute('SELECT * FROM forecast')
conn.commit()
forecast = curr.fetchall()


#-------------------------
colors = {
    'background': '#111111',
    'text': '#7FDBFF'}

app = Dash(__name__)
app.layout =  html.Div(children= [html.Div ( className = 'Parent', children=[
                                html.Div(className='left-child', children = [
                                                    dcc.Graph(id='live-graph', animate=True),
                                                    dcc.Interval(id='graph-update',interval=1000),
                                                    ]
                                        ),
                                html.Div(style={'padding': 10, 'width': 900}, className='right-child', children=[
                                                dcc.Graph(id="wind-histogram"),
                                                dcc.Store(id='histogramdata', data=results)
                                ])
                                ]),
                            html.Div(className='Bottom-Parent', children=[
                                html.Div(className='bottom-left', children=[
                                                    dcc.Graph(id='current-temp', style={'display':'inline-block', 'width': 900}),
                                                    dcc.Interval(id='temp-update', interval=30000),
                                                    dcc.Store(id='temp-data', data=current_weather),
                                                    dcc.Graph(id='current-status', style={'display':'inline-block', 'border-left': 2}),
                                                    dcc.Store(id = 'forecastdata', data = forecast)
                                ]),
                                

                                ]),
                        
                ])
#-----------------------------------------------------------------------------------------^
#----Variables for Scatter
X = deque(maxlen=20)
X.append(results[0][0])
Y = deque(maxlen=20)
Y.append(results[0][1])
@app.callback(Output(component_id ='live-graph', component_property='figure'),
            Input(component_id='graph-update', component_property='n_intervals'),
        )
def update_graph_scatter(n):
    if len(results) > 0:
        dt = results[0][0]
        wind = results[0][1]
        X.append(dt)
        Y.append(wind)
        results.pop(0)
    
    else:
        dt = datetime.strptime(X[-1], "%Y-%m-%d %H:%M:%S")
        dt = dt + timedelta(hours=1)
        dt = datetime.strftime(dt, "%Y-%m-%d %H:%M:%S")
        X.append(dt)
        Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))
    
    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers',
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),
                                                title='Mavericks Beach Offshore Wind Speed ',
                                                plot_bgcolor=colors['background'],
                                                paper_bgcolor=colors['background'],
                                                font_color=colors['text']

                                                ),
                                                }
#-----------------------------------------------------------------------------------^
@app.callback(
    Output("wind-histogram", "figure"), 
    Input('histogramdata', 'data')
    )
def update_wind_histogram( results):
    df = pd.DataFrame(results, columns =['Date', 'Wind'])
    df = pd.concat([df]*41, ignore_index=True)
    df = df['Wind'] # replace with your own data source
    fig = px.histogram(df, range_x=[0, 10])
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        title_text='Distribution of Wind', title_x=0.5,
        xaxis=dict(
            title="Wind Speed"),
        
        )
    return fig
#------------------------------------------------------------------^
@app.callback(Output(component_id ='current-temp', component_property='figure'),
            Input(component_id='temp-data', component_property='data'),
        )
def update_current_temp(data):
    df = pd.DataFrame(data, columns =['Date', 'Status', 'Temp'])
    fig = px.bar(df, x="Date", y="Temp", color="Temp")

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'])

    return fig

@app.callback(Output(component_id ='current-status', component_property='figure'),
            Input(component_id='forecastdata', component_property='data'),
        )
def update_status_graph(data):
    df = pd.DataFrame(data, columns =['Date', 'Status', 'Temp'])# replace with your own data source
    
    values = df['Status'].value_counts(normalize=True).values
    names = df['Status'].value_counts(normalize=True).index
    
    fig = px.pie(df, values=values, names=names, hole=.7)
    
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'])
    
    return fig
    

if __name__ == '__main__':
    app.run_server(debug=True)