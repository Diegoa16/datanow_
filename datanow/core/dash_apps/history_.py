from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, date
import statistics as st
from django_plotly_dash import DjangoDash
#import dash_leaflet as dl

## reading weather station ID dataset
data = pd.read_csv("core/dash_apps/estaciones_mtgnet.csv", sep=';')

app = DjangoDash('history_', external_stylesheets=[dbc.themes.BOOTSTRAP])


card_content_dropdwn = [
    dbc.CardBody(
        [
            html.H6('Seleccione la estación', style = {'textAlign':'center'}),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(id= 'station-dropdown',
                                 options = [{'label':i,'value':i} for i in data['NOMBRE'].unique()],
                                 value = '',
                                 placeholder = 'Selecione la estación a consultar',
                                 ),
                    
                    ], style = {'width':'40%'}), 
                
                
                ])
            
            ]

    )
]

card_content_date = [
    dbc.CardBody(
        [
            html.H6('Seleccione la fecha', style = {'textAlign':'center'}),
            dbc.Row([
                
                dbc.Col([                    
                    dcc.DatePickerRange(id='date_pick_range',
                        start_date = date.today().strftime('%Y-%m-%d'),
                        #end_date_placeholder_text = 'Select a date'
                        min_date_allowed = datetime(2020,1,1),
                        #max_date_allowed = datetime(2025,,19),
                        end_date = date.today().strftime('%Y-%m-%d')
                        ),             
                
                
                    ], style = {'width':'40%'})
                
                
                ])
            
            ]

    )
]
        

body_app = dbc.Container([
    
    
    #html.Br(),
    html.Br(),
    
    
    dbc.Row(html.H4(f'Datos Históricos (Seleccione por periodos de 15 días)'), style={'color':'#4e73df', 'text-align':'center'}),
    
    html.Hr(),
    dbc.Row([
    
        dbc.Col([dbc.Card(card_content_dropdwn, style={'height':'100px','text-align':'center'})]),
        dbc.Col([dbc.Card(card_content_date, style={'height':'100px','text-align':'center'})])

        ]),
    
    html.Br(),
    
    dbc.Row([
            #dbc.Col([dbc.Card(id = 'card_num12', style={'height':'500px'})]),
            dbc.Col(dcc.Loading(children=[dbc.Card(id = 'card_num12', style={'height':'500px'})], fullscreen=True)),
                  
        ]),
    
    html.Br(),
    html.Br(),
    
    dbc.Row([
            dbc.Col([dbc.Card(id = 'card_num13', style={'height':'500px'})]),
                  
        ]),
    
    html.Br(),
    html.Br(),
    
    dbc.Row([
            dbc.Col([dbc.Card(id = 'card_num14', style={'height':'500px'})]),
                  
        ]),
    
    html.Br(),
    html.Br(),
    
    dbc.Row([
            dbc.Col([dbc.Card(id = 'card_num15', style={'height':'500px'})]),
                  
        ]),
    
    html.Br(),
    html.Br(),
    
    dbc.Row([
            dbc.Col([dbc.Card(id = 'card_num16', style={'height':'500px'})]),
                  
        ]),
    
    html.Br(),
    html.Br(),
    
    dbc.Row([
            dbc.Col([dbc.Card(id = 'card_num17', style={'height':'500px'})]),
                  
        ]),
    
    html.Br(),
    html.Br(),
    
    dbc.Row([
            dbc.Col([dbc.Card(id = 'card_num18', style={'height':'500px'})]),
                  
        ]),
    
    html.Br(),
    html.Br(),
    
    
    ],
    style = {'backgroundColor':'#ffffff'})

app.layout = html.Div([body_app])

@app.callback([
               Output('card_num12','children'),
               Output('card_num13','children'),
               Output('card_num14','children'),
               Output('card_num15','children'),
               Output('card_num16','children'),
               Output('card_num17','children'),
               Output('card_num18','children')],
              [Input('station-dropdown','value'),
               Input('date_pick_range', 'start_date'),
               Input('date_pick_range', 'end_date')])

def update_cards(value, start_date, end_date):
    
    station = data[data['NOMBRE']==value].reset_index()['ID'][0]
    url = 'https://api.meteoagronet.com/api/v1/MonuDRQQVoWsCrDKnFSruyGvCToEHU/weatherstation/lastdata?idstation='+ f'{station}'
    response = requests.request("GET", url)
    df_ws=pd.DataFrame(response.json()['last_data'], index=[0])
    date_s = df_ws['report_date_locale'][0]
    dt_p = pd.to_datetime(date_s, format='%Y-%m-%dT%H:%M')
        
    # Máximos y mínimos día del último envío
    dt_xn = dt_p.strftime('%Y-%m-%d')
    url2 = f'https://api.meteoagronet.com/api/v1/MonuDRQQVoWsCrDKnFSruyGvCToEHU/weatherstation/rangedata?idstation='+ f'{station}' + f'&date_end={dt_xn}&date_start={dt_xn}'
    response2 = requests.request("GET", url2)
    df_ws_xn = pd.DataFrame(response2.json()['data_range'])
    df_ws_xn['time'] = df_ws_xn['report_date_locale'].str.slice(12, 16)
    temp_min = float(min(df_ws_xn['temp_c']))
    temp_max = float(max(df_ws_xn['temp_c']))
    pres_min = float(min(df_ws_xn['pressure_rel_hpa']))
    pres_max = float(max(df_ws_xn['pressure_rel_hpa']))
        
    # Máximos y mínimos históricos
    url3 = f'https://api.meteoagronet.com/api/v1/MonuDRQQVoWsCrDKnFSruyGvCToEHU/weatherstation/rangedata?idstation='+ f'{station}' + f'&date_end={end_date}&date_start={start_date}'
    response3 = requests.request("GET", url3)
    df_wsh = pd.DataFrame(response3.json()['data_range'])
    df_wsh['DayOfMonth'] = pd.to_datetime(df_wsh['report_date_locale'], format='%Y-%m-%d %H:%M')
    df_wsh['DayOfMonth'] = df_wsh['DayOfMonth'].dt.strftime('%Y-%m-%d %H:%M')
    # max-min temperatura
    temp_min = float(min(df_wsh['temp_c']))
    tn_time = df_wsh.loc[df_wsh['temp_c'].idxmin()]['DayOfMonth']
    temp_max = float(max(df_wsh['temp_c']))
    tx_time = df_wsh.loc[df_wsh['temp_c'].idxmax()]['DayOfMonth']
    # max-min humedad relativa
    hum_min = float(min(df_wsh['relative_humidity']))
    hrn_time = df_wsh.loc[df_wsh['relative_humidity'].idxmin()]['DayOfMonth']
    hum_max = float(max(df_wsh['relative_humidity']))
    hrx_time = df_wsh.loc[df_wsh['relative_humidity'].idxmax()]['DayOfMonth']
    # max-min presión
    pres_min = float(min(df_wsh['pressure_rel_hpa']))
    pn_time = df_wsh.loc[df_wsh['pressure_rel_hpa'].idxmin()]['DayOfMonth']
    pres_max = float(max(df_wsh['pressure_rel_hpa']))
    px_time = df_wsh.loc[df_wsh['pressure_rel_hpa'].idxmax()]['DayOfMonth']
    # max vel viento
    vv_max = float(max(df_wsh['wind_speed_kmh']))
    vvx_time = df_wsh.loc[df_wsh['wind_speed_kmh'].idxmax()]['DayOfMonth']
    # max solar
    sr_max = float(max(df_wsh['solar_rad_wm2']))
    srx_time = df_wsh.loc[df_wsh['solar_rad_wm2'].idxmax()]['DayOfMonth']
    
        
    fig = go.Figure(data = [go.Scatter(x=df_wsh['DayOfMonth'], y = df_wsh['temp_c'],
                                       line=dict(color='firebrick', width=2),
                                       text=df_wsh['temp_c'], 
                                       name='Temperatura del aire',
                                       )
                            ])
    
    fig.add_annotation(dict(font=dict(color='#4e73df',size=12),
                                        x=tn_time,
                                        y=temp_min,
                                        showarrow=True,
                                        text='min temp = ' + str(temp_min) + '  ',
                                        textangle=0,
                                        xanchor='right',
                                        xref="x",
                                        yref="y"))
    
    fig.add_annotation(dict(font=dict(color='orange',size=12),
                                        x=tx_time,
                                        y=temp_max,
                                        showarrow=True,
                                        text='max temp = ' + str(temp_max) + '  ',
                                        textangle=0,
                                        xanchor='right',
                                        xref="x",
                                        yref="y"))
    
    fig.update_layout(title='Temperatura del Aire',
                      xaxis_title = 'día/hora',
                      yaxis_title = '°C',
                      plot_bgcolor = 'white',
                      margin=dict(l = 40, r = 5, t = 60, b = 40)
                      )
    
    fig1 = go.Figure(data = [go.Scatter(x=df_wsh['DayOfMonth'], y = df_wsh['relative_humidity'],
                                       line=dict(color='#4e73df', width=2),
                                       text=df_wsh['relative_humidity'], 
                                       name='Humedad del aire',
                                       )
                            ])
    
    fig1.add_annotation(dict(font=dict(color='red',size=12),
                                        x=hrn_time,
                                        y=hum_min,
                                        showarrow=True,
                                        text='min hum = ' + str(hum_min) + '  ',
                                        textangle=0,
                                        xanchor='left',
                                        xref="x",
                                        yref="y"))
    
    fig1.add_annotation(dict(font=dict(color='lightblue',size=12),
                                        x=hrx_time,
                                        y=hum_max,
                                        showarrow=True,
                                        text='max hum = ' + str(hum_max) + '  ',
                                        textangle=0,
                                        xanchor='right',
                                        xref="x",
                                        yref="y"))
    
    fig1.update_layout(title='Humedad del Aire',
                      xaxis_title = 'día/hora',
                      yaxis_title = '%',
                      plot_bgcolor = 'white',
                      margin=dict(l = 40, r = 5, t = 60, b = 40)
                      )
    
    fig2 = go.Figure([go.Bar(x=df_wsh['DayOfMonth'], 
                             y = df_wsh['precip_today_mm'], 
                             marker_color = 'blue', 
                             name = 'Precipitación')
                     ])
    fig2.update_layout(title='Precipitación',
                      xaxis_title = 'día/hora',
                      yaxis_title = 'mm',
                      plot_bgcolor = 'white',
                      margin=dict(l = 40, r = 5, t = 60, b = 40),
                      barmode = 'group',
                      yaxis = dict(range=[0,150],
                                  tickmode = 'linear',
                                  tick0 = 0,
                                  dtick = 25)
                      )
    
    fig3 = go.Figure(data = [go.Scatter(x=df_wsh['DayOfMonth'], y = df_wsh['pressure_rel_hpa'],
                                       line=dict(color='black', width=2),
                                       text=df_wsh['pressure_rel_hpa'], 
                                       name='Presión del aire',
                                       )
                            ])
    
    fig3.add_annotation(dict(font=dict(color='#4e73df',size=12),
                                        x=pn_time,
                                        y=pres_min,
                                        showarrow=True,
                                        text='min pres = ' + str(pres_min) + '  ',
                                        textangle=0,
                                        xanchor='right',
                                        xref="x",
                                        yref="y"))
    
    fig3.add_annotation(dict(font=dict(color='orange',size=12),
                                        x=px_time,
                                        y=pres_max,
                                        showarrow=True,
                                        text='max pres = ' + str(pres_max) + '  ',
                                        textangle=0,
                                        xanchor='right',
                                        xref="x",
                                        yref="y"))
    
    fig3.update_layout(title='Presión del Aire',
                      xaxis_title = 'día/hora',
                      yaxis_title = 'hpa',
                      plot_bgcolor = 'white',
                      margin=dict(l = 40, r = 5, t = 60, b = 40)
                      )
    
    fig4 = go.Figure(data = [go.Scatter(x=df_wsh['DayOfMonth'], y = df_wsh['wind_degrees'],
                                       text=df_wsh['wind_dir'],
                                       marker_color='orange',
                                       mode='markers',
                                       name='Dirección del viento',
                                       )
                            ])
    
    fig4.update_layout(title='Dirección del viento',
                      xaxis_title = 'día/hora',
                      yaxis_title = '°',
                      plot_bgcolor = 'white',
                      margin=dict(l = 40, r = 5, t = 60, b = 40),
                      yaxis = dict(range=[0,360],
                                  tickmode = 'linear',
                                  tick0 = 0,
                                  dtick = 90)
                      )
    
    fig5 = go.Figure(data = [go.Scatter(x=df_wsh['DayOfMonth'], y = df_wsh['wind_speed_kmh'],
                                       marker_color='green',
                                       mode='markers',
                                       text=df_wsh['wind_speed_kmh'], 
                                       name='Velocidad del viento',
                                       )
                            ])
    
    fig5.add_annotation(dict(font=dict(color='#4e73df',size=12),
                                        x=vvx_time,
                                        y=vv_max,
                                        showarrow=True,
                                        text='max vel = ' + str(vv_max) + '  ',
                                        textangle=0,
                                        xanchor='right',
                                        xref="x",
                                        yref="y"))
    
    fig5.update_layout(title='Velocidad del viento',
                      xaxis_title = 'día/hora',
                      yaxis_title = 'kmh',
                      plot_bgcolor = 'white',
                      margin=dict(l = 40, r = 5, t = 60, b = 40)
                      )
    
    fig6 = go.Figure(data = [go.Scatter(x=df_wsh['DayOfMonth'], y = df_wsh['solar_rad_wm2'],
                                       line=dict(color='yellow', width=2),
                                       text=df_wsh['solar_rad_wm2'], 
                                       name='Radiación Solar',
                                       )
                            ])
    
    fig6.add_annotation(dict(font=dict(color='red',size=12),
                                        x=srx_time,
                                        y=sr_max,
                                        showarrow=True,
                                        text='max SRad = ' + str(sr_max) + '  ',
                                        textangle=0,
                                        xanchor='right',
                                        xref="x",
                                        yref="y"))
    
    fig6.update_layout(title='Radiación Solar',
                      xaxis_title = 'día/hora',
                      yaxis_title = 'wm2',
                      plot_bgcolor = 'white',
                      margin=dict(l = 40, r = 5, t = 60, b = 40)
                      )


    
    card_content11 = [
        
        dbc.CardBody([dcc.Graph(figure=fig)], style={"width": "100%"}),
        
        ]  
    
    card_content12 = [
        
        dbc.CardBody([dcc.Graph(figure=fig1)], style={"width": "100%"}),
        
        ]  
    
    card_content13 = [
        
        dbc.CardBody([dcc.Graph(figure=fig2)], style={"width": "100%"}),
        
        ]  
    
    card_content14 = [
        
        dbc.CardBody([dcc.Graph(figure=fig3)], style={"width": "100%"}),
        
        ]  
    
    card_content15 = [
        
        dbc.CardBody([dcc.Graph(figure=fig4)], style={"width": "100%"}),
        
        ]  
    
    card_content16 = [
        
        dbc.CardBody([dcc.Graph(figure=fig5)], style={"width": "100%"}),
        
        ]  
    
    card_content17 = [
        
        dbc.CardBody([dcc.Graph(figure=fig6)], style={"width": "100%"}),
        
        ]  
    
    return card_content11, \
           card_content12, card_content13, card_content14, card_content15, card_content16, card_content17
           
    
#if __name__ == "__main__":
#    app.run_server()