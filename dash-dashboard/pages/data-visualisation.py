import dash
import pandas as pd
from dash import html, dcc, dash_table
import mysql.connector
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import datetime

dash.register_page(__name__, title='MFLG')

layout = html.Div([
    html.H1('Data Visualisation'),
    html.Div(),
])
