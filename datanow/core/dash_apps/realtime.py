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


## reading weather station ID dataset
data = pd.read_csv("core/dash_apps/estaciones_mtgnet.csv", sep=';')
api_key = ''
app = DjangoDash('realtime', external_stylesheets=[dbc.themes.BOOTSTRAP])

card_content_dropdwn = [
    dbc.CardBody(
        [
            html.H6('Seleccione la estación', style = {'textAlign':'center'}),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    #html.H6('Current Period'),
                    
                    dcc.Dropdown(id= 'station-dropdown',
                                 options = [{'label':i,'value':i} for i in data['NOMBRE'].unique()],
                                 value = '',
                                 placeholder = 'Selecione la estación a consultar',
                                 ),
                    
                    ], style = {'width':'40%'}),               
                
                
                    ])
                
                
                ])
            
            ]
        
body_app = dbc.Container([
    
    
    #html.Br(),
    html.Br(),
    dbc.Row(html.H4(f'Tiempo Real'), style={'color':'#4e73df', 'text-align':'center'}),
    
    #html.Br(),
    
    html.Br(),
    
    dbc.Row([
            dbc.Col([dbc.Card(card_content_dropdwn, style={'height':'200px'})], width = 3),
            dbc.Col(dcc.Loading(children=[dbc.Card(id = 'card_num3', style={'height':'200px'})], fullscreen=False)),
            dbc.Col([dbc.Card(id = 'card_num2', style={'height':'200px'})], width = 3),
        
        ]),
    
    html.Br(),
    html.Br(),
    
    dbc.Row([
            dbc.Col([dbc.Card(id = 'card_num4', style={'height':'150px'})]),
            dbc.Col([dbc.Card(id = 'card_num5', style={'height':'150px'})]),
            dbc.Col([dbc.Card(id = 'card_num6', style={'height':'150px'})]),
            dbc.Col([dbc.Card(id = 'card_num7', style={'height':'150px'})]),
        
        ]),
    
    html.Br(),
    html.Br(),
    
    dbc.Row([
            dbc.Col([dbc.Card(id = 'card_num8', style={'height':'150px'})]),
            dbc.Col([dbc.Card(id = 'card_num9', style={'height':'150px'})]),
            dbc.Col([dbc.Card(id = 'card_num10', style={'height':'150px'})]),
            dbc.Col([dbc.Card(id = 'card_num11', style={'height':'150px'})]),
        
        ]),
    
    html.Br(),
    html.Hr(),
    html.Br(),    
    ],
    style = {'backgroundColor':'#ffffff'})

app.layout = html.Div([body_app])

@app.callback([
               Output('card_num2','children'),
               Output('card_num3','children'),
               Output('card_num4','children'),
               Output('card_num5','children'),
               Output('card_num6','children'),
               Output('card_num7','children'),
               Output('card_num8','children'),
               Output('card_num9','children'),
               Output('card_num10','children'),
               Output('card_num11','children')],
              Input('station-dropdown','value')
               )

def update_cards(value):
    
    station = data[data['NOMBRE']==value].reset_index()['ID'][0]
    nombre = data[data['NOMBRE']==value].reset_index()['NOMBRE'][0]
    lat = data[data['NOMBRE']==value].reset_index()['LAT'][0]
    lon = data[data['NOMBRE']==value].reset_index()['LON'][0]
    url = f'https://api.meteoagronet.com/api/v1/{api_key}/weatherstation/lastdata?idstation='+ f'{station}'
    response = requests.request("GET", url)
    df_ws=pd.DataFrame(response.json()['last_data'], index=[0])
    temp = df_ws['temp_c'][0]
    date_s = df_ws['report_date_locale'][0]
    dt_p = pd.to_datetime(date_s, format='%Y-%m-%dT%H:%M')
    dt_p1 = dt_p.strftime('%Y-%m-%d %H:%M')
    rh = df_ws['relative_humidity'][0]
    pres = df_ws['pressure_rel_hpa'][0]
    dew = df_ws['dewpoint_c'][0]
    prec = df_ws['precip_today_mm'][0]
    wind_d = df_ws['wind_degrees'][0]
    wind_v = df_ws['wind_speed_kmh'][0]
    solar = df_ws['solar_rad_wm2'][0]
    uv = df_ws['uv_index'][0]
    
    # Máximos y mínimos día del último envío
    dt_xn = dt_p.strftime('%Y-%m-%d')
    url2 = f'https://api.meteoagronet.com/api/v1/{api_key}/weatherstation/rangedata?idstation='+ f'{station}' + f'&date_end={dt_xn}&date_start={dt_xn}'
    response2 = requests.request("GET", url2)
    df_ws_xn = pd.DataFrame(response2.json()['data_range'])
    df_ws_xn['time'] = df_ws_xn['report_date_locale'].str.slice(12, 16)
    temp_min = float(min(df_ws_xn['temp_c']))
    time_min_xn = df_ws_xn.loc[df_ws_xn['temp_c'].idxmin()]['time']
    temp_max = float(max(df_ws_xn['temp_c']))
    time_max_xn = df_ws_xn.loc[df_ws_xn['temp_c'].idxmax()]['time']
    rh_min = float(min(df_ws_xn['relative_humidity']))
    rh_max = float(max(df_ws_xn['relative_humidity']))
    pres_min = float(min(df_ws_xn['pressure_rel_hpa']))
    pres_max = float(max(df_ws_xn['pressure_rel_hpa']))
    wind_vmax = float(max(df_ws_xn['wind_speed_kmh']))
    solar_max = float(max(df_ws_xn['solar_rad_wm2']))
    uv_max = float(max(df_ws_xn['uv_index']))
    wind_d_mode = st.mode(df_ws_xn['wind_dir'])
    
    def date_diff (date_s):
        dt1 = date_s
        dt1 = pd.to_datetime(dt1, format='%Y-%m-%dT%H:%M:%S.%f')
        dt1 = dt1.strftime('%Y-%m-%d %H:%M:%S.%f')
        # convert string to datetime
        dt1 = datetime.strptime(dt1, "%Y-%m-%d %H:%M:%S.%f")
        dt2 = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')
        # convert string to datetime
        dt2 = datetime.strptime(dt2, "%Y-%m-%d %H:%M:%S.%f")
        # difference between datetime in timedelta
        delta = dt2 - dt1
        if delta.seconds <= 60:
            diference = 'Hace 1 minuto'
        elif delta.seconds >60 and delta.seconds <3601:
            diference = f'Hace {round(delta.seconds/60)} minutos'
        elif delta.seconds >3600 and delta.seconds <84401:
            diference = f'Hace {round(delta.seconds/3600)} horas'
        else:
            diference = f'Hace {round(delta.seconds/84400)} días'
        
        return diference
    
    def wind_dir(dir):
        if dir > 0 and dir < 11.26:
            wd = 'N'
        elif dir > 11.26 and dir < 33.76:
            wd = 'NNE'
        elif dir > 33.76 and dir < 56.26:
            wd = 'NE'
        elif dir > 56.26 and dir < 78.76:
            wd = 'ENE'
        elif dir > 78.76 and dir < 101.26:
            wd = 'E'
        elif dir > 101.26 and dir < 123.76:
            wd = 'ESE'
        elif dir > 123.76 and dir < 146.26:
            wd = 'SE'
        elif dir > 146.26 and dir < 168.76:
            wd = 'SSE'
        elif dir > 168.76 and dir < 191.26:
            wd = 'S'
        elif dir > 191.26 and dir < 213.76:
            wd = 'SSW'
        elif dir > 213.76 and dir < 236.26:
            wd = 'SW'
        elif dir > 236.26 and dir < 258.76:
            wd = 'WSW'
        elif dir > 258.76 and dir < 281.26:
            wd = 'W'
        elif dir > 281.26 and dir < 303.76:
            wd = 'WNW'
        elif dir > 303.76 and dir < 326.26:
            wd = 'NW'
        elif dir > 326.26 and dir < 348.76:
            wd = 'NNW'
        elif dir > 348.76 and dir < 0:
            wd = 'N'
        return wd
    
    fig = px.scatter_mapbox(data, lat="LAT", lon="LON", hover_name="NOMBRE", hover_data=["ID", "CIUDAD","DEPTO","PAIS"],
                        color_discrete_sequence=["fuchsia"], zoom=10, height=170, center=dict(lat=lat,lon=lon))
    fig.update_traces(marker={'size': 12})
    fig.update_layout(
            mapbox_style="open-street-map",
            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    
    
    card_content1 = [
        
        dbc.CardBody(
            [
                html.H6('ID Estación', style = {"fontWeight":"lighter","textAlign":"center"}),
                html.H3('{0}'.format(station), style = {'color':'#090059','textAlign':'center'}),
                html.H6('Fecha del reporte', style = {"fontWeight":"lighter","textAlign":"center"}),
                html.H4('{0}{1}'.format(dt_p1, ' GMT-5'), style = {'color':'#090059','textAlign':'center'}),
                html.H6('{0}'.format(date_diff(date_s)), style = {'color':'#090059','textAlign':'center'}),
               
                ]
            )
        
        ]
    
    card_content2 = [               
        dbc.CardBody([dcc.Graph(figure=fig)], style={"width": "100%"}),
        ]
    
    card_content3 = [
        
        dbc.CardBody(
            [
                html.H6('Humedad relativa del aire', style = {"fontWeight":"lighter","textAlign":"center"}),
                html.H5('{0}{1}'.format('max: ',rh_max), style = {'color':'#4e73df','textAlign':'center'}),
                html.H3('{0}{1}'.format(rh,' %'), style = {'color':'black','textAlign':'center'}),
                html.H5('{0}{1}'.format('min: ',rh_min), style = {'color':'red','textAlign':'center'}),
                #html.H6('{0}'.format(name), style = {"fontWeight":"lighter","textAlign":"center"}),
                #dcc.Markdown(dangerously_allow_html = True,
                   #children = ["<sub>+{0}{1}{2}</sub>".format("$",diff_1,"M")],style = {'color':'#090059','textAlign':'center'}
                   #)
                ]
            )
        
        ]
    
    card_content4 = [
        
        dbc.CardBody(
            [
                html.H6('Presión del aire', style = {"fontWeight":"lighter","textAlign":"center"}),
                html.H5('{0}{1}'.format('max: ',pres_max), style = {'color':'green','textAlign':'center'}),
                html.H3('{0}{1}'.format(pres,' hpa'), style = {'color':'black','textAlign':'center'}),
                html.H5('{0}{1}'.format('min: ',pres_min), style = {'color':'black','textAlign':'center'}),
                #html.H6('{0}'.format(name), style = {"fontWeight":"lighter","textAlign":"center"}),
                #dcc.Markdown(dangerously_allow_html = True,
                   #children = ["<sub>+{0}{1}{2}</sub>".format("$",diff_1,"M")],style = {'color':'#090059','textAlign':'center'}
                   #)
                ]
            )
        
        ]
    
    card_content5 = [
        
        dbc.CardBody(
            [
                html.H6('Precipitación', style = {"fontWeight":"lighter","textAlign":"center"}),
                html.H5('{0}'.format('Día'), style = {'color':'darkblue','textAlign':'center'}),
                html.H3('{0}{1}'.format(prec,' mm'), style = {'color':'black','textAlign':'center'}),
                html.H5('{0}'.format(' '), style = {'color':'#4e73df','textAlign':'center'}),
                #html.H6('{0}'.format(name), style = {"fontWeight":"lighter","textAlign":"center"}),
                #dcc.Markdown(dangerously_allow_html = True,
                   #children = ["<sub>+{0}{1}{2}</sub>".format("$",diff_1,"M")],style = {'color':'#090059','textAlign':'center'}
                   #)
                ]
            )
        
        ]
    
    card_content6 = [
        
        dbc.CardBody(
            [
                html.H6('Dirección del viento', style = {"fontWeight":"lighter","textAlign":"center"}),
                html.H5('{0}'.format(wind_dir(wind_d)), style = {'color':'red','textAlign':'center'}),
                html.H3('{0}{1}'.format(wind_d,' °'), style = {'color':'black','textAlign':'center'}),
                html.H5('{0}{1}'.format('Predominante: ',wind_d_mode), style = {'color':'orange','textAlign':'center'}),
                #html.H6('{0}'.format(name), style = {"fontWeight":"lighter","textAlign":"center"}),
                #dcc.Markdown(dangerously_allow_html = True,
                   #children = ["<sub>+{0}{1}{2}</sub>".format("$",diff_1,"M")],style = {'color':'#090059','textAlign':'center'}
                   #)
                ]
            )
        
        ]
    
    card_content7 = [
        
        dbc.CardBody(
            [
                html.H6('Velocidad del viento', style = {"fontWeight":"lighter","textAlign":"center"}),
                html.H5('{0}{1}'.format('max: ', wind_vmax), style = {'color':'#4e73df','textAlign':'center'}),
                html.H3('{0}{1}'.format(wind_v,' kmh'), style = {'color':'black','textAlign':'center'}),
                html.H5('{0}'.format(' '), style = {'color':'lightblue','textAlign':'center'}),
                #html.H6('{0}'.format(name), style = {"fontWeight":"lighter","textAlign":"center"}),
                #dcc.Markdown(dangerously_allow_html = True,
                   #children = ["<sub>+{0}{1}{2}</sub>".format("$",diff_1,"M")],style = {'color':'#090059','textAlign':'center'}
                   #)
                ]
            )
        
        ]
    
    card_content8 = [
        
        dbc.CardBody(
            [
                html.H6('Radiación Solar', style = {"fontWeight":"lighter","textAlign":"center"}),
                html.H5('{0}{1}'.format('max: ',solar_max), style = {'color':'red','textAlign':'center'}),
                html.H3('{0}{1}'.format(solar,' wm2'), style = {'color':'black','textAlign':'center'}),
                html.H5('{0}'.format(' '), style = {'color':'lightblue','textAlign':'center'}),
                #html.H6('{0}'.format(name), style = {"fontWeight":"lighter","textAlign":"center"}),
                #dcc.Markdown(dangerously_allow_html = True,
                   #children = ["<sub>+{0}{1}{2}</sub>".format("$",diff_1,"M")],style = {'color':'#090059','textAlign':'center'}
                   #)
                ]
            )
        
        ]
    
    card_content9 = [
        
        dbc.CardBody(
            [
                html.H6('Radiación UV', style = {"fontWeight":"lighter","textAlign":"center"}),
                html.H5('{0}{1}'.format('max: ', uv_max), style = {'color':'red','textAlign':'center'}),
                html.H3('{0}{1}'.format(uv,' index'), style = {'color':'black','textAlign':'center'}),
                html.H5('{0}'.format(' '), style = {'color':'lightblue','textAlign':'center'}),
                #html.H6('{0}'.format(name), style = {"fontWeight":"lighter","textAlign":"center"}),
                #dcc.Markdown(dangerously_allow_html = True,
                   #children = ["<sub>+{0}{1}{2}</sub>".format("$",diff_1,"M")],style = {'color':'#090059','textAlign':'center'}
                   #)
                ]
            )
        
        ]
    
    card_content10 = [
        
        dbc.CardBody(
            [
                html.H6('Temperatura del aire', style = {"fontWeight":"lighter","textAlign":"center"}),
                html.H5('{0}{1}'.format('max: ',temp_max,), style = {'color':'red','textAlign':'center'}),
                html.H3('{0}{1}'.format(temp,' °C'), style = {'color':'black','textAlign':'center'}),
                html.H5('{0}{1}'.format('min: ',temp_min), style = {'color':'blue','textAlign':'center'}),
                          
               
                ]
            )
                
        ]  
    
    return card_content1, card_content2, card_content3, card_content4, card_content5, \
           card_content6, card_content7, card_content8, card_content9, card_content10, 
           
    
#if __name__ == "__main__":
#    app.run_server()
