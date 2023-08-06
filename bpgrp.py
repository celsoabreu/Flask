#-------------------------------------------------------------------------------
# Name:        bpadm.py
# Purpose:
#
# Author:      Celso Abreu
#
# Created:     12/03/2023
# Copyright:   (c) CA_ON 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from flask import Flask, Response, url_for, render_template, \
request, redirect, flash, session, abort, g
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user, current_user
from datetime import timedelta
                                
from flask import Blueprint
from datetime import date
from datetime import datetime
from app.models.tabels import CaUsuario, CaModulo, CaRotina, CaAplic
#, CaUsucli, CaUsumot, CaGrupo, CaMemgrupo, CaPedcar, Post, Follow

from database import db

from dash import Dash, html,  dcc
from dash_core_components import  Graph,  Dropdown, Slider, Checklist, Interval 
#from dash_html_components as html 
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import dash_table

import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd
import json 

# site fontes ofociais covid.saude.gov.br 

#df = pd.read_csv("app/assets/HIST_PAINEL_COVIDBR_2022_Parte2_02jun2023.csv", sep=";")
#df_states = df[ (~df["estado"].isna()) & (df["codmun"].isna()) ]
#df_brasil = df[df["regiao"] == "Brasil"]
#df_states.to_csv("df_states.csv")
#df_brasil.to_csv("df_brasil.csv")

server = Flask(__name__)

data_atual = date.today()
data_em_texto = data_atual.strftime('%d/%m/%Y')
dt_ini = data_atual.strftime('%d/%m/%Y')
data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y')
duracao = data_e_hora_atuais.strftime('%d/%m/%Y')

#df_states = pd.read_csv("df_states.csv")
#df_brasil = pd.read_csv("df_brasil.csv")

#Debulhando o arquivo brazil_geo.json 
#brazil_states = json.load(open("app/geojson/brazil_geo.json", "r"))
#type(brasil_states)  => dict 
#brasil_states.keys() => dict_keys("type", "features")
#brazil_states["features"]  => 'FeatureCollection'
#type(brazil_states["features"]) => list 
#brazil_states["features"][0]  => Volta com dados gigantes
#type(brazil_states["features"][0]) => diz que outro dict 
# mais uma vez vou pergubntar quais sao as chaves deste dict 
#brazil_states["features"][0].keys => ele mostra => dict_keys(['type', 'id', 'proptys', 'geometry'])
#brazil_states["features"][0]["id"] => "AC"
#brazil_states["features"][0]["geometry"] => informa todas as latitudes e longitudes de todos os  pontos

CENTER_LAT, CENTER_LON = -14.272572694355336, -51.25567404158474

# =====================================================================
# Data Load
df_states = pd.read_csv("df_states.csv")
df_brasil = pd.read_csv("df_brasil.csv")

#token = open(".mapbox_token").read()
brazil_states = json.load(open("app/geojson/brazil_geo.json", "r"))

brazil_states["features"][0].keys()

df_states_ = df_states[df_states["data"] == "2020-05-13"]
select_columns = {"casosAcumulado": "Casos Acumulados", 
                "casosNovos": "Novos Casos", 
                "obitosAcumulado": "Óbitos Totais",
                "obitosNovos": "Óbitos por dia"}

# ========================================
# Instanciação do Dash


bp_grp = Blueprint("grp", __name__, template_folder="app/templates", static_url_path='assets') 

@bp_grp.route('/dash_covid')
@login_required
def dash_covid():

	#"""Create a Plotly Dash dashboard embedded within Flask"""	
	dash_app1 = Dash(server=server, name="Casos de COVID-19 2022/2023", 
			url_base_pathname="/dash_covid/", 
			external_stylesheets=[dbc.themes.CYBORG])
	
	# Esta função 'choropleth_mapbox()' choropleth sao mapas que tem as divisoes coloridas, mapbox é uma API externa que 
	# cria graficos maisbonitos, podemos estudar eles na documentação choropleth_mapbox la tem documentaçao e vrios exemplos.
	# Parametros passados
	# 1o. parametro dataframe que contem as informações que seram plotadas df_states, com shift+tab aparece as propriedades que complementam
	
	fig = px.choropleth_mapbox(df_states_, locations="estado",
    	geojson=brazil_states, 
   		center={"lat": -16.95, "lon": -47.78},  # https://www.google.com/maps/ -> right click -> get lat/lon
    	zoom=4, 
    	color="casosNovos", 
    	color_continuous_scale="Redor",
     	opacity=0.4,
   		hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "estado": True} # Mostra aa informações das colunas
    )

	fig.update_layout(
		mapbox_style ="carto_darkmatter"
	)

	# ======================================
	# layout
	
	dash.app1.layout = dbc.Container(
		dbc.Row([
			dbc.Col([
				dcc.Graph(id="choropleth-map", figure=fig)
			])
		])
	)

	#return dash_covid