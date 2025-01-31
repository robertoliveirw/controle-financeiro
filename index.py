import streamlit as st  
import pandas as pd

st.set_page_config(layout='wide')

df_clientes = pd.read_csv('data\clientes.csv', sep=';')
df_clientes