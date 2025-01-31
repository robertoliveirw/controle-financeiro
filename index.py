import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout='wide')

# HEADER
# Título
st.title('Baskuit - Acompanhamento Financeiro')

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

# Organizar os gráficos por linha
# Primeiro, exibimos os gráficos de indicadores (entradas, saídas, saldo)
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

# Exibir o gráfico de linhas abaixo dos indicadores
st.plotly_chart(fig_linhas, use_container_width=True)

# Botões para adicionar entradas, saídas e clientes
# Criar os botões na barra lateral
if st.sidebar.button('Adicionar Entrada'):
    with st.form(key='form_entrada'):
        st.subheader("Adicionar Entrada")
        cliente_entrada = st.text_input("Cliente")
        item_comprado = st.text_input("Item Comprado")
        data_entrada = st.date_input("Data da Entrada", min_value=pd.to_datetime('2020-01-01'))
        valor_entrada = st.number_input("Valor da Entrada (R$)", min_value=0.0, format="%.2f")

        if st.form_submit_button("Salvar Entrada"):
            try:
                # Carregar o arquivo de entradas
                df_entradas = pd.read_csv('data/entradas.csv', sep=';', decimal='.')

                # Adicionar os novos dados ao dataframe
                new_entry = {
                    'Cliente': cliente_entrada,
                    'Item Comprado': item_comprado,
                    'Data da Entrada': data_entrada,
                    'Valor': valor_entrada
                }

                # Adicionar a nova entrada
                df_entradas = df_entradas.append(new_entry, ignore_index=True)

                # Salvar o dataframe atualizado de volta no arquivo CSV
                df_entradas.to_csv('data/entradas.csv', sep=';', decimal='.', index=False)

                st.success("Entrada adicionada com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar a entrada: {e}")


if st.sidebar.button('Adicionar Saída'):
    with st.form(key='form_saida'):
        st.subheader("Adicionar Saída")
        data_saida = st.date_input("Data da Saída", min_value=pd.to_datetime('2020-01-01'))
        local_saida = st.text_input("Local")
        item_saida = st.text_input("Item")
        valor_saida = st.number_input("Valor da Saída (R$)", min_value=0.0, format="%.2f")

        if st.form_submit_button("Salvar Saída"):
            try:
                # Carregar o arquivo de saídas
                df_saidas = pd.read_csv('data/saidas.csv', sep=';', decimal='.')

                # Adicionar os novos dados ao dataframe
                new_exit = {
                    'Data': data_saida,
                    'Local': local_saida,
                    'Item': item_saida,
                    'Valor': valor_saida
                }

                # Adicionar a nova saída
                df_saidas = df_saidas.append(new_exit, ignore_index=True)

                # Salvar o dataframe atualizado de volta no arquivo CSV
                df_saidas.to_csv('data/saidas.csv', sep=';', decimal='.', index=False)

                st.success("Saída adicionada com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar a saída: {e}")


if st.sidebar.button('Adicionar Cliente'):
    with st.form(key='form_cliente'):
        st.subheader("Adicionar Cliente")
        nome_cliente = st.text_input("Nome do Cliente")
        aniversario_cliente = st.date_input("Data de Aniversário")
        contato_cliente = st.text_input("Contato")
        instagram_cliente = st.text_input("Instagram")

        if st.form_submit_button("Salvar Cliente"):
            try:
                # Carregar o arquivo de clientes
                df_clientes = pd.read_csv('data/clientes.csv', sep=';', decimal='.')

                # Adicionar os novos dados ao dataframe
                new_client = {
                    'Nome': nome_cliente,
                    'Aniversario': aniversario_cliente,
                    'Contato': contato_cliente,
                    'Instagram': instagram_cliente
                }

                # Adicionar o novo cliente
                df_clientes = df_clientes.append(new_client, ignore_index=True)

                # Salvar o dataframe atualizado de volta no arquivo CSV
                df_clientes.to_csv('data/clientes.csv', sep=';', decimal='.', index=False)

                st.success("Cliente adicionado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar o cliente: {e}")
