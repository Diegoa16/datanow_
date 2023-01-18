import dash
import plotly
from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
from datetime import datetime, date
import psycopg2
from datetime import datetime, tzinfo, timedelta
from dateutil import tz
import pytz
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
from io import BytesIO
from django_plotly_dash import DjangoDash
#from dash_extensions.snippets import send_bytes

## reading weather station ID dataset
data = pd.read_csv("core/dash_apps/estaciones_mtgnet.csv", sep=';')
MA_LOGO = 'https://www.meteoagro.co/static/core/img/logo.png'

app = DjangoDash('_downloads', external_stylesheets=[dbc.themes.BOOTSTRAP])

card_content_dropdwn1 = [
    dbc.CardBody(
        [
            html.H6('1. Seleccione la estación', style = {'textAlign':'center'}),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    #html.H6('Current Period'),
                    
                    dcc.Dropdown(id= 'station-dropdown1',
                                 options = [{'label':i,'value':i} for i in data['NOMBRE'].unique()],
                                 value = '',
                                 placeholder = 'Selecione la estación a consultar',
                                 ),
                    ], style = {'width':'100%'}),               
                ])
            ]
        )
    ]
card_content_datep1 = [
    dbc.CardBody(
        [
            html.H6('2. Seleccion el rango de fechas', style = {'textAlign':'center'}),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.DatePickerRange(id='date_pick_range1',
                                        start_date = date.today().strftime('%Y-%m-%d'),
                                        #end_date_placeholder_text = 'Select a date'
                                        min_date_allowed = datetime(2020,1,1),
                                        #max_date_allowed = datetime(2025,,19),
                                        end_date = date.today().strftime('%Y-%m-%d')
                                        ),
                    ], style = {'width':'100%'}),               
                ])
            ]
        )
    ]

card_content_checklist1 = [
    dbc.CardBody(
        [
            html.H6('3. Seleccione periodicidad', style = {'textAlign':'center'}),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(id = 'dropdown_periodicidad',
                        options = [
                            {'label':'Minutal', 'value':5},
                            {'label':'Horario', 'value':3},
                            {'label':'Diario', 'value':1, 'disabled':False}
                            ],
                        value =3,
                        placeholder = 'Seleccione periodicidad',
                        multi = False
                        )], style = {'width':'100%'}),               
                ])
            ]
        )
    ]

card_content_checklist2 = [
    dbc.CardBody(
        [
            html.H6('4. Seleccione formato de salida', style = {'textAlign':'center'}),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(id = 'dropdown_formato',
                        options = [
                            {'label':'csv', 'value':7},
                            {'label':'pdf', 'value':9},
                            ],
                        value = 7,
                        placeholder = 'Seleccione formato',
                        multi = False
                        )], style = {'width':'100%'}),               
                ])
            ]
        )
    ]

card_content_button1 = [
    dbc.CardBody(
        [
            html.H6('5. Descargue la información', style = {'textAlign':'center'}),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Button(id='submit-button-state1', n_clicks=0, children='Descargar'), dcc.Download(id="download1"),
                    ], style = {'width':'100%'}),               
                ])
            ]
        )
    ]


body_app = dbc.Container([
    
    
    html.Hr(),
    
    dbc.Row(html.H4('Módulo de descarga de datos'), style={'color':'#4e73df', 'text-align':'center'}),
    
    html.Hr(),
    html.Br(),
    dbc.Row([
            dbc.Col([dbc.Card(card_content_dropdwn1, style={'height':'200px','text-align':'center'})]),
            dbc.Col([dbc.Card(card_content_datep1, style={'height':'200px', 'text-align':'center'})]),
            dbc.Col([dbc.Card(card_content_checklist1, style={'height':'200px', 'text-align':'center'})])
            ]),
    html.Br(),
    dbc.Row([
            dbc.Col([dbc.Card(card_content_checklist2, style={'height':'200px', 'text-align':'center'})]),
            dbc.Col(dcc.Loading(children=[dbc.Card(card_content_button1, style={'height':'200px', 'text-align':'center'})], fullscreen=True)),
            ]),
    html.Br(),
    html.Hr(),
    
    
    
    html.Br(),
    
    
    ],
    style = {'backgroundColor':'#f7f7f7'})

app.layout = html.Div([body_app])
    
@app.callback(Output("download1", "data"),
              [Input('station-dropdown1','value'),
               Input('date_pick_range1', 'start_date'),
               Input('date_pick_range1', 'end_date'),
               Input('dropdown_periodicidad','value'),
               Input('dropdown_formato','value'),
               Input("submit-button-state1", "n_clicks")])
def generate_df1(value, start_date, end_date, value1, value2, n_clicks):
    if value:
        ## connecting to postgresql
        conn = psycopg2.connect(host='', port = , database='', user='', password='')
        ## reset button
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if 'submit-button-state1' in changed_id:
            station = data[data['NOMBRE']==value].reset_index()['ID'][0]
            date_ini = datetime.strptime(start_date, "%Y-%m-%d")
            #print(date_ini)
            ini = date_ini - timedelta(days=1)
            date_fin = datetime.strptime(end_date, "%Y-%m-%d")
            #print(date_fin)
            fin = date_fin + timedelta(days=2)
            fin2 = (date_fin + timedelta(days=1)).strftime('%Y-%m-%d')
            #statment= f""" SELECT * FROM ws_climate_hour_data WHERE gpm_code = '{station}' AND wshour_report_date between '{ini}' and '{fin}' """
            statment= f"""SELECT * FROM ws_climate_data WHERE gpm_code = '{station}' AND wswdat_report_date between '{ini}' and '{fin}' ORDER BY wswdat_report_date ASC """
            df= pd.read_sql_query(statment,con=conn)
            local_zone = tz.tzlocal()
            df['ws_report_date_local'] = pd.DatetimeIndex(df['wswdat_report_date']).tz_convert(local_zone)
            mask = (df['ws_report_date_local'] >= start_date) & (df['ws_report_date_local'] <= fin2 )
            df = df.loc[mask]
            #df = df.sort_values(by='ws_report_date_local')
            df['percip_interval_mm'] = (df['wswdat_precip_today_mm'] - df['wswdat_precip_today_mm'].shift(1))
            df.loc[df["percip_interval_mm"] < 0, "percip_interval_mm"] = 0
            df1 = df[['ws_report_date_local', 'gpm_code','wswdat_temp_c','wswdat_relative_humidity','wswdat_dewpoint_c',
                    'wswdat_pressure_rel_hpa','wswdat_pressure_abs_hpa','wswdat_precip_rate_mmh','wswdat_precip_today_mm',
                    'percip_interval_mm','wswdat_wind_degrees','wswdat_wind_dir','wswdat_wind_speed_kmh','wswdat_wind_gust_kmh','wswdat_windchill_c',
                    'wswdat_heat_index_c','wswdat_solar_rad_wm2','wswdat_illuminance_lux','wswdat_uv_index','wswdat_eto_mm']] 
            df1.columns = ['Fecha', 'ID_Estacion','Temp_celsius','Hum_Rel_%','Pto_Rocio_Celsius',
                    'Presion_rel_hpa','Presion_abs_hpa','Precip_rate_mmh','Precip_hoy_mm',
                    'Precip_interval_mm','Dir_viento_grados','Dir_viento_cardinal','Vel_viento_kmh','Rafaga_viento_kmh','Enfriamiento_aire_celsius',
                    'Indice_calor_celsius','Solar_rad_wm2','Iluminancia_lux','UV_index','Eto_mm']
            df1['Solar_rad_wm2'] = df1['Solar_rad_wm2'].replace(0, np.NaN)
            df1 = df1.replace([None], np.NaN)
            
            if value1 == 5 and value2 == 7:
                return dcc.send_data_frame(df1.to_csv, filename=f"{station}_{start_date}_{end_date}.csv", index=False, sep=';', decimal=',')
            elif value1 == 3 and value2 == 7:
                # Summarize to hour
                # Variables promediadas, max,min
                df_p = df1[['Fecha','Temp_celsius','Hum_Rel_%','Pto_Rocio_Celsius',
                        'Presion_rel_hpa','Presion_abs_hpa','Dir_viento_grados','Vel_viento_kmh','Rafaga_viento_kmh',
                        'Enfriamiento_aire_celsius','Indice_calor_celsius','Solar_rad_wm2','Iluminancia_lux','UV_index']]
                df_p['Solar_rad_wm2'] = df_p['Solar_rad_wm2'].replace(np.NaN, 0)
                df_h_mean = round(df_p.groupby(pd.Grouper(key='Fecha', freq='60min')).mean(),1)
                df_x = df1[['Fecha','Temp_celsius','Hum_Rel_%','Pto_Rocio_Celsius',
                        'Presion_rel_hpa','Presion_abs_hpa','Precip_hoy_mm','Vel_viento_kmh','Rafaga_viento_kmh',
                        'Enfriamiento_aire_celsius','Indice_calor_celsius','Solar_rad_wm2','Iluminancia_lux','UV_index','Eto_mm']]
                df_x['Solar_rad_wm2'] = df_x['Solar_rad_wm2'].replace(np.NaN, 0)
                df_h_max = round(df_x.groupby(pd.Grouper(key='Fecha', freq='60min')).max(),1)
                df_h_max.columns=["X"+str(i) for i in range(1, len(df_h_max.columns)+1)]
                df_n = df1[['Fecha','Temp_celsius','Hum_Rel_%','Pto_Rocio_Celsius',
                        'Presion_rel_hpa','Presion_abs_hpa','Enfriamiento_aire_celsius','Indice_calor_celsius']]
                df_h_min = round(df_n.groupby(pd.Grouper(key='Fecha', freq='60min')).min(),1)
                df_h_min.columns=["N"+str(i) for i in range(1, len(df_h_min.columns)+1)]
                # Variables agregadas
                df_h_sum = df1[['Fecha','Precip_interval_mm']]
                df_h_sum = round(df_h_sum.groupby(pd.Grouper(key='Fecha', freq='60min')).sum(),1)
                # Unión de dataframes
                dfmerged = pd.merge(df_h_mean,df_h_min,on='Fecha')
                dfmerged = pd.merge(dfmerged,df_h_max,on='Fecha')
                dfmerged = pd.merge(dfmerged,df_h_sum,on='Fecha')
                dfmerged['ID_Estacion'] = f'{station}' 
                dfinal = dfmerged[['ID_Estacion','Temp_celsius','N1','X1','Hum_Rel_%','N2','X2','Pto_Rocio_Celsius','N3','X3',
                                    'Presion_rel_hpa','N4','X4','Presion_abs_hpa','N5','X5','X6','Precip_interval_mm','Dir_viento_grados',
                                    'Vel_viento_kmh','X7','Rafaga_viento_kmh','X8','Enfriamiento_aire_celsius','Solar_rad_wm2','X13','X14']] 
                dfinal.columns = ['ID_Estacion','Tprom_celsius','Tmin_celsius','Tmax_celsius','Hum_Rel_prom_%','Hum_Rel_min_%','Hum_Rel_max_%','Rocio_prom_celsius','Rocio_min_celsius','Rocio_max_celsius',
                                    'Presion_rel_prom_hpa','Presion_rel_min_hpa','Presion_rel_max_hpa','Presion_abs_prom_hpa','Presion_abs_min_hpa','Presion_abs_max_hpa',
                                    'Precip_acum_dia_mm','Precip_hora_mm','Dir_viento_prom_grados','Vel_viento_prom_kmh','Vel_viento_max_kmh','Rafaga_viento_prom_kmh','Rafaga_viento_max_kmh',
                                    'Enfriamiento_aire_prom_celsius','Solar_rad_prom_wm2','UV_index_max','Eto_hora_mm']
                dfinal = dfinal.reset_index()
                dfinal['Fecha'] = dfinal['Fecha'].dt.strftime('%Y-%m-%d %H:%M')
                return dcc.send_data_frame(dfinal.to_csv, filename=f"{station}_{start_date}_{end_date}.csv", index=False, sep=',', decimal='.')
            elif value1 == 3 and value2 == 7:
                return dcc.send_data_frame(dfinal.to_csv, filename=f"{station}_{start_date}_{end_date}.csv", index=False, sep=',', decimal='.')
            elif value1 == 1 and value2 == 7:
                pass
            elif value1 == 3  and value2 == 9:
                # Summarize to hour
                # Variables promediadas, max,min
                df_p = df1[['Fecha','Temp_celsius','Hum_Rel_%','Pto_Rocio_Celsius',
                        'Presion_rel_hpa','Presion_abs_hpa','Dir_viento_grados','Vel_viento_kmh','Rafaga_viento_kmh',
                        'Enfriamiento_aire_celsius','Indice_calor_celsius','Solar_rad_wm2','Iluminancia_lux','UV_index']]
                df_p['Solar_rad_wm2'] = df_p['Solar_rad_wm2'].replace(np.NaN, 0)
                df_h_mean = round(df_p.groupby(pd.Grouper(key='Fecha', freq='60min')).mean(),1)
                df_x = df1[['Fecha','Temp_celsius','Hum_Rel_%','Pto_Rocio_Celsius',
                        'Presion_rel_hpa','Presion_abs_hpa','Precip_hoy_mm','Vel_viento_kmh','Rafaga_viento_kmh',
                        'Enfriamiento_aire_celsius','Indice_calor_celsius','Solar_rad_wm2','Iluminancia_lux','UV_index','Eto_mm']]
                df_x['Solar_rad_wm2'] = df_x['Solar_rad_wm2'].replace(np.NaN, 0)
                df_h_max = round(df_x.groupby(pd.Grouper(key='Fecha', freq='60min')).max(),1)
                df_h_max.columns=["X"+str(i) for i in range(1, len(df_h_max.columns)+1)]
                df_n = df1[['Fecha','Temp_celsius','Hum_Rel_%','Pto_Rocio_Celsius',
                        'Presion_rel_hpa','Presion_abs_hpa','Enfriamiento_aire_celsius','Indice_calor_celsius']]
                df_h_min = round(df_n.groupby(pd.Grouper(key='Fecha', freq='60min')).min(),1)
                df_h_min.columns=["N"+str(i) for i in range(1, len(df_h_min.columns)+1)]
                # Variables agregadas
                df_h_sum = df1[['Fecha','Precip_interval_mm']]
                df_h_sum = round(df_h_sum.groupby(pd.Grouper(key='Fecha', freq='60min')).sum(),1)
                # Unión de dataframes
                dfmerged = pd.merge(df_h_mean,df_h_min,on='Fecha')
                dfmerged = pd.merge(dfmerged,df_h_max,on='Fecha')
                dfmerged = pd.merge(dfmerged,df_h_sum,on='Fecha')
                dfmerged['ID_Estacion'] = 'COLCUBO28'
                dfinal = dfmerged[['ID_Estacion','Temp_celsius','N1','X1','Hum_Rel_%','N2','X2','Pto_Rocio_Celsius','N3','X3',
                                    'Presion_rel_hpa','N4','X4','Presion_abs_hpa','N5','X5','X6','Precip_interval_mm','Dir_viento_grados',
                                    'Vel_viento_kmh','X7','Rafaga_viento_kmh','X8','Enfriamiento_aire_celsius','Solar_rad_wm2','X13','X14']] 
                dfinal.columns = ['ID_Estacion','Tprom_celsius','Tmin_celsius','Tmax_celsius','Hum_Rel_prom_%','Hum_Rel_min_%','Hum_Rel_max_%','Rocio_prom_celsius','Rocio_min_celsius','Rocio_max_celsius',
                                    'Presion_rel_prom_hpa','Presion_rel_min_hpa','Presion_rel_max_hpa','Presion_abs_prom_hpa','Presion_abs_min_hpa','Presion_abs_max_hpa',
                                    'Precip_acum_dia_mm','Precip_hora_mm','Dir_viento_prom_grados','Vel_viento_prom_kmh','Vel_viento_max_kmh','Rafaga_viento_prom_kmh','Rafaga_viento_max_kmh',
                                    'Enfriamiento_aire_prom_celsius','Solar_rad_prom_wm2','UV_index_max','Eto_hora_mm']
                dfinal = dfinal.reset_index()
                dfinal['Fecha'] = dfinal['Fecha'].dt.strftime('%Y-%m-%d %H:%M')
                def create_pdf(n_clicks):
                    # Graficas datos 
                    s = 3
                    r = 90
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    plt.plot(dfinal['Fecha'], dfinal['Tprom_celsius'], color = 'r')
                    #plt.plot(dfinal['Fecha'], dfinal['Tmax_celsius'], label="line2", color = 'r')
                    plt.title('Temperatura del aire', fontsize=10)
                    plt.ylabel('°C', fontsize=10)
                    plt.xticks(dfinal['Fecha'], dfinal['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    # Converting Figure to an image:
                    img_buf = BytesIO()  # Create image object
                    plt.savefig(img_buf, dpi=200, bbox_inches='tight')  # Save the 
            
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    plt.plot(dfinal['Fecha'], dfinal['Hum_Rel_prom_%'],  label="line1", color = 'b')
                    #plt.plot(dfinal['Fecha'], dfinal['Tmax_celsius'], label="line2", color = 'r')
                    plt.title('Humedad del aire', fontsize=10)
                    plt.ylabel('%', fontsize=10)
                    plt.xticks(dfinal['Fecha'], dfinal['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    # Converting Figure to an image:
                    img_buf2 = BytesIO()  # Create image object
                    plt.savefig(img_buf2, dpi=200, bbox_inches='tight')  # Save the image
            
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    plt.plot(dfinal['Fecha'], dfinal['Presion_rel_prom_hpa'],  label="line1", color = 'g')
                    #plt.plot(dfinal['Fecha'], dfinal['Tmax_celsius'], label="line2", color = 'r')
                    plt.title('Presión del aire', fontsize=10)
                    plt.ylabel('hpa', fontsize=10)
                    plt.xticks(dfinal['Fecha'], dfinal['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    # Converting Figure to an image:
                    img_buf3 = BytesIO()  # Create image object
                    plt.savefig(img_buf3, dpi=200, bbox_inches='tight')  # Save the image
            
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    plt.bar(dfinal['Fecha'], dfinal['Precip_hora_mm'],  label="line1", color = 'b')
                    #plt.plot(dfinal['Fecha'], dfinal['Tmax_celsius'], label="line2", color = 'r')
                    plt.title('Precipitación', fontsize=10)
                    plt.ylabel('mm', fontsize=10)
                    plt.xticks(dfinal['Fecha'], dfinal['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    # Converting Figure to an image:
                    img_buf4 = BytesIO()  # Create image object
                    plt.savefig(img_buf4, dpi=200, bbox_inches='tight')  # Save the image
                    
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    plt.scatter(dfinal['Fecha'], dfinal['Dir_viento_prom_grados'],  label="line1", color = 'orange')
                    #plt.plot(dfinal['Fecha'], dfinal['Tmax_celsius'], label="line2", color = 'r')
                    plt.title('Dirección del viento', fontsize=10)
                    plt.ylabel('°', fontsize=10)
                    plt.xticks(dfinal['Fecha'], dfinal['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    # Setting the number of ticks
                    plt.ylim(0, 360)
                    plt.yticks([45, 90, 135, 180, 225, 270, 315, 360])
                    # Converting Figure to an image:
                    img_buf5 = BytesIO()  # Create image object
                    plt.savefig(img_buf5, dpi=200, bbox_inches='tight')  # Save the image
                    
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    plt.plot(dfinal['Fecha'], dfinal['Vel_viento_prom_kmh'],  label="Promedio", color = 'orange')
                    plt.scatter(dfinal['Fecha'], dfinal['Vel_viento_max_kmh'], label="Máximo", color = 'r')
                    plt.title('Velocidad del viento', fontsize=10)
                    plt.ylabel('kmh', fontsize=10)
                    plt.xticks(dfinal['Fecha'], dfinal['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    plt.legend(loc="upper left")
                    # Setting the number of ticks
                    #plt.ylim(0, 360)
                    #plt.yticks([45, 90, 135, 180, 225, 270, 315, 360])
                    # Converting Figure to an image:
                    img_buf6 = BytesIO()  # Create image object
                    plt.savefig(img_buf6, dpi=200, bbox_inches='tight')  # Save the image
                    
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    plt.plot(dfinal['Fecha'], dfinal['Rafaga_viento_prom_kmh'],  label="Promedio", color = 'orange')
                    plt.scatter(dfinal['Fecha'], dfinal['Rafaga_viento_max_kmh'], label="Máximo", color = 'r')
                    plt.title('Ráfaga de viento', fontsize=10)
                    plt.ylabel('kmh', fontsize=10)
                    plt.xticks(dfinal['Fecha'], dfinal['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    plt.legend(loc="upper left")
                    # Setting the number of ticks
                    #plt.ylim(0, 360)
                    #plt.yticks([45, 90, 135, 180, 225, 270, 315, 360])
                    # Converting Figure to an image:
                    img_buf7 = BytesIO()  # Create image object
                    plt.savefig(img_buf7, dpi=200, bbox_inches='tight')  # Save the image
                    
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    plt.plot(dfinal['Fecha'], dfinal['Solar_rad_prom_wm2'],  label="Promedio", color = 'yellow')
                    #plt.bar(dfinal['Fecha'], dfinal['UV_index_max'], label="Máximo", color = 'purple')
                    plt.title('Radiación solar', fontsize=10)
                    plt.ylabel('wm2', fontsize=10)
                    plt.xticks(dfinal['Fecha'], dfinal['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    plt.legend(loc="upper left")
                    # Setting the number of ticks
                    #plt.ylim(0, 360)
                    #plt.yticks([45, 90, 135, 180, 225, 270, 315, 360])
                    # Converting Figure to an image:
                    img_buf8 = BytesIO()  # Create image object
                    plt.savefig(img_buf8, dpi=200, bbox_inches='tight')  # Save the image
                    
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    #plt.plot(dfinal['Fecha'], dfinal['Solar_rad_prom_wm2'],  label="Promedio", color = 'yellow')
                    plt.bar(dfinal['Fecha'], dfinal['UV_index_max'], label="Máximo", color = 'purple')
                    plt.title('Radiación UV', fontsize=10)
                    plt.ylabel('Index', fontsize=10)
                    plt.xticks(dfinal['Fecha'], dfinal['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    plt.legend(loc="upper left")
                    # Setting the number of ticks
                    #plt.ylim(0, 360)
                    #plt.yticks([45, 90, 135, 180, 225, 270, 315, 360])
                    # Converting Figure to an image:
                    img_buf9 = BytesIO()  # Create image object
                    plt.savefig(img_buf9, dpi=200, bbox_inches='tight')  # Save the image
                    
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    plt.bar(dfinal['Fecha'], dfinal['Eto_hora_mm'],  label="line1", color = 'b')
                    #plt.plot(dfinal['Fecha'], dfinal['Tmax_celsius'], label="line2", color = 'r')
                    plt.title('Evapotranspiración', fontsize=10)
                    plt.ylabel('mm', fontsize=10)
                    plt.xticks(dfinal['Fecha'], dfinal['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    plt.ylim(0, 12)
                    # Converting Figure to an image:
                    img_buf10 = BytesIO()  # Create image object
                    plt.savefig(img_buf10, dpi=200, bbox_inches='tight')  # Save the image
            
                    plt.close('all')
                    
                    station = data[data['NOMBRE']==value].reset_index()['ID'][0]
                    #nombre = data[data['NOMBRE']==value].reset_index()['NOMBRE'][0]
                    lat = round(data[data['NOMBRE']==value].reset_index()['LAT'][0],2)
                    lon = round(data[data['NOMBRE']==value].reset_index()['LON'][0],2)
                    ciudad = data[data['NOMBRE']==value].reset_index()['CIUDAD'][0]
                    depto = data[data['NOMBRE']==value].reset_index()['DEPTO'][0]
                    pais = data[data['NOMBRE']==value].reset_index()['PAIS'][0]
                    
                    class PDF(FPDF):
                        def __init__(self):
                            super().__init__()
                        def header(self):
                            self.set_font('Arial', '', 12)
                            pdf.image(MA_LOGO, x=40, y=12.5, w=12, h=10)
                            self.cell(0, 15, f'Meteoagro DataNow - Resumen horario para el período {start_date} a {end_date}',align='C', border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                            pdf.ln(5)
                        def footer(self):
                            self.set_y(-15)
                            self.set_font('Arial', '', 12)
                            self.cell(0, 10, 'Meteoagro DataNow - 2022 - Todos los derechos reservados',align='C', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
                            
                    ch = 7
                    w1= 8
                    pdf = PDF() # Instance of custom class
                    pdf.add_page(orientation = 'L')
                    pdf.set_font('Helvetica', '', 10)
                    pdf.multi_cell(0, 10, f'ID Estación: {station}       Nombre: {value}        Ubicación: {ciudad}-{depto}-{pais}      Latitud: {lat}  Longitud: {lon} ',
                                border=1, align='C')
                    # Table Header
                    pdf.set_font('Arial', 'B', 6)
                    pdf.ln(5)
                    pdf.cell(w=22, h=14, txt='Fecha', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    #pdf.cell(w=18, h=14, txt='ID Estación', border=1, ln=0, align='C')
                    pdf.cell(w=24, h=ch, txt='Temperatura (°C)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=24, h=ch, txt='Humedad Relativa (%)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=24, h=ch, txt='Presión del aire (hpa)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=21, h=ch, txt='Precipitación (mm)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=21, h=ch, txt='Precipitación (mm)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='Dirección Viento', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='Velocidad Viento', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='Velocidad Viento', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='Ráfaga Viento', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='Ráfaga Viento', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='Radiacion Solar', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=15, h=ch, txt='UV Index', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='ETo (mm)', border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
                    pdf.cell(w=22, h=ch, txt='', border=0, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    #pdf.cell(w=18, h=ch, txt='', border=0, ln=0, align='C')
                    pdf.cell(w=w1, h=ch, txt='prom', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=w1, h=ch, txt='min', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=w1, h=ch, txt='max', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=w1, h=ch, txt='prom', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=w1, h=ch, txt='min', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=w1, h=ch, txt='max', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=w1, h=ch, txt='prom', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=w1, h=ch, txt='min', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=w1, h=ch, txt='max', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=21, h=ch, txt='acumulado horario', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=21, h=ch, txt='acumulado diario', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='promedio (°)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='promedio (kmh)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='máximo (kmh)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='promedio (kmh)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='máximo (kmh)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='wm2 hora', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=15, h=ch, txt='prom hora', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='acum horario', border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
                    # Table contents
                    pdf.set_font('Arial', '', 7)
                    for i in range(0, len(dfinal)):
                        pdf.cell(w=22, h=ch, 
                                txt=dfinal['Fecha'].iloc[i], 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=w1, h=ch, 
                                txt=dfinal['Tprom_celsius'].iloc[i].astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=w1, h=ch, 
                                txt=dfinal['Tmin_celsius'].iloc[i].astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=w1, h=ch, 
                                txt=dfinal['Tmax_celsius'].iloc[i].astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=w1, h=ch, 
                                txt=dfinal['Hum_Rel_prom_%'].iloc[i].astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=w1, h=ch, 
                                txt=dfinal['Hum_Rel_min_%'].iloc[i].astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=w1, h=ch, 
                                txt=dfinal['Hum_Rel_max_%'].iloc[i].astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=w1, h=ch, 
                                txt=dfinal['Presion_abs_prom_hpa'].iloc[i].astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=w1, h=ch, 
                                txt=dfinal['Presion_abs_min_hpa'].iloc[i].astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=w1, h=ch, 
                                txt=dfinal['Presion_abs_max_hpa'].iloc[i].astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=21, h=ch, 
                                txt=round(dfinal['Precip_hora_mm'].iloc[i],1).astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=21, h=ch, 
                                txt=round(dfinal['Precip_acum_dia_mm'].iloc[i],1).astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=18, h=ch, 
                                txt=round(dfinal['Dir_viento_prom_grados'].iloc[i],1).astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=18, h=ch, 
                                txt=round(dfinal['Vel_viento_prom_kmh'].iloc[i],1).astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=18, h=ch, 
                                txt=round(dfinal['Vel_viento_max_kmh'].iloc[i],1).astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=18, h=ch, 
                                txt=round(dfinal['Rafaga_viento_prom_kmh'].iloc[i],1).astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=18, h=ch, 
                                txt=round(dfinal['Rafaga_viento_max_kmh'].iloc[i],1).astype(str), 
                                border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=18, h=ch, 
                                txt=round(dfinal['Solar_rad_prom_wm2'].iloc[i],1).astype(str), 
                                border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=15, h=ch, 
                                txt=round(dfinal['UV_index_max'].iloc[i],1).astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=18, h=ch, 
                                txt=round(dfinal['Eto_hora_mm'].iloc[i],1).astype(str), 
                                border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
                    pdf.ln(5)
                    pdf.set_font('Arial', 'B', 12)
                    pdf.cell(0, 10, 'Gráficas de los datos', 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
                    pdf.image(img_buf,w=pdf.epw,h=50) # Make the image full width
                    pdf.ln(5)
                    pdf.image(img_buf2,w=pdf.epw,h=50)
                    pdf.ln(5)
                    pdf.image(img_buf3,w=pdf.epw,h=50)
                    pdf.ln(5)
                    pdf.image(img_buf4,w=pdf.epw,h=50) # Make the image full width
                    pdf.ln(5)
                    pdf.image(img_buf5,w=pdf.epw,h=50) # Make the image full width
                    pdf.ln(5)
                    pdf.image(img_buf6,w=pdf.epw,h=50) # Make the image full 
                    pdf.ln(5)
                    pdf.image(img_buf7,w=pdf.epw,h=50) # Make the image full width
                    pdf.ln(5)
                    pdf.image(img_buf8,w=pdf.epw,h=50) # Make the image full width
                    pdf.ln(5)
                    pdf.image(img_buf9,w=pdf.epw,h=50) # Make the image full width
                    pdf.ln(5)
                    pdf.image(img_buf10,w=pdf.epw,h=50) # Make the image full width
                    return pdf
                
                def write_pdf(bytes_io):
                    pdf = create_pdf(n_clicks) # pass argument to PDF creation here
                    bytes_io.write(pdf.output())

                return dcc.send_bytes(write_pdf, f'{station}_{start_date}_{end_date}.pdf')
            
            elif value1 == 1  and value2 == 9:
                # Summarize to hour
                # Variables promediadas, max,min
                df_p = df1[['Fecha','Temp_celsius','Hum_Rel_%','Pto_Rocio_Celsius',
                        'Presion_rel_hpa','Presion_abs_hpa','Dir_viento_grados','Vel_viento_kmh','Rafaga_viento_kmh',
                        'Enfriamiento_aire_celsius','Indice_calor_celsius','Solar_rad_wm2','Iluminancia_lux','UV_index']]
                df_p['Solar_rad_wm2'] = df_p['Solar_rad_wm2'].replace(np.NaN, 0)
                df_h_mean = round(df_p.groupby(pd.Grouper(key='Fecha', freq='60min')).mean(),1)
                df_x = df1[['Fecha','Temp_celsius','Hum_Rel_%','Pto_Rocio_Celsius',
                        'Presion_rel_hpa','Presion_abs_hpa','Precip_hoy_mm','Vel_viento_kmh','Rafaga_viento_kmh',
                        'Enfriamiento_aire_celsius','Indice_calor_celsius','Solar_rad_wm2','Iluminancia_lux','UV_index','Eto_mm']]
                df_x['Solar_rad_wm2'] = df_x['Solar_rad_wm2'].replace(np.NaN, 0)
                df_h_max = round(df_x.groupby(pd.Grouper(key='Fecha', freq='60min')).max(),1)
                df_h_max.columns=["X"+str(i) for i in range(1, len(df_h_max.columns)+1)]
                df_n = df1[['Fecha','Temp_celsius','Hum_Rel_%','Pto_Rocio_Celsius',
                        'Presion_rel_hpa','Presion_abs_hpa','Enfriamiento_aire_celsius','Indice_calor_celsius']]
                df_h_min = round(df_n.groupby(pd.Grouper(key='Fecha', freq='60min')).min(),1)
                df_h_min.columns=["N"+str(i) for i in range(1, len(df_h_min.columns)+1)]
                # Variables agregadas
                df_h_sum = df1[['Fecha','Precip_interval_mm']]
                df_h_sum = round(df_h_sum.groupby(pd.Grouper(key='Fecha', freq='60min')).sum(),1)
                # Unión de dataframes
                dfmerged = pd.merge(df_h_mean,df_h_min,on='Fecha')
                dfmerged = pd.merge(dfmerged,df_h_max,on='Fecha')
                dfmerged = pd.merge(dfmerged,df_h_sum,on='Fecha')
                dfmerged['ID_Estacion'] = f'{station}' 
                dfinal = dfmerged[['ID_Estacion','Temp_celsius','N1','X1','Hum_Rel_%','N2','X2','Pto_Rocio_Celsius','N3','X3',
                                    'Presion_rel_hpa','N4','X4','Presion_abs_hpa','N5','X5','X6','Precip_interval_mm','Dir_viento_grados',
                                    'Vel_viento_kmh','X7','Rafaga_viento_kmh','X8','Enfriamiento_aire_celsius','Solar_rad_wm2','X13','X14']] 
                dfinal.columns = ['ID_Estacion','Tprom_celsius','Tmin_celsius','Tmax_celsius','Hum_Rel_prom_%','Hum_Rel_min_%','Hum_Rel_max_%','Rocio_prom_celsius','Rocio_min_celsius','Rocio_max_celsius',
                                    'Presion_rel_prom_hpa','Presion_rel_min_hpa','Presion_rel_max_hpa','Presion_abs_prom_hpa','Presion_abs_min_hpa','Presion_abs_max_hpa',
                                    'Precip_acum_dia_mm','Precip_hora_mm','Dir_viento_prom_grados','Vel_viento_prom_kmh','Vel_viento_max_kmh','Rafaga_viento_prom_kmh','Rafaga_viento_max_kmh',
                                    'Enfriamiento_aire_prom_celsius','Solar_rad_prom_wm2','UV_index_max','Eto_hora_mm']
                dfinal = dfinal.reset_index()
                #dfinal['Fecha'] = dfinal['Fecha'].dt.strftime('%Y-%m-%d %H:%M')
                # Summarize to daily
                day_mean = round(dfinal.groupby(pd.Grouper(key='Fecha', freq='1D')).mean(),1)
                day_min = round(dfinal.groupby(pd.Grouper(key='Fecha', freq='1D')).min(),1)
                day_max = round(dfinal.groupby(pd.Grouper(key='Fecha', freq='1D')).max(),1)
                day_sum = round(dfinal.groupby(pd.Grouper(key='Fecha', freq='1D')).sum(),1)
                day_merged = pd.merge(day_mean,day_min,on='Fecha')
                day_merged.columns=["F"+str(i) for i in range(1, len(day_merged.columns)+1)]
                day_merged = pd.merge(day_merged,day_max,on='Fecha')
                day_merged = pd.merge(day_merged,day_sum,on='Fecha')
                day_merged.columns=["F"+str(i) for i in range(1, len(day_merged.columns)+1)]
                day_df = day_merged[['F27','F1','F29','F57','F4','F32','F60','F7','F35','F63','F10','F38','F66','F13','F41','F69','F70','F18','F19','F74','F21','F76','F23','F104','F79','F106']]
                day_df.columns = ['ID_Estacion','Tprom_celsius_dia','Tmin_celsius_dia','Tmax_celsius_dia','Hum_Rel_prom_%_dia','Hum_Rel_min_%_dia','Hum_Rel_max_%_dia','Rocio_prom_celsius_dia','Rocio_min_celsius_dia','Rocio_max_celsius_dia',
                                    'Presion_rel_prom_hpa_dia','Presion_rel_min_hpa_dia','Presion_rel_max_hpa_dia','Presion_abs_prom_hpa_dia','Presion_abs_min_hpa_dia','Presion_abs_max_hpa_dia',
                                    'Precip_acum_dia_mm','Dir_viento_prom_dia_grados','Vel_viento_prom_kmh_dia','Vel_viento_max_kmh_dia','Rafaga_viento_prom_kmh_dia','Rafaga_viento_max_kmh_dia',
                                    'Enfriamiento_aire_prom_celsius_dia','Solar_rad_acum_dia_kwm2d','UV_index_max_dia','Eto_acum_dia_mm']
                day_df['Solar_rad_acum_dia_kwm2d'] = day_df['Solar_rad_acum_dia_kwm2d'] * 0.001
                day_df['Eto_acum_dia_mm'] = day_df['Eto_acum_dia_mm'].replace(0,np.NaN)
                day_df = day_df.reset_index()
                day_df['Fecha'] = day_df['Fecha'].dt.strftime('%Y-%m-%d %H:%M')
                def create_pdf(n_clicks):
                    # Graficas datos 
                    s = 3
                    r = 90
                    # Gráfica de temperatura del aire diaria
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    plt.plot(day_df['Fecha'], day_df['Tprom_celsius_dia'], label="Tprom", color = 'red')
                    plt.plot(day_df['Fecha'], day_df['Tmax_celsius_dia'], label="Tmax", color = 'darkred')
                    plt.plot(day_df['Fecha'], day_df['Tmin_celsius_dia'], label="Tmin", color = 'darkblue')
                    plt.title('Temperatura del aire', fontsize=10)
                    plt.ylabel('°C', fontsize=10)
                    plt.xticks(day_df['Fecha'], day_df['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    plt.legend(loc="upper left")
                    # Converting Figure to an image:
                    img_buf1 = BytesIO()  # Create image object
                    plt.savefig(img_buf1, dpi=200, bbox_inches='tight')  # Save the 
                    # Gráfica de humedad del aire diaria
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    plt.plot(day_df['Fecha'], day_df['Hum_Rel_prom_%_dia'], label="HRprom", color = 'blue')
                    plt.plot(day_df['Fecha'], day_df['Hum_Rel_min_%_dia'], label="HRmin", color = 'darkred')
                    plt.plot(day_df['Fecha'], day_df['Hum_Rel_max_%_dia'], label="HRmax", color = 'darkblue')
                    plt.title('Humedad del aire', fontsize=10)
                    plt.ylabel('%', fontsize=10)
                    plt.xticks(day_df['Fecha'], day_df['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    plt.legend(loc="upper left")
                    # Converting Figure to an image:
                    img_buf2 = BytesIO()  # Create image object
                    plt.savefig(img_buf2, dpi=200, bbox_inches='tight')  # Save the 
                    # Gráfica de presión del aire diaria
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    plt.plot(day_df['Fecha'], day_df['Presion_abs_prom_hpa_dia'], label="Promedio", color = 'green')
                    plt.plot(day_df['Fecha'], day_df['Presion_abs_min_hpa_dia'], label="Mínima", color = 'darkred')
                    plt.plot(day_df['Fecha'], day_df['Presion_abs_max_hpa_dia'], label="Máxima", color = 'darkblue')
                    plt.title('Presión del aire', fontsize=10)
                    plt.ylabel('%', fontsize=10)
                    plt.xticks(day_df['Fecha'], day_df['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    plt.legend(loc="upper left")
                    # Converting Figure to an image:
                    img_buf3 = BytesIO()  # Create image object
                    plt.savefig(img_buf3, dpi=200, bbox_inches='tight')  # Save the
                    # Gráfica de precipitación diaria
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    plt.bar(day_df['Fecha'], day_df['Precip_acum_dia_mm'],  label="Precipitación día", color = 'b')
                    #plt.plot(dfinal['Fecha'], dfinal['Tmax_celsius'], label="line2", color = 'r')
                    plt.title('Precipitación', fontsize=10)
                    plt.ylabel('mm', fontsize=10)
                    plt.xticks(day_df['Fecha'], day_df['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    # Converting Figure to an image:
                    img_buf4 = BytesIO()  # Create image object
                    plt.savefig(img_buf4, dpi=200, bbox_inches='tight')  # Save the image
                    # Gráfica de dirección del viento
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    plt.scatter(day_df['Fecha'], day_df['Dir_viento_prom_dia_grados'],  label="line1", color = 'orange')
                    #plt.plot(dfinal['Fecha'], dfinal['Tmax_celsius'], label="line2", color = 'r')
                    plt.title('Dirección del viento', fontsize=10)
                    plt.ylabel('°', fontsize=10)
                    plt.xticks(day_df['Fecha'], day_df['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    # Setting the number of ticks
                    plt.ylim(0, 360)
                    plt.yticks([45, 90, 135, 180, 225, 270, 315, 360])
                    # Converting Figure to an image:
                    img_buf5 = BytesIO()  # Create image object
                    plt.savefig(img_buf5, dpi=200, bbox_inches='tight')  # Save the image
                    # Gráfica de velocidad del viento
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    plt.plot(day_df['Fecha'], day_df['Vel_viento_prom_kmh_dia'],  label="Promedio", color = 'orange')
                    plt.scatter(day_df['Fecha'], day_df['Vel_viento_max_kmh_dia'], label="Máximo", color = 'r')
                    plt.title('Velocidad del viento', fontsize=10)
                    plt.ylabel('kmh', fontsize=10)
                    plt.xticks(day_df['Fecha'], day_df['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    plt.legend(loc="upper left")
                    # Setting the number of ticks
                    #plt.ylim(0, 360)
                    #plt.yticks([45, 90, 135, 180, 225, 270, 315, 360])
                    # Converting Figure to an image:
                    img_buf6 = BytesIO()  # Create image object
                    plt.savefig(img_buf6, dpi=200, bbox_inches='tight')  # Save the image
                    # Gráfica de ráfaga del viento
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    plt.plot(day_df['Fecha'], day_df['Rafaga_viento_prom_kmh_dia'],  label="Promedio", color = 'orange')
                    plt.scatter(day_df['Fecha'], day_df['Rafaga_viento_max_kmh_dia'], label="Máximo", color = 'r')
                    plt.title('Ráfaga de viento', fontsize=10)
                    plt.ylabel('kmh', fontsize=10)
                    plt.xticks(day_df['Fecha'], day_df['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    plt.legend(loc="upper left")
                    # Setting the number of ticks
                    #plt.ylim(0, 360)
                    #plt.yticks([45, 90, 135, 180, 225, 270, 315, 360])
                    # Converting Figure to an image:
                    img_buf7 = BytesIO()  # Create image object
                    plt.savefig(img_buf7, dpi=200, bbox_inches='tight')  # Save the image
                    # Gráfica de radiación solar
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    plt.plot(day_df['Fecha'], day_df['Solar_rad_acum_dia_kwm2d'],  label="Acumulado", color = 'yellow')
                    #plt.bar(dfinal['Fecha'], dfinal['UV_index_max'], label="Máximo", color = 'purple')
                    plt.title('Radiación solar', fontsize=10)
                    plt.ylabel('kwm2/día', fontsize=10)
                    plt.xticks(day_df['Fecha'], day_df['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    plt.legend(loc="upper left")
                    # Setting the number of ticks
                    #plt.ylim(0, 360)
                    #plt.yticks([45, 90, 135, 180, 225, 270, 315, 360])
                    # Converting Figure to an image:
                    img_buf8 = BytesIO()  # Create image object
                    plt.savefig(img_buf8, dpi=200, bbox_inches='tight')  # Save the image
                    # Gráfica de radiación UV
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    #plt.plot(dfinal['Fecha'], dfinal['Solar_rad_prom_wm2'],  label="Promedio", color = 'yellow')
                    plt.bar(day_df['Fecha'], day_df['UV_index_max_dia'], label="Máximo", color = 'purple')
                    plt.title('Radiación UV', fontsize=10)
                    plt.ylabel('Index', fontsize=10)
                    plt.xticks(day_df['Fecha'], day_df['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    plt.legend(loc="upper left")
                    # Setting the number of ticks
                    #plt.ylim(0, 360)
                    #plt.yticks([45, 90, 135, 180, 225, 270, 315, 360])
                    # Converting Figure to an image:
                    img_buf9 = BytesIO()  # Create image object
                    plt.savefig(img_buf9, dpi=200, bbox_inches='tight')  # Save the image
                    # Gráfica de Evapotranspiración
                    plt.figure(figsize=(12, 2))  # Create a new figure object
                    plt.bar(day_df['Fecha'], day_df['Eto_acum_dia_mm'],  label="line1", color = 'b')
                    #plt.plot(dfinal['Fecha'], dfinal['Tmax_celsius'], label="line2", color = 'r')
                    plt.title('Evapotranspiración', fontsize=10)
                    plt.ylabel('mm', fontsize=10)
                    plt.xticks(day_df['Fecha'], day_df['Fecha'], rotation=r, size=s)
                    plt.yticks( size=10)
                    plt.ylim(0, 12)
                    # Converting Figure to an image:
                    img_buf10 = BytesIO()  # Create image object
                    plt.savefig(img_buf10, dpi=200, bbox_inches='tight')  # Save the image
            
                    plt.close('all')
                    
                    station = data[data['NOMBRE']==value].reset_index()['ID'][0]
                    lat = round(data[data['NOMBRE']==value].reset_index()['LAT'][0],2)
                    lon = round(data[data['NOMBRE']==value].reset_index()['LON'][0],2)
                    ciudad = data[data['NOMBRE']==value].reset_index()['CIUDAD'][0]
                    depto = data[data['NOMBRE']==value].reset_index()['DEPTO'][0]
                    pais = data[data['NOMBRE']==value].reset_index()['PAIS'][0]
                    
                    class PDF(FPDF):
                        def __init__(self):
                            super().__init__()
                        def header(self):
                            self.set_font('Arial', '', 12)
                            pdf.image(MA_LOGO, x=40, y=12.5, w=12, h=10)
                            self.cell(0, 15, f'Meteoagro DataNow - Resumen diario para el período {start_date} a {end_date}',align='C', border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                            pdf.ln(5)
                        def footer(self):
                            self.set_y(-15)
                            self.set_font('Arial', '', 12)
                            self.cell(0, 10, 'Meteoagro DataNow - 2022 - Todos los derechos reservados',align='C', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
                            
                    ch = 7
                    w1= 8
                    pdf = PDF() # Instance of custom class
                    pdf.add_page(orientation = 'L')
                    pdf.set_font('Helvetica', '', 10)
                    pdf.multi_cell(0, 10, f'ID Estación: {station}       Nombre: {value}        Ubicación: {ciudad}-{depto}-{pais}      Latitud: {lat}  Longitud: {lon} ',
                                border=1, align='C')
                    # Table Header
                    pdf.set_font('Arial', 'B', 6)
                    pdf.ln(5)
                    pdf.cell(w=22, h=14, txt='Fecha', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    #pdf.cell(w=18, h=14, txt='ID Estación', border=1, ln=0, align='C')
                    pdf.cell(w=24, h=ch, txt='Temperatura (°C)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=24, h=ch, txt='Humedad Relativa (%)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=24, h=ch, txt='Presión del aire (hpa)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    #pdf.cell(w=21, h=ch, txt='Precipitación (mm)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=21, h=ch, txt='Precipitación (mm)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='Dirección Viento', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='Velocidad Viento', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='Velocidad Viento', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='Ráfaga Viento', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='Ráfaga Viento', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='Radiacion Solar', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=15, h=ch, txt='UV Index', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='ETo (mm)', border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
                    pdf.cell(w=22, h=ch, txt='', border=0, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    #pdf.cell(w=18, h=ch, txt='', border=0, ln=0, align='C')
                    pdf.cell(w=w1, h=ch, txt='prom', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=w1, h=ch, txt='min', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=w1, h=ch, txt='max', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=w1, h=ch, txt='prom', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=w1, h=ch, txt='min', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=w1, h=ch, txt='max', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=w1, h=ch, txt='prom', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=w1, h=ch, txt='min', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=w1, h=ch, txt='max', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    #pdf.cell(w=21, h=ch, txt='acumulado horario', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=21, h=ch, txt='acumulado diario', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='promedio (°)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='promedio (kmh)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='máximo (kmh)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='promedio (kmh)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='máximo (kmh)', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='kwm2 día', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=15, h=ch, txt='max día', border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                    pdf.cell(w=18, h=ch, txt='acum diario', border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
                    # Table contents
                    pdf.set_font('Arial', '', 7)
                    for i in range(0, len(day_df)):
                        pdf.cell(w=22, h=ch, 
                                txt=day_df['Fecha'].iloc[i], 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=w1, h=ch, 
                                txt=day_df['Tprom_celsius_dia'].iloc[i].astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=w1, h=ch, 
                                txt=day_df['Tmin_celsius_dia'].iloc[i].astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=w1, h=ch, 
                                txt=day_df['Tmax_celsius_dia'].iloc[i].astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=w1, h=ch, 
                                txt=day_df['Hum_Rel_prom_%_dia'].iloc[i].astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=w1, h=ch, 
                                txt=day_df['Hum_Rel_min_%_dia'].iloc[i].astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=w1, h=ch, 
                                txt=day_df['Hum_Rel_max_%_dia'].iloc[i].astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=w1, h=ch, 
                                txt=day_df['Presion_abs_prom_hpa_dia'].iloc[i].astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=w1, h=ch, 
                                txt=day_df['Presion_abs_min_hpa_dia'].iloc[i].astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=w1, h=ch, 
                                txt=day_df['Presion_abs_max_hpa_dia'].iloc[i].astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        #pdf.cell(w=21, h=ch, 
                                #txt=round(day_df['Precip_hora_mm'].iloc[i],1).astype(str), 
                                #border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=21, h=ch, 
                                txt=round(day_df['Precip_acum_dia_mm'].iloc[i],1).astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=18, h=ch, 
                                txt=round(day_df['Dir_viento_prom_dia_grados'].iloc[i],1).astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=18, h=ch, 
                                txt=round(day_df['Vel_viento_prom_kmh_dia'].iloc[i],1).astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=18, h=ch, 
                                txt=round(day_df['Vel_viento_max_kmh_dia'].iloc[i],1).astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=18, h=ch, 
                                txt=round(day_df['Rafaga_viento_prom_kmh_dia'].iloc[i],1).astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=18, h=ch, 
                                txt=round(day_df['Rafaga_viento_max_kmh_dia'].iloc[i],1).astype(str), 
                                border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=18, h=ch, 
                                txt=round(day_df['Solar_rad_acum_dia_kwm2d'].iloc[i],1).astype(str), 
                                border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=15, h=ch, 
                                txt=round(day_df['UV_index_max_dia'].iloc[i],1).astype(str), 
                                border=1,  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
                        pdf.cell(w=18, h=ch, 
                                txt=round(day_df['Eto_acum_dia_mm'].iloc[i],1).astype(str), 
                                border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
                    pdf.ln(5)
                    pdf.set_font('Arial', 'B', 12)
                    pdf.cell(0, 10, 'Gráficas de los datos', 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
                    pdf.image(img_buf1,w=pdf.epw,h=50) # Make the image full width
                    pdf.ln(5)
                    pdf.image(img_buf2,w=pdf.epw,h=50)
                    pdf.ln(5)
                    pdf.image(img_buf3,w=pdf.epw,h=50)
                    pdf.ln(5)
                    pdf.image(img_buf4,w=pdf.epw,h=50) # Make the image full width
                    pdf.ln(5)
                    pdf.image(img_buf5,w=pdf.epw,h=50) # Make the image full width
                    pdf.ln(5)
                    pdf.image(img_buf6,w=pdf.epw,h=50) # Make the image full 
                    pdf.ln(5)
                    pdf.image(img_buf7,w=pdf.epw,h=50) # Make the image full width
                    pdf.ln(5)
                    pdf.image(img_buf8,w=pdf.epw,h=50) # Make the image full width
                    pdf.ln(5)
                    pdf.image(img_buf9,w=pdf.epw,h=50) # Make the image full width
                    pdf.ln(5)
                    pdf.image(img_buf10,w=pdf.epw,h=50) # Make the image full width
                    return pdf
                
                def write_pdf(bytes_io):
                    pdf = create_pdf(n_clicks) # pass argument to PDF creation here
                    bytes_io.write(pdf.output())

                return dcc.send_bytes(write_pdf, f'{station}_{start_date}_{end_date}.pdf')
            

    #if __name__ == "__main__":
    #    app.run_server()
