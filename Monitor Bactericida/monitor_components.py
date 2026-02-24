import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster


def carregar_dados():
    # Carregamento de dados
    df = pd.read_csv('sample_data_clean.csv', sep=',')
    df_coordenadas = pd.read_csv('coordenadas2.csv') #, encoding='ISO-8859-1')
    
    df_mesclado = pd.merge(df, df_coordenadas, on='ds_unidade_coleta', how='left')
    
    coluna_microorganismo = 'ds_micro_organismo'
    coluna_unidade = 'ds_unidade_coleta'
    
    # Agrupar pelas colunas e contar as ocorrências
    microorganismo_vs_unidade = df.groupby([coluna_microorganismo, coluna_unidade]).size().reset_index(name='Quantidade')
      
    # Mesclar os arquivos
    df_mapa1 = pd.merge(microorganismo_vs_unidade, df_coordenadas, on='ds_unidade_coleta', how='left')
    
    return df, df_coordenadas, df_mesclado, df_mapa1

df, df_coordenadas, df_mesclado, df_mapa1 = carregar_dados()








#################################### Exibição de Data Frames ####################################

def exibir_df_dados():
    st.header("Variáveis do Banco de Dados", divider='rainbow')
        
    # Exibir o DataFrame mesclado no Streamlit
    st.dataframe(df)
    
    
def exibir_df_mesclado():
    st.header("Variáveis do Banco de Dados com Coordenadas das Unidades", divider='rainbow')
    st.dataframe(df_mesclado)


def exibir_df_dados_selecionados():
    st.header("Variáveis Selecionadas para Manipulação", divider='rainbow')
    
    # Colunas G, J, P, Z, AB, AC, AD, AE viram índices do python (Ex. A é 0; B é 1; ...)
    colunas_selecionadas = [15, 20, 28, 30, 32, 48, 49] 
    dados_selecionados = df_mesclado.iloc[:, colunas_selecionadas]
    
    st.dataframe(dados_selecionados) # Exibição do dataframe (dados)


def exibir_df_antibiotico_bac():
    # Tabela Bactéria x Antibiótico (Índice 28 e 30)
    # Definindo as colunas de Microorganismo e Antibiótico
    coluna_microorganismo = 'ds_micro_organismo'
    coluna_antibiotico = 'ds_antibiotico_microorganismo'
    
    # Agrupar por Microorganismo e Antibiótico e contar as ocorrências
    microorganismo_vs_antibiotico = df.groupby([coluna_microorganismo, coluna_antibiotico]).size().reset_index(name='Quantidade')
    resultado = microorganismo_vs_antibiotico
    
    # Exibir o DataFrame resultante no Streamlit
    st.header('Frequência de Microorganismos e Antibióticos', divider='rainbow')
    st.dataframe(resultado)


def exibir_df_unidade_bac():
    df_unidade_bac = df_mapa1
    
    st.header('Frequência de Microorganismo por Unidade', divider='rainbow')
    st.dataframe(df_unidade_bac)
    







  
##################################### Exibição de Gráficos #####################################
    
def exibir_grafico_antibiograma_bac(estilo_grafico):
    
    df.dropna(subset=['ds_antibiotico_microorganismo'], inplace = True)
    
    # Dicionário de cores
    legenda_cores = {'Sensível': 'lightgreen',
                     'Sensível Dose-Dependente': 'lightblue',
                     'Resistente': 'tomato',
                     'Não aplicável': 'white',
                     'Sensível Aumentando Exposição': 'gold'}
    
    if estilo_grafico.lower() == 'scatter':    
        st.header('Evolução das Interpretações de Antibiograma para uma Bactéria ao Longo dos Anos',divider='rainbow')

        # Converter a coluna dh_coleta_exame para DateTime e extrair o ano
        df['dh_coleta_exame'] = pd.to_datetime(df['dh_coleta_exame'])
        df['Ano'] = df['dh_coleta_exame'].dt.year
        
        # Criar SelectBoxes para Microorganismo e Antibiótico
        microorganismo_escolhido = st.selectbox('Microorganismo', ['Escolha um Microorganismo'] + list(df['ds_micro_organismo'].unique()))
        antibiotico_escolhido = st.selectbox('Antibiótico', ['Escolha um Antibiótico'] + list(df['ds_antibiotico_microorganismo'].unique()))
    
        # Filtrar o DataFrame
        df_filtrado = df[(df['ds_micro_organismo'] == microorganismo_escolhido) & (df['ds_antibiotico_microorganismo'] == antibiotico_escolhido)]
    
        # Agrupar e contar os dados
        resultado_agrupado = df_filtrado.groupby(['Ano', 'cd_interpretacao_antibiograma']).size().reset_index(name='Quantidade')
        
        # Criar o Gráfico de Linha com Plotly
        fig = px.scatter(resultado_agrupado, 
                         x='Ano', 
                         y='Quantidade', 
                         color='cd_interpretacao_antibiograma', 
                         color_discrete_map = legenda_cores,
                         trendline="lowess") # lowess', 'rolling', 'ewm', 'expanding', 'ols'
        
        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig,use_container_width=True)
        
    
    if estilo_grafico.lower() == 'bar':
        st.header('Frequência de Interpretação do Antibiograma para um Devido Antibiótico ', divider='rainbow')
        resultado_agrupado2 = df.groupby(['ds_micro_organismo', 'ds_antibiotico_microorganismo', 'cd_interpretacao_antibiograma']).size().reset_index(name='Quantidade')
        
        # Criar a SelectBox para escolher o Antibiótico
        antibiotico_escolhido2 = st.selectbox('', ['Escolha o Antibiótico'] + list(df['ds_antibiotico_microorganismo'].unique()))
        
        #if antibiotico_escolhido2 == 'Todos':
            
        
        # Filtrar o DataFrame com base no Antibiótico escolhido
        df_filtrado2 = resultado_agrupado2[resultado_agrupado2['ds_antibiotico_microorganismo'] == antibiotico_escolhido2]
        
        # Criar o Gráfico com Plotly
        fig = px.bar(df_filtrado2, 
                     x='ds_micro_organismo', 
                     y='Quantidade', 
                     color='cd_interpretacao_antibiograma',
                     color_discrete_map = legenda_cores,
                     title=f'Frequência de Interpretação do Antibiograma para o Antibiótico {antibiotico_escolhido2}')
        
        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)













#################################### Exibição de Mapas ####################################

def exibir_mapa_unidade_bac():    
    # Aplicação Streamlit
    st.header('Mapa de Microorganismo por Unidade',divider='rainbow')
    
    df = df_mapa1
    
    
    df.dropna(subset=['latitude'], inplace = True)
    df.dropna(subset=['longitude'], inplace = True)
    
    
# =============================================================================
#     max_quantidade = df_mapa1['Quantidade'].max()
#     df_mapa1['tamanho_normalizado'] = df_mapa1['Quantidade'] / max_quantidade * 5000  # Ajuste esse fator de escala conforme necessário
#     
#     
#     # Caixa de seleção para microorganismos
#     microorganismo_selecionado = st.selectbox('', ['Todos'] + list(df_mapa1['ds_micro_organismo'].unique()))
#     
#     # Caixa de seleção para unidades de coleta
#     unidade_coleta_selecionada = st.selectbox('', ['Todos'] +  list(df_mapa1['ds_unidade_coleta'].unique()))
#     
#     # Botão para focar na unidade de coleta no mapa
#     if st.button('Clique aqui para ir até a unidade no mapa'):
#         unidade_coleta_info = df_mapa1[df_mapa1['ds_unidade_coleta'] == unidade_coleta_selecionada].iloc[0]
#         latitude = unidade_coleta_info['latitude']
#         longitude = unidade_coleta_info['longitude']
#         zoom = 15  # Zoom mais próximo para a unidade
#     else:
#         latitude = df_mapa1['latitude'].mean()
#         longitude = df_mapa1['longitude'].mean()
#         zoom = 11
#     
#     # Filtrar dados com base no microorganismo e unidade de coleta selecionados
#     if unidade_coleta_selecionada == 'Todos':
#         dados_filtrados = df_mapa1[df_mapa1['ds_micro_organismo'] == microorganismo_selecionado]
#     else:
#         dados_filtrados = df_mapa1[(df_mapa1['ds_micro_organismo'] == microorganismo_selecionado) & (df['ds_unidade_coleta'] == unidade_coleta_selecionada)]
# 
#     
#     # Configurar o mapa
#     st.pydeck_chart(pdk.Deck(
#         map_style='mapbox://styles/mapbox/light-v8',
#         initial_view_state=pdk.ViewState(
#             latitude=latitude,
#             longitude=longitude,
#             zoom=zoom,
#             pitch=50,
#         ),
#         layers=[
#             pdk.Layer(
#                 'ScatterplotLayer',
#                 data=dados_filtrados,
#                 get_position='[longitude, latitude]',
#                 get_color='[200, 30, 0, 160]',
#                 get_radius='tamanho_normalizado',  # Use o valor normalizado para o tamanho do círculo
#                 pickable=True
#             ),
#         ],
#         tooltip={
#             'html': '<b>Quantidade:</b> {Quantidade}',
#             'style': {
#                 'color': 'white'
#             }
#         }
#     ))
# =============================================================================
 
    







   

    
    # Caixa de seleção para microorganismos
    microorganismo_selecionado = st.selectbox('Selecione um microorganismo', ['Todos'] + list(df['ds_micro_organismo'].unique()))
    
    # Caixa de seleção para unidades de coleta
    unidade_coleta_selecionada = st.selectbox('Selecione uma unidade de coleta', ['Todos'] + list(df['ds_unidade_coleta'].unique()))
    
    # Botão para focar na unidade de coleta no mapa
    botao_focado = st.button('Clique aqui para ir até a unidade no mapa!')
    
    # Filtrar dados com base no microorganismo e unidade de coleta selecionados
    if microorganismo_selecionado != 'Todos':
        df = df[df['ds_micro_organismo'] == microorganismo_selecionado]
    if unidade_coleta_selecionada != 'Todos':
        df = df[df['ds_unidade_coleta'] == unidade_coleta_selecionada]
    
    # Criar mapa usando Folium
    if botao_focado and unidade_coleta_selecionada != 'Todos':
        unidade_coleta_info = df[df['ds_unidade_coleta'] == unidade_coleta_selecionada].iloc[0]
        mapa = folium.Map(location=[unidade_coleta_info['latitude'], unidade_coleta_info['longitude']], zoom_start=15)
    else:
        mapa = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=11)
    
    # Adicionar marcadores ao mapa
    marker_cluster = MarkerCluster().add_to(mapa)
    for _, row in df.iterrows():
        folium.CircleMarker(location=[row['latitude'], row['longitude']],
                            radius=25, # Ajuste o tamanho conforme necessário
                            popup=f"Microorganismo: {row['ds_micro_organismo']}<br>Quantidade: {row['Quantidade']}",
                            fill=True).add_to(marker_cluster)
    
    # Mostrar o mapa no Streamlit
    folium_static(mapa)




    st.header('',divider='blue')

    mapbox_token = "SUA_CHAVE_DO_MAPBOX"
    
    #st.header('Mapa de Frequência de Microorganismos por Unidade', divider='rainbow')
    
    # Adicionar a Select Box para escolher o microorganismo
    microorganismo_escolhido = st.selectbox('Selecione o Microorganismo', df_mapa1['ds_micro_organismo'].unique())
    
    # Filtrar o DataFrame com base no Microorganismo escolhido
    df_filtrado = df_mapa1[df_mapa1['ds_micro_organismo'] == microorganismo_escolhido]
    
    # Create an interactive map using plotly express with Mapbox
    fig = px.scatter_mapbox(df_filtrado,
                            lat='latitude',
                            lon='longitude',
                            size='Quantidade',
                            color='ds_unidade_coleta',
                            hover_name='ds_unidade_coleta',
                            title=f'Mapa de Frequência de {microorganismo_escolhido} por Unidade',
                            mapbox_style="carto-positron",  # Escolha o estilo do mapa (veja as opções disponíveis)
                            zoom=3,  # Defina o nível de zoom inicial
                            center=dict(lat=-14.235, lon=-51.925))  # Centralize no Brasil
    
    # Customize the layout
    fig.update_layout(mapbox=dict(accesstoken=mapbox_token),  # Adicione a chave do Mapbox
                      showlegend=True, legend_title_text='Unidade de Coleta',
                      margin=dict(l=0, r=0, t=0, b=0))  # Margens do layout
    
    # Show the map in Streamlit
    st.plotly_chart(fig)