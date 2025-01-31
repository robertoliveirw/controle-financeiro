import streamlit as st  
import pandas as pd

st.set_page_config(layout='wide')

# Carregar dados
df_clientes = pd.read_csv('data\clientes.csv', sep=';', decimal='.')
df_clientes['Aniversario'] = pd.to_datetime(df_clientes['Aniversario'], dayfirst=True)
df_clientes

df_entradas = pd.read_csv('data\entradas.csv', sep=';', decimal='.')
df_entradas['Data da Entrada'] = pd.to_datetime(df_entradas['Data da Entrada'], dayfirst=True)
df_entradas

df_saidas = pd.read_csv('data\saidas.csv', sep=';', decimal='.')
df_saidas['Data'] = pd.to_datetime(df_saidas['Data'], dayfirst=True)
df_saidas

# Calcular os totais