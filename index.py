import streamlit as st  
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout='wide')

# HEADER
# Título
st.title('Baskuit - Acompanhamento Financeiro')

# Descrição
st.write(''' 
        • Entradas 💵: Acompanhe o total de receitas geradas, com dados atualizados para um controle preciso do fluxo de caixa. \n 
        • Saídas 💸: Monitore as despesas e saídas de recursos, ajudando a identificar áreas de custos. \n 
        • Saldo 📉📈: Veja o saldo atual, com a diferença entre entradas e saídas, para garantir a saúde financeira.''')

# Carregar dados
df_clientes = pd.read_csv('data/clientes.csv', sep=';', decimal='.')
df_clientes['Aniversario'] = pd.to_datetime(df_clientes['Aniversario'], dayfirst=True)

df_entradas = pd.read_csv('data/entradas.csv', sep=';', decimal='.')
df_entradas['Data da Entrada'] = pd.to_datetime(df_entradas['Data da Entrada'], dayfirst=True)

df_saidas = pd.read_csv('data/saidas.csv', sep=';', decimal='.')
df_saidas['Data'] = pd.to_datetime(df_saidas['Data'], dayfirst=True)   

# Calcular os totais
total_entradas = df_entradas['Valor'].sum()
total_saidas = df_saidas['Valor'].sum()
saldo_total = total_entradas - total_saidas

# Converter as datas para datetime no formato correto
start_date = df_entradas['Data da Entrada'].min().to_pydatetime()
end_date = df_entradas['Data da Entrada'].max().to_pydatetime()

# Slider para filtro lateral (convertendo para datetime)
start_date_slider, end_date_slider = st.sidebar.slider(
    "Selecione o intervalo de datas",
    min_value=start_date,
    max_value=end_date,
    value=(start_date, end_date),
    format="DD/MM/YYYY"
)

# Filtrando os dados com base no intervalo de datas
df_entradas_filtrado = df_entradas[(df_entradas['Data da Entrada'] >= start_date_slider) & (df_entradas['Data da Entrada'] <= end_date_slider)]
df_saidas_filtrado = df_saidas[(df_saidas['Data'] >= start_date_slider) & (df_saidas['Data'] <= end_date_slider)]

# Calcular os totais com os dados filtrados
total_entradas = df_entradas_filtrado['Valor'].sum()
total_saidas = df_saidas_filtrado['Valor'].sum()
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

# Exibir o gráfico
st.plotly_chart(fig, use_container_width=True)
