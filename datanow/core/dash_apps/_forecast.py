import dash
from dash import html, Input, Output, dcc, State
import dash_bootstrap_components as dbc
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, date
import statistics as st
import base64
from io import BytesIO
from ast import literal_eval
from django_plotly_dash import DjangoDash


data = pd.read_csv("core/dash_apps/estaciones_mtgnet.csv", sep=';')
#api_key = 'UV5tO4P3w5hiLGRWYrhCn0PpTL6B3EaI'
api_key = 'YGsX7rhgvfFxiX5ymm6hkvQg6hNxt6r2'

app = DjangoDash('_forecast', external_stylesheets=[dbc.themes.BOOTSTRAP])

def encode_image(image_url):
    buffered = BytesIO(requests.get(image_url).content)
    image_base64 = base64.b64encode(buffered.getvalue())
    return b'data:image/png;base64,' + image_base64

img1 = (encode_image('https://developer.accuweather.com/sites/default/files/01-s.png')).decode()
img2 = (encode_image('https://developer.accuweather.com/sites/default/files/02-s.png')).decode()
img3 = (encode_image('https://developer.accuweather.com/sites/default/files/03-s.png')).decode()
img4 = (encode_image('https://developer.accuweather.com/sites/default/files/04-s.png')).decode()
img5 = (encode_image('https://developer.accuweather.com/sites/default/files/05-s.png')).decode()
img6 = (encode_image('https://developer.accuweather.com/sites/default/files/06-s.png')).decode()
img7 = (encode_image('https://developer.accuweather.com/sites/default/files/07-s.png')).decode()
img8 = (encode_image('https://developer.accuweather.com/sites/default/files/08-s.png')).decode()
#img9 = (encode_image('')
#img10 = (encode_image('')
img11 = (encode_image('https://developer.accuweather.com/sites/default/files/11-s.png')).decode()
img12 = (encode_image('https://developer.accuweather.com/sites/default/files/12-s.png')).decode()
img13 = (encode_image('https://developer.accuweather.com/sites/default/files/13-s.png')).decode()
img14 = (encode_image('https://developer.accuweather.com/sites/default/files/14-s.png')).decode()                           
img15 = (encode_image('https://developer.accuweather.com/sites/default/files/15-s.png')).decode()
img16 = (encode_image('https://developer.accuweather.com/sites/default/files/16-s.png')).decode()
img17 = (encode_image('https://developer.accuweather.com/sites/default/files/17-s.png')).decode()
img18 = (encode_image('https://developer.accuweather.com/sites/default/files/18-s.png')).decode()
img19 = (encode_image('https://developer.accuweather.com/sites/default/files/19-s.png')).decode()
img20 = (encode_image('https://developer.accuweather.com/sites/default/files/20-s.png')).decode()
img21 = (encode_image('https://developer.accuweather.com/sites/default/files/21-s.png')).decode()
img22 = (encode_image('https://developer.accuweather.com/sites/default/files/22-s.png')).decode()
img23 = (encode_image('https://developer.accuweather.com/sites/default/files/23-s.png')).decode()
img24 = (encode_image('https://developer.accuweather.com/sites/default/files/24-s.png')).decode()
img25 = (encode_image('https://developer.accuweather.com/sites/default/files/25-s.png')).decode()
img26 = (encode_image('https://developer.accuweather.com/sites/default/files/26-s.png')).decode()
#img27 = (encode_image('')
#img28 = (encode_image('')
img29 = (encode_image('https://developer.accuweather.com/sites/default/files/29-s.png')).decode()
img30 = (encode_image('https://developer.accuweather.com/sites/default/files/30-s.png')).decode()
img31 = (encode_image('https://developer.accuweather.com/sites/default/files/31-s.png')).decode()
img32 = (encode_image('https://developer.accuweather.com/sites/default/files/32-s.png')).decode()
img33 = (encode_image('https://developer.accuweather.com/sites/default/files/33-s.png')).decode()
img34 = (encode_image('https://developer.accuweather.com/sites/default/files/34-s.png')).decode()
img35 = (encode_image('https://developer.accuweather.com/sites/default/files/35-s.png')).decode()
img36 = (encode_image('https://developer.accuweather.com/sites/default/files/36-s.png')).decode()
img37 = (encode_image('https://developer.accuweather.com/sites/default/files/37-s.png')).decode()
img38 = (encode_image('https://developer.accuweather.com/sites/default/files/38-s.png')).decode()
img39 = (encode_image('https://developer.accuweather.com/sites/default/files/39-s.png')).decode()
img40 = (encode_image('https://developer.accuweather.com/sites/default/files/40-s.png')).decode()
img41 = (encode_image('https://developer.accuweather.com/sites/default/files/41-s.png')).decode()
img42 = (encode_image('https://developer.accuweather.com/sites/default/files/42-s.png')).decode()
img43 = (encode_image('https://developer.accuweather.com/sites/default/files/43-s.png')).decode()
img44 = (encode_image('https://developer.accuweather.com/sites/default/files/44-s.png')).decode()

def icon(icon):
    i = icon
    locals()[i] = icon
    return icon

card_content_dropdwn = [
    dbc.CardBody(
        [
            html.H6('Consulta por ciudad/lugar o por coordenadas', style = {'textAlign':'center'}),
            
            dbc.Row([                
                dbc.Col([
                dcc.Input(id = 'input_lugar',
                          type = 'text',
                          placeholder = 'Ciudad o lugar',
                          value = '',
                          debounce = True
                          ),
                dcc.Input(id = 'input_lat',
                          type = 'text',
                          placeholder = 'Latitud',
                          value = '',
                          debounce = True
                          ),
                dcc.Input(id = 'input_lon',
                          type = 'text',
                          placeholder = 'Longitud',
                          value = '',
                          debounce = True
                          ),
                
                html.Button(id='submit-button-state', n_clicks=0, children='Consultar')
                ], style = {'width':'100', 'display':'inline-block'}) 
                ]),
            
            html.Br(),
            
            ]
        
        )
    
    ]

card_content_dropdwn1 = [
    dbc.CardBody(
        [
            html.H6('Consulta por  estación', style = {'textAlign':'center'}),
            
            dbc.Row([
                
                dbc.Col([
                    #html.H6('Current Period'),
                    
                    dcc.Dropdown(id= 'station-dropdown',
                                 options = [{'label':i,'value':i} for i in data['ID'].unique()],
                                 value = '',
                                 placeholder = 'Selecione la estación a consultar',
                                 ),
                    
                    ], style = {'width':'100', 'display':'inline-block'}),
                
                 
                
                
                ]),
            
            html.Br(),
            
            ]
        
        
        
        )
    
    
    ]


body_app = dbc.Container([
    
    
    dbc.Row(html.H2('PRONÓSTICO A 5 DÍAS'), style={'color':'#4e73df', 'text-align':'center','fontfamily':'Montserrat'}),
    
    html.Br(),
    
    dbc.Row([
            dbc.Col([dbc.Card(card_content_dropdwn, style={'height':'100px'})], width = '60%'),        
        ]),
    
    html.Br(),
    
    dbc.Row([
            dbc.Col([dbc.Card(card_content_dropdwn1, style={'height':'100px'})], width = '60%'),        
        ]),
    
    html.Br(),
    
    dbc.Row([
            dbc.Col([dbc.Card(id = 'card_num14', style={'height':'80px'})]),
        ]),
    
    html.Br(),
    
    dbc.Row([
            dbc.Col([dbc.Card(id = 'card_num1', style={'height':'710px'})]),
            dbc.Col([dbc.Card(id = 'card_num2', style={'height':'710px'})]),
            dbc.Col(dcc.Loading(children=[dbc.Card(id = 'card_num3', style={'height':'710px'})], fullscreen=True)),
            dbc.Col([dbc.Card(id = 'card_num4', style={'height':'710px'})]),
            dbc.Col([dbc.Card(id = 'card_num5', style={'height':'710px'})])
            
        
        ]),
    
    html.Br(),
    
    dbc.Row([
            dbc.Col([dbc.Card(id = 'card_num6', style={'height':'470px'})]),
            dbc.Col([dbc.Card(id = 'card_num7', style={'height':'470px'})]),
            dbc.Col([dbc.Card(id = 'card_num8', style={'height':'470px'})]),
            dbc.Col([dbc.Card(id = 'card_num9', style={'height':'470px'})]),
            dbc.Col([dbc.Card(id = 'card_num10', style={'height':'470px'})])
            
        
        ]),
    
    html.Br(),
  
    dbc.Row(html.H4(f'GRÁFICAS DEL PRONÓSTICO'), style={'color':'#4e73df', 'text-align':'center'}),
    
    html.Br(),
    
    dbc.Row([
            dbc.Col([dbc.Card(id = 'card_num11', style={'height':'500px'})]),
            
        ]),
    
    html.Br(),
    
    dbc.Row([
            dbc.Col([dbc.Card(id = 'card_num12', style={'height':'500px'})]),
            
        ]),
    
    html.Br(),
    
    dbc.Row([
            dbc.Col([dbc.Card(id = 'card_num13', style={'height':'500px'})]),
            
        ]),
    
    html.Br(),
    
])
    

app.layout = html.Div([body_app])

@app.callback([Output('card_num1','children'),
               Output('card_num2','children'),
               Output('card_num3','children'),
               Output('card_num4','children'),
               Output('card_num5','children'),
               Output('card_num6','children'),
               Output('card_num7','children'),
               Output('card_num8','children'),
               Output('card_num9','children'),
               Output('card_num10','children'),
               Output('card_num11','children'),
               Output('card_num12','children'),
               Output('card_num13','children'),
               Output('card_num14','children')],
              [Input('station-dropdown','value'),
               Input('submit-button-state','n_clicks'),
               State('input_lugar', 'value'),
               State('input_lat', 'value'),
               State('input_lon', 'value'),
               ])

def update_cards(value, n_clicks, input_lugar, input_lat, input_lon):
    
    def key_loc():
     
        if input_lugar != '':
            url_lug = f'http://dataservice.accuweather.com/locations/v1/cities/autocomplete?apikey={api_key}&q={input_lugar}&language=es'
            response_lug = requests.request("GET", url_lug)
            if  str(response_lug) == '<Response [503]>':
                geo = 'Servicio No Disponible'
                city = None
                province = None
                country = None
            elif pd.DataFrame(response_lug.json()).columns[1] == 'Key':
                lug = pd.DataFrame(response_lug.json())
                geo = lug['Key'][0]
                city =  lug['LocalizedName'][0]
                province = lug['AdministrativeArea'][0]['LocalizedName']
                country = lug['Country'][0]['ID']
            else:
                geo = None
                city = None
                province = None
                country = None
               
        elif input_lat != '' and input_lon != '':
            geo_url = f'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={api_key}&q={input_lat}%2C{input_lon}&language=es&details=true&toplevel=false'
            response2 = requests.request("GET", geo_url)
            lug = list(response2.json())
            if list(response2.json())[1] == 'Key':
                geo = response2.json()['Key']
                city =  response2.json()['LocalizedName']
                province = response2.json()['AdministrativeArea']['LocalizedName']
                country = response2.json()['Country']['ID']
            elif list(response2.json())[0] == 'Code':
                geo = 'Servicio No Disponible'
                city = None
                province = None
                country = None
            else:
                geo = None
                city = None
                province = None
                country = None
            
        elif value != '':
            geo = data[data['ID']==value].reset_index()['ACCUW_KEY'][0]
            city = data[data['ID']==value].reset_index()['NOMBRE'][0]
            province = data[data['ID']==value].reset_index()['CIUDAD'][0]
            country = data[data['ID']==value].reset_index()['PAIS'][0]
        else: 
            geo = None
            city = None
            province = None
            country = None
            
        return geo, city, province, country
    
    location = key_loc()
    print(location)
    geo = location[0]
    city = location[1]
    province = location[2]
    country = location[3]
    
    if geo == 'Servicio No Disponible' or geo == None:
        
        card_content14 = [
            
            dbc.CardBody(
                [
                    dbc.Col(html.H4('Pronóstico para: {0}'.format(geo)), style = {'width':'100%','color':'#4e73df','textAlign':'center'}),
                    
                    
                    ]
                )
            
            ]
        
        card_content1 = [dbc.CardBody([])]
        card_content2 = [dbc.CardBody([])]
        card_content3 = [dbc.CardBody([])]
        card_content4 = [dbc.CardBody([])]
        card_content5 = [dbc.CardBody([])]
        card_content6 = [dbc.CardBody([])]
        card_content7 = [dbc.CardBody([])]
        card_content8 = [dbc.CardBody([])]
        card_content9 = [dbc.CardBody([])]
        card_content10 = [dbc.CardBody([])]
        card_content11 = [dbc.CardBody([])]
        card_content12 = [dbc.CardBody([])]
        card_content13 = [dbc.CardBody([])]
        
        return card_content1, card_content2, card_content3, card_content4, card_content5, card_content6, card_content7, card_content8, card_content9, card_content10,\
            card_content11, card_content12, card_content13, card_content14
        
    else:    
        url = f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{geo}?apikey={api_key}&language=es&details=true&metric=true'
        response = requests.request("GET", url)
        df=pd.DataFrame(response.json()['DailyForecasts']) 
        
        def tabla_pronostico(dataframe):
            
            dates = df['Date']
            dates = dates.str.slice(0,10)
            temp = df['Temperature']
            ster = df['RealFeelTemperature']
            sun = df['Sun']
            hsun = df['HoursOfSun']
            uv = df['AirAndPollen']
            dia = df['Day']
            noche = df['Night']
            tn = []
            tx = []
            stn = []
            stx = []
            sr = []
            ss = []
            uvr = []
            ic = []
            icp = []
            pty = []
            pi = []
            psp = []
            plp = []
            pp = []
            tp = []
            rp = []
            sp = []
            ip = []
            ws = []
            wd = []
            wdl = []
            wsg = []
            wdg = []
            wdlg = []
            pt = []
            rt = []
            sto = []
            it = []
            hp = []
            hr = []
            hs = []
            hi = []
            cc = []
            eto = []
            si = []
            nic = []
            nicp = []
            npty = []
            npi = []
            npsp = []
            nplp = []
            npp = []
            ntp = []
            nrp = []
            nsp = []
            nip = []
            nws = []
            nwd = []
            nwdl = []
            nwsg = []
            nwdg = []
            nwdlg = []
            npt = []
            nrt = []
            nst = []
            nit = []
            nhp = []
            nhr = []
            nhs = []
            nhi = []
            ncc = []
            for i, v in temp.items():
                t = temp[i]['Minimum']['Value']
                tn.append(t)
                t = temp[i]['Maximum']['Value']
                tx.append(t)
                t = ster[i]['Minimum']['Value']
                stn.append(t)
                t = ster[i]['Maximum']['Value']
                stx.append(t)
                t = sun[i]['Rise']
                sr.append(t)
                t = sun[i]['Set']
                ss.append(t)
                t = uv[i][5]['Value']
                uvr.append(t)
                t = dia[i]['Icon']
                ic.append(t)
                t = dia[i]['IconPhrase']
                icp.append(t)
                
                if dia[i]['HasPrecipitation'] == True:
                    t = dia[i]['PrecipitationType']
                    pty.append(t)
                    t = dia[i]['PrecipitationIntensity']
                    pi.append(t)
                else:
                    t = 'False'
                    pty.append(t)
                    pi.append(t)
                    
                t = dia[i]['ShortPhrase']
                psp.append(t)
                t = dia[i]['LongPhrase']
                plp.append(t)
                t = dia[i]['PrecipitationProbability']
                pp.append(t)
                t = dia[i]['ThunderstormProbability']
                tp.append(t)
                t = dia[i]['RainProbability']
                rp.append(t)
                t = dia[i]['SnowProbability']
                sp.append(t)
                t = dia[i]['IceProbability']
                ip.append(t)
                t = dia[i]['Wind']['Speed']['Value']
                ws.append(t)
                t = dia[i]['Wind']['Direction']['Degrees']
                wd.append(t)
                t = dia[i]['Wind']['Direction']['English']
                wdl.append(t)
                t = dia[i]['WindGust']['Speed']['Value']
                wsg.append(t)
                t = dia[i]['WindGust']['Direction']['Degrees']
                wdg.append(t)
                t = dia[i]['WindGust']['Direction']['English']
                wdlg.append(t)
                t = dia[i]['TotalLiquid']['Value']
                pt.append(t)
                t = dia[i]['Rain']['Value']
                rt.append(t)
                t = dia[i]['Snow']['Value']
                sto.append(t)
                t = dia[i]['Ice']['Value']
                it.append(t)
                t = float(dia[i]['HoursOfPrecipitation'])
                hp.append(t)
                t = float(dia[i]['HoursOfRain'])
                hr.append(t)
                t = float(dia[i]['HoursOfSnow'])
                hs.append(t)
                t = float(dia[i]['HoursOfIce'])
                hi.append(t)
                t = dia[i]['CloudCover']
                cc.append(t)
                t = dia[i]['Evapotranspiration']['Value']
                eto.append(t)
                t = dia[i]['SolarIrradiance']['Value']
                si.append(t)
                t = noche[i]['Icon']
                nic.append(t)
                t = noche[i]['IconPhrase']
                nicp.append(t)
                
                if noche[i]['HasPrecipitation'] == True:
                    t = noche[i]['PrecipitationType']
                    npty.append(t)
                    t = noche[i]['PrecipitationIntensity']
                    npi.append(t)
                else:
                    t = 'False'
                    npty.append(t)
                    t = 'False'
                    npi.append(t)
                    
                t = noche[i]['ShortPhrase']
                npsp.append(t)
                t = noche[i]['LongPhrase']
                nplp.append(t)
                t = noche[i]['PrecipitationProbability']
                npp.append(t)
                t = noche[i]['ThunderstormProbability']
                ntp.append(t)
                t = noche[i]['RainProbability']
                nrp.append(t)
                t = noche[i]['SnowProbability']
                nsp.append(t)
                t = noche[i]['IceProbability']
                nip.append(t)
                t = noche[i]['Wind']['Speed']['Value']
                nws.append(t)
                t = noche[i]['Wind']['Direction']['Degrees']
                nwd.append(t)
                t = noche[i]['Wind']['Direction']['English']
                nwdl.append(t)
                t = noche[i]['WindGust']['Speed']['Value']
                nwsg.append(t)
                t = noche[i]['WindGust']['Direction']['Degrees']
                nwdg.append(t)
                t = noche[i]['WindGust']['Direction']['English']
                nwdlg.append(t)
                t = noche[i]['TotalLiquid']['Value']
                npt.append(t)
                t = noche[i]['Rain']['Value']
                nrt.append(t)
                t = noche[i]['Snow']['Value']
                nst.append(t)
                t = noche[i]['Ice']['Value']
                nit.append(t)
                t = float(noche[i]['HoursOfPrecipitation'])
                nhp.append(t)
                t = float(noche[i]['HoursOfRain'])
                nhr.append(t)
                t = float(noche[i]['HoursOfSnow'])
                nhs.append(t)
                t = float(noche[i]['HoursOfIce'])
                nhi.append(t)
                t = noche[i]['CloudCover']
                ncc.append(t)
                  
            df_pron = pd.concat([dates, pd.DataFrame(tn),
                             pd.DataFrame(tx), pd.DataFrame(stn), pd.DataFrame(stx),
                             pd.DataFrame(sr), pd.DataFrame(ss), pd.DataFrame(hsun),
                             pd.DataFrame(uvr), pd.DataFrame(ic), pd.DataFrame(icp),
                             pd.DataFrame(pty), pd.DataFrame(pi), pd.DataFrame(psp), pd.DataFrame(plp),
                             pd.DataFrame(pp), pd.DataFrame(tp), pd.DataFrame(rp),
                             pd.DataFrame(sp), pd.DataFrame(ip), pd.DataFrame(ws),
                             pd.DataFrame(wd), pd.DataFrame(wdl), pd.DataFrame(wsg),
                             pd.DataFrame(wdg), pd.DataFrame(wdlg), pd.DataFrame(pt),
                             pd.DataFrame(rt), pd.DataFrame(sto), pd.DataFrame(it),
                             pd.DataFrame(hp), pd.DataFrame(hr), pd.DataFrame(hs),
                             pd.DataFrame(hi), pd.DataFrame(cc), pd.DataFrame(eto),
                             pd.DataFrame(si), pd.DataFrame(nic), pd.DataFrame(nicp),
                             pd.DataFrame(npty), pd.DataFrame(npi), pd.DataFrame(npsp), pd.DataFrame(nplp),
                             pd.DataFrame(npp), pd.DataFrame(ntp), pd.DataFrame(nrp),
                             pd.DataFrame(nsp), pd.DataFrame(nip), pd.DataFrame(nws),
                             pd.DataFrame(nwd), pd.DataFrame(nwdl), pd.DataFrame(nwsg),
                             pd.DataFrame(nwdg), pd.DataFrame(nwdlg), pd.DataFrame(npt),
                             pd.DataFrame(nrt), pd.DataFrame(nst), pd.DataFrame(nit),
                             pd.DataFrame(nhp), pd.DataFrame(nhr), pd.DataFrame(nhs),
                             pd.DataFrame(nhi), pd.DataFrame(ncc)], axis="columns")
                 
            df_pron.columns = ['Date', 'Tn','Tx','SensacionTmin','SensacionTmax',
                           'Sunrise','Sunset','HoursSun','UV','Dia_icon','Dia_Icon_Frase',
                           'PrecType','PrecIntensity','ShortPhrase','LongPhrase','PrecProb','ThunderProb',
                           'RainProb','SnowProb','IceProb','WindSpeed','WindDirection',
                           'WindDirectionL','WindGustSpeed', 'WindGustDirection',
                           'WindGustDirectionL','TotalLiquid','Rain','Snow','Ice','HoursOfPrec',
                           'HoursOfRain','HoursOfSnow','HoursOfIce','CloudCover','Eto','SolarIrradiance',
                           'Noche_icon','Noche_Icon_Frase','NPrecType','NPrecIntensity','NShortPhrase','NLongPhrase',
                           'NPrecProb','NThunderProb','NRainProb','NSnowProb','NIceProb','NWindSpeed',
                           'NWindDirection','NWindDirectionL','NWindGustSpeed', 'NWindGustDirection',
                           'NWindGustDirectionL','NTotalLiquid','NRain','NSnow','NIce','NHoursOfPrec',
                           'NHoursOfRain','NHoursOfSnow','NHoursOfIce','NCloudCover']
            df_pron['Sunrise'] = df_pron['Sunrise'].str.slice(11,16)
            df_pron['Sunset'] = df_pron['Sunset'].str.slice(11,16)
            
            return df_pron
    
        d = tabla_pronostico(df)
        d['Dia_icon2'] = 'img' + d['Dia_icon'].astype(str)
        d['Noche_icon2'] = 'img' + d['Noche_icon'].astype(str)
        d['Prec_Dia'] = d['TotalLiquid'] + d['NTotalLiquid']
        d['Solar_MJ'] = (d['SolarIrradiance'] * 0.001 * 3.6)
        
        fig = go.Figure(data = [go.Scatter(x=d['Date'], y = d['Tx'],
                                           line=dict(color='#e4605e', width=2),
                                           #text='{0}{1}'.format(d['Tx'],' °C'), 
                                           name='Temperatura máxima del aire °C',
                                           ),
                                go.Scatter(x=d['Date'], y = d['Tn'],
                                           line=dict(color='#1e90ff', width=2),
                                           #text='{0}{1}'.format(d['Tn'],' °C'), 
                                           name='Temperatura mínima del aire °C',
                                           )
                                ])
        fig.update_layout(title='Temperatura máxima y mínima pronosticada',
                          xaxis_title = 'día/hora',
                          yaxis_title = '°C',
                          plot_bgcolor = 'white',
                          margin=dict(l = 20, r = 5, t = 30, b = 20)
                          )
        
        fig2 = go.Figure([go.Bar(x=d['Date'], 
                                 y = d['Prec_Dia'], 
                                 marker_color = '#4682b4', 
                                 name = 'Precipitación mm/día'),
                          go.Bar(x=d['Date'], 
                                 y = d['Eto'], 
                                 marker_color = '#e4605e', 
                                 name = 'Evapotransporación mm/día')
                         ])
        fig2.update_layout(title='Cantidades esperadas de precipitación y evapotranspiración',
                          xaxis_title = 'día/hora',
                          yaxis_title = 'mm',
                          plot_bgcolor = 'white',
                          margin=dict(l = 40, r = 5, t = 60, b = 40),
                          barmode = 'group'
                          )
        
        fig3 = go.Figure([go.Bar(x=d['Date'], 
                                 y = d['Solar_MJ'], 
                                 marker_color = '#f4d03f', 
                                 name = 'Radiación Solar MJ/m2/día'),
                          go.Bar(x=d['Date'], 
                                 y = d['UV'], 
                                 marker_color = '#9b59b6', 
                                 name = 'Radiación UV Index')
                         ])
        fig3.update_layout(title='Radiación solar y UV',
                          xaxis_title = 'día/hora',
                          yaxis_title = 'MJ/m2/día',
                          plot_bgcolor = 'white',
                          margin=dict(l = 40, r = 5, t = 60, b = 40),
                          barmode = 'group'
                          )
        
        card_content14 = [
            
            dbc.CardBody(
                [
                    dbc.Col(html.H4('Pronóstico para: {0}, {1}, {2}'.format(city,province,country)), style = {'width':'100%','color':'#1a5276','textAlign':'center'}),
                    
                    
                    ]
                )
            
            ]
        
        card_content1 = [
            
            dbc.CardBody(
                [
                    html.H6(d['Date'][0], style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Col(html.H5('Día'), style = {'width':'50%','color':'#2471a3','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H5('Noche'), style = {'width':'50%','color':'#34495e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.Img(src=eval(d['Dia_icon2'][0])), style = {'width':'50%','color':'red','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.Img(src=eval(d['Noche_icon2'][0])), style = {'width':'50%','color':'red','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.P(d['ShortPhrase'][0]), style = {'width':'50%','color':'#212f3c','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.P(d['NShortPhrase'][0]), style = {'width':'50%','color':'#212f3c','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['PrecProb'][0]," %")), style = {'width':'50%','color':'#1a5276','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NPrecProb'][0]," %")), style = {'width':'50%','color':'#1a5276','textAlign':'center','display':'inline-block'}),
                    html.H6('Probabilidad de lluvia', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['CloudCover'][0],' %')), style = {'width':'50%','color':'darkgrey','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NCloudCover'][0],' %')), style = {'width':'50%','color':'darkgrey','textAlign':'center','display':'inline-block'}),
                    html.H6('Cobertura de nubes', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindSpeed'][0],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindSpeed'][0],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindDirectionL'][0],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindDirectionL'][0],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    html.H6('Velocidad del viento (kmh)', style = {"fontWeight":"lighter","textAlign":"center"}),
                    html.H6('Dirección del viento', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindGustSpeed'][0],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindGustSpeed'][0],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindGustDirectionL'][0],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindGustDirectionL'][0],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    html.H6('Ráfaga del viento (kmh)', style = {"fontWeight":"lighter","textAlign":"center"}),
                    html.H6('Dirección de ráfaga', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    
                    ]
                )
            
            ]
        
        card_content2 = [
            
            dbc.CardBody(
                [
                    html.H6(d['Date'][1], style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Col(html.H5('Día'), style = {'width':'50%','color':'#2471a3','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H5('Noche'), style = {'width':'50%','color':'#34495e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.Img(src=eval(d['Dia_icon2'][1])), style = {'width':'50%','color':'red','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.Img(src=eval(d['Noche_icon2'][1])), style = {'width':'50%','color':'red','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.P(d['ShortPhrase'][1]), style = {'width':'50%','color':'#212f3c','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.P(d['NShortPhrase'][1]), style = {'width':'50%','color':'#212f3c','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['PrecProb'][1]," %")), style = {'width':'50%','color':'#1a5276','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NPrecProb'][1]," %")), style = {'width':'50%','color':'#1a5276','textAlign':'center','display':'inline-block'}),
                    html.H6('Probabilidad de lluvia', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['CloudCover'][1],' %')), style = {'width':'50%','color':'darkgrey','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NCloudCover'][1],' %')), style = {'width':'50%','color':'darkgrey','textAlign':'center','display':'inline-block'}),
                    html.H6('Cobertura de nubes', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindSpeed'][1],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindSpeed'][1],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindDirectionL'][1],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindDirectionL'][1],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    html.H6('Velocidad del viento (kmh)', style = {"fontWeight":"lighter","textAlign":"center"}),
                    html.H6('Dirección del viento', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindGustSpeed'][1],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindGustSpeed'][1],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindGustDirectionL'][1],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindGustDirectionL'][1],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    html.H6('Ráfaga del viento (kmh)', style = {"fontWeight":"lighter","textAlign":"center"}),
                    html.H6('Dirección de ráfaga', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    ]
                )
            
            ]
        
        card_content3 = [
            
            dbc.CardBody(
                [
                    html.H6(d['Date'][2], style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Col(html.H5('Día'), style = {'width':'50%','color':'#2471a3','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H5('Noche'), style = {'width':'50%','color':'#34495e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.Img(src=eval(d['Dia_icon2'][2])), style = {'width':'50%','color':'red','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.Img(src=eval(d['Noche_icon2'][2])), style = {'width':'50%','color':'red','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.P(d['ShortPhrase'][2]), style = {'width':'50%','color':'#212f3c','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.P(d['NShortPhrase'][2]), style = {'width':'50%','color':'#212f3c','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['PrecProb'][2]," %")), style = {'width':'50%','color':'#1a5276','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NPrecProb'][2]," %")), style = {'width':'50%','color':'#1a5276','textAlign':'center','display':'inline-block'}),
                    html.H6('Probabilidad de lluvia', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['CloudCover'][2],' %')), style = {'width':'50%','color':'darkgrey','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NCloudCover'][2],' %')), style = {'width':'50%','color':'darkgrey','textAlign':'center','display':'inline-block'}),
                    html.H6('Cobertura de nubes', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindSpeed'][2],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindSpeed'][2],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindDirectionL'][2],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindDirectionL'][2],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    html.H6('Velocidad del viento (kmh)', style = {"fontWeight":"lighter","textAlign":"center"}),
                    html.H6('Dirección del viento', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindGustSpeed'][2],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindGustSpeed'][2],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindGustDirectionL'][2],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindGustDirectionL'][2],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    html.H6('Ráfaga del viento (kmh)', style = {"fontWeight":"lighter","textAlign":"center"}),
                    html.H6('Dirección de ráfaga', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    ]
                )
            
            ]
        
        card_content4 = [
            
            dbc.CardBody(
                [
                    html.H6(d['Date'][3], style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Col(html.H5('Día'), style = {'width':'50%','color':'#2471a3','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H5('Noche'), style = {'width':'50%','color':'#34495e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.Img(src=eval(d['Dia_icon2'][3])), style = {'width':'50%','color':'red','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.Img(src=eval(d['Noche_icon2'][3])), style = {'width':'50%','color':'red','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.P(d['ShortPhrase'][3]), style = {'width':'50%','color':'#212f3c','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.P(d['NShortPhrase'][3]), style = {'width':'50%','color':'#212f3c','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['PrecProb'][3]," %")), style = {'width':'50%','color':'#1a5276','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NPrecProb'][3]," %")), style = {'width':'50%','color':'#1a5276','textAlign':'center','display':'inline-block'}),
                    html.H6('Probabilidad de lluvia', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['CloudCover'][3],' %')), style = {'width':'50%','color':'darkgrey','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NCloudCover'][3],' %')), style = {'width':'50%','color':'darkgrey','textAlign':'center','display':'inline-block'}),
                    html.H6('Cobertura de nubes', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindSpeed'][3],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindSpeed'][3],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindDirectionL'][3],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindDirectionL'][3],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    html.H6('Velocidad del viento (kmh)', style = {"fontWeight":"lighter","textAlign":"center"}),
                    html.H6('Dirección del viento', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindGustSpeed'][3],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindGustSpeed'][3],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindGustDirectionL'][3],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindGustDirectionL'][3],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    html.H6('Ráfaga del viento (kmh)', style = {"fontWeight":"lighter","textAlign":"center"}),
                    html.H6('Dirección de ráfaga', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    ]
                )
            
            ]
        
        card_content5 = [
            
            dbc.CardBody(
                [
                    html.H6(d['Date'][4], style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Col(html.H5('Día'), style = {'width':'50%','color':'#2471a3','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H5('Noche'), style = {'width':'50%','color':'#34495e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.Img(src=eval(d['Dia_icon2'][4])), style = {'width':'50%','color':'red','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.Img(src=eval(d['Noche_icon2'][4])), style = {'width':'50%','color':'red','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.P(d['ShortPhrase'][4]), style = {'width':'50%','color':'#212f3c','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.P(d['NShortPhrase'][4]), style = {'width':'50%','color':'#212f3c','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['PrecProb'][4]," %")), style = {'width':'50%','color':'#1a5276','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NPrecProb'][4]," %")), style = {'width':'50%','color':'#1a5276','textAlign':'center','display':'inline-block'}),
                    html.H6('Probabilidad de lluvia', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['CloudCover'][4],' %')), style = {'width':'50%','color':'darkgrey','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NCloudCover'][4],' %')), style = {'width':'50%','color':'darkgrey','textAlign':'center','display':'inline-block'}),
                    html.H6('Cobertura de nubes', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindSpeed'][4],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindSpeed'][4],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindDirectionL'][4],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindDirectionL'][4],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    html.H6('Velocidad del viento (kmh)', style = {"fontWeight":"lighter","textAlign":"center"}),
                    html.H6('Dirección del viento', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindGustSpeed'][4],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindGustSpeed'][4],'')), style = {'width':'50%','color':'darker','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['WindGustDirectionL'][4],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4('{0}{1}'.format(d['NWindGustDirectionL'][4],'')), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    html.H6('Ráfaga del viento (kmh)', style = {"fontWeight":"lighter","textAlign":"center"}),
                    html.H6('Dirección de ráfaga', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                        
                    ]
                )
            
            ]
    
        
        card_content6 = [
            
            dbc.CardBody(
                [ 
                    dbc.Col(html.H4(d['Tn'][0]), style = {'width':'50%','color':'#21618c','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4(d['Tx'][0]), style = {'width':'50%','color':'#922b21','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Temperatura min', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Temperatura max', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4(d['SensacionTmin'][0]), style = {'width':'50%','color':'#21618c','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4(d['SensacionTmax'][0]), style = {'width':'50%','color':'#922b21','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Sensación min', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Sensación max', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['Eto'][0]," mm")), style = {'width':'100%','color':'#b03a2e','textAlign':'center','display':'inline-block'}),
                    html.H6('Evapotranspiración', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4(d['HoursSun'][0]), style = {'width':'50%','color':'red','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4(d['UV'][0]), style = {'width':'50%','color':'#884ea0','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Horas de Sol', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('UV Index', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H6(d['Sunrise'][0]), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6(d['Sunset'][0]), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Amanecer', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Puesta del sol', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    ]
                )
            
            ]
        
        card_content7 = [
            
            dbc.CardBody(
                [
                    dbc.Col(html.H4(d['Tn'][1]), style = {'width':'50%','color':'#21618c','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4(d['Tx'][1]), style = {'width':'50%','color':'#922b21','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Temperatura min', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Temperatura max', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4(d['SensacionTmin'][1]), style = {'width':'50%','color':'#21618c','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4(d['SensacionTmax'][1]), style = {'width':'50%','color':'#922b21','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Sensación min', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Sensación max', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['Eto'][1]," mm")), style = {'width':'100%','color':'#b03a2e','textAlign':'center','display':'inline-block'}),
                    html.H6('Evapotranspiración', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4(d['HoursSun'][1]), style = {'width':'50%','color':'red','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4(d['UV'][1]), style = {'width':'50%','color':'#884ea0','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Horas de Sol', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('UV Index', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H6(d['Sunrise'][1]), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6(d['Sunset'][1]), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Amanecer', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Puesta del sol', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    ]
                )
            
            ]
        
        card_content8 = [
            
            dbc.CardBody(
                [
                    dbc.Col(html.H4(d['Tn'][2]), style = {'width':'50%','color':'#21618c','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4(d['Tx'][2]), style = {'width':'50%','color':'#922b21','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Temperatura min', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Temperatura max', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4(d['SensacionTmin'][2]), style = {'width':'50%','color':'#21618c','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4(d['SensacionTmax'][2]), style = {'width':'50%','color':'#922b21','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Sensación min', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Sensación max', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['Eto'][2]," mm")), style = {'width':'100%','color':'#b03a2e','textAlign':'center','display':'inline-block'}),
                    html.H6('Evapotranspiración', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4(d['HoursSun'][2]), style = {'width':'50%','color':'red','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4(d['UV'][2]), style = {'width':'50%','color':'#884ea0','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Horas de Sol', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('UV Index', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H6(d['Sunrise'][2]), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6(d['Sunset'][2]), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Amanecer', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Puesta del sol', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    ]
                )
            
            ]
        
        card_content9 = [
            
            dbc.CardBody(
                [
                    dbc.Col(html.H4(d['Tn'][3]), style = {'width':'50%','color':'#21618c','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4(d['Tx'][3]), style = {'width':'50%','color':'#922b21','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Temperatura min', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Temperatura max', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4(d['SensacionTmin'][3]), style = {'width':'50%','color':'#21618c','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4(d['SensacionTmax'][3]), style = {'width':'50%','color':'#922b21','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Sensación min', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Sensación max', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['Eto'][3]," mm")), style = {'width':'100%','color':'#b03a2e','textAlign':'center','display':'inline-block'}),
                    html.H6('Evapotranspiración', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4(d['HoursSun'][3]), style = {'width':'50%','color':'red','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4(d['UV'][3]), style = {'width':'50%','color':'#884ea0','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Horas de Sol', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('UV Index', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H6(d['Sunrise'][3]), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6(d['Sunset'][3]), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Amanecer', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Puesta del sol', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    ]
                )
            
            ]
        
        card_content10 = [
            
            dbc.CardBody(
                [
                    dbc.Col(html.H4(d['Tn'][4]), style = {'width':'50%','color':'#21618c','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4(d['Tx'][4]), style = {'width':'50%','color':'#922b21','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Temperatura min', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Temperatura max', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4(d['SensacionTmin'][4]), style = {'width':'50%','color':'#21618c','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4(d['SensacionTmax'][4]), style = {'width':'50%','color':'#922b21','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Sensación min', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Sensación max', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4('{0}{1}'.format(d['Eto'][4]," mm")), style = {'width':'100%','color':'#b03a2e','textAlign':'center','display':'inline-block'}),
                    html.H6('Evapotranspiración', style = {"fontWeight":"lighter","textAlign":"center"}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H4(d['HoursSun'][4]), style = {'width':'50%','color':'red','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H4(d['UV'][4]), style = {'width':'50%','color':'#884ea0','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Horas de Sol', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('UV Index', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    dbc.Col(html.H6(d['Sunrise'][4]), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6(d['Sunset'][4]), style = {'width':'50%','color':'#ca6f1e','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Amanecer', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Col(html.H6('Puesta del sol', style = {'fontWeight':'lighter'}), style = {'width':'50%','color':'lighter','textAlign':'center','display':'inline-block'}),
                    dbc.Row(html.Br()),
                    ]
                )
            
            ]
        
        card_content11 = [
            
            dbc.CardBody(
                [
                    dbc.CardBody([dcc.Graph(figure=fig)], style={"width": "100%"}),
                    ]
                )
            
            ]
        
        card_content12 = [
            
            dbc.CardBody(
                [
                   dbc.CardBody([dcc.Graph(figure=fig2)], style={"width": "100%"}),
                    ]
                )
            
            ]
        
        card_content13 = [
            
            dbc.CardBody(
                [
                   dbc.CardBody([dcc.Graph(figure=fig3)], style={"width": "100%"}),
                    ]
                )
            
            ]
    
        
        return card_content1, card_content2, card_content3, card_content4, card_content5, card_content6, card_content7, card_content8, card_content9, card_content10,\
            card_content11, card_content12, card_content13, card_content14
         
    
#if __name__ == "__main__":
#    app.run_server()