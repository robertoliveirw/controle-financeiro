import streamlit as st  
import pandas as pd

st.set_page_config(layout='wide')

df_clientes = pd.read_csv('data\clientes.csv', sep=';', decimal='.')
df_clientes

df_entradas = pd.read_csv('data\entradas.csv', sep=';', decimal='.')
df_entradas

df_saidas = pd.read_csv('data\saidas.csv', sep=';', decimal='.')
df_saidas