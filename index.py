import streamlit as st  
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

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
fig_caixa = go.Figure()

fig_caixa.add_trace(go.Indicator(
    mode="number",
    value=total_entradas,
    title={"text": "Entradas (R$)"},
    domain={'row': 0, 'column': 0}
))

fig_caixa.add_trace(go.Indicator(
    mode="number",
    value=total_saidas,
    title={"text": "Saídas (R$)"},
    domain={'row': 0, 'column': 1}
))

fig_caixa.add_trace(go.Indicator(
    mode="number",
    value=saldo_total,
    title={"text": "Saldo (R$)"},
    domain={'row': 0, 'column': 2}
))

fig_caixa.update_layout(
    grid={'rows': 1, 'columns': 3, 'pattern': "independent"},
    template="plotly_white"
)

# Exibir o gráfico de indicadores
st.plotly_chart(fig_caixa, use_container_width=True)

# Preparar os dados para o gráfico de linhas
df_entradas_filtrado_grouped = df_entradas_filtrado.groupby('Data da Entrada').agg({'Valor': 'sum'}).reset_index()
df_entradas_filtrado_grouped['Tipo'] = 'Entrada'  # Adicionar coluna para identificar entradas

df_saidas_filtrado_grouped = df_saidas_filtrado.groupby('Data').agg({'Valor': 'sum'}).reset_index()
df_saidas_filtrado_grouped['Tipo'] = 'Saída'  # Adicionar coluna para identificar saídas

# Renomear a coluna 'Data' para 'Data da Entrada' nas saídas para combinar com as entradas
df_saidas_filtrado_grouped = df_saidas_filtrado_grouped.rename(columns={'Data': 'Data da Entrada'})

# Concatenando as entradas e saídas para o gráfico
df_combined = pd.concat([df_entradas_filtrado_grouped, df_saidas_filtrado_grouped], axis=0, ignore_index=True)

# Criar o gráfico de linhas
fig_linhas = px.line(
    df_combined,
    x="Data da Entrada",  # Eixo X será a data
    y="Valor",             # Eixo Y será o valor
    color="Tipo",          # As linhas serão diferenciadas pelo tipo (entrada ou saída)
    labels={"Valor": "Valor (R$)", "Data da Entrada": "Data"},
    title="Entradas e Saídas ao Longo do Tempo"
)

# Exibir o gráfico de linhas
st.plotly_chart(fig_linhas, use_container_width=True)
