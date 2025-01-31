import streamlit as st  
import pandas as pd
import plotly.graph_objects as go


st.set_page_config(layout='wide')

# Carregar dados
df_clientes = pd.read_csv('data\clientes.csv', sep=';', decimal='.')
df_clientes['Aniversario'] = pd.to_datetime(df_clientes['Aniversario'], dayfirst=True)

df_entradas = pd.read_csv('data\entradas.csv', sep=';', decimal='.')
df_entradas['Data da Entrada'] = pd.to_datetime(df_entradas['Data da Entrada'], dayfirst=True)

df_saidas = pd.read_csv('data\saidas.csv', sep=';', decimal='.')
df_saidas['Data'] = pd.to_datetime(df_saidas['Data'], dayfirst=True)   

# Calcular os totais
total_entradas = df_entradas['Valor'].sum()
total_saidas = df_saidas['Valor'].sum()
saldo_total = total_entradas - total_saidas

# Criar os quadros com Plotly
fig = go.Figure()

fig.add_trace(go.Indicator(
    mode="number",
    value=total_entradas,
    title={"text": "Entradas (R$)"},
    domain={'row': 0, 'column': 0}
))

fig.add_trace(go.Indicator(
    mode="number",
    value=total_saidas,
    title={"text": "Saídas (R$)"},
    domain={'row': 0, 'column': 1}
))

fig.add_trace(go.Indicator(
    mode="number",
    value=saldo_total,
    title={"text": "Saldo (R$)"},
    domain={'row': 0, 'column': 2}
))

fig.update_layout(
    grid={'rows': 1, 'columns': 3, 'pattern': "independent"},
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)