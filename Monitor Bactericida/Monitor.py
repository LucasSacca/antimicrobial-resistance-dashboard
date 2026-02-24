import streamlit as st
import hydralit_components as hc
import pandas as pd
import plotly.express as px
import pydeck as pdk
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

from monitor_components import *

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

logo_einstein = 'logo_einstein.jpg'
predio_einstein = 'predio_einstein.jpg'
hospital_einstein = 'Fachada.png'
chacara_klabin = 'ChacaraKlabin.png'
alphaville = 'Alphaville.png'
bacteria = 'Bacteria.png'
grupo = 'Grupo1.png'



col1, col2, col3 = st.columns([0.5,10,2])

with col2:
    st.header('')
    st.title('Painel de Monitoramento de Bactérias')
    st.header('')

with col3:
    st.header('')
    st.image(logo_einstein)#, width=400)


# specify the primary menu definition
menu_data = [
    {'icon': "fas fa-home", 'label': "Home"},
    {'icon': "fas fa-table", 'label': "Tabelas"},
    {
        'icon': "far fa-chart-bar",
        'label': "Gráficos",
        'submenu': [
            {'id': 'subid11', 'icon': "fa fa-paperclip", 'label': "Evolução do Antibiograma para uma Bactéria no Decorrer dos Anos"},
            {'id': 'subid12', 'icon': "fa fa-paperclip", 'label': "AntibiogramaXAntibiótico"}
        ]
    },
    {'icon': "fas fa-map", 'label': "Mapa da Rede"}
]

over_theme = {'txc_inactive': '#FFFFFF'}

menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    #login_name='Logout',  # Logout ainda é um link, não um botão de encerramento
    hide_streamlit_markers=True, 
    sticky_nav=True, 
    sticky_mode='pinned', 
)


# Adicionando a mensagem de boas-vindas na Home
if menu_id == 'Home':
    
# =============================================================================
#     col1, col2, col3 = st.columns([1,20,20])
#     
#     with col2:
#         st.header('', divider='blue') 
#         st.title('Sobre o Projeto:') 
#         st.subheader('Painel de monitoramento voltado para a facilitação das tomadas de decisões sobre o uso de antibióticos para o combate de microrganismos, avaliando a resistência desses contra os fármacos no decorrer dos anos.')
#         st.header('', divider='blue') 
# 
#         #st.header('', divider='blue') 
#         st.header('E-mail para contato:') 
#         st.subheader('email@decontato.com.br')
#         st.header('', divider='blue') 
#     with col3:
#         st.image(predio_einstein)
# =============================================================================
   
    
    col1, col2, col3 = st.columns([1,4,1])
    
    with col2:
        st.header('', divider='blue') 
        st.title('Sobre o Projeto') 
        st.subheader('Painel de monitoramento voltado para a facilitação das tomadas de decisões sobre o uso de antibióticos para o combate de microrganismos, avaliando a resistência desses contra os fármacos no decorrer dos anos.')
        st.image(bacteria)
        st.header('', divider='blue') 
        
        st.header('Conheça as unidades do Einstein:')
        image_paths = [hospital_einstein, chacara_klabin, alphaville]
        current_image_idx = st.session_state.get('current_image_idx', 0)
    
        # Exibe a imagem atual
        st.image(image_paths[current_image_idx])
        st.subheader('Clique *Avançar* para ir para próxima imagem e *Voltar* para voltar')
    
        # Botão para retroceder
        if st.button('Voltar') and current_image_idx > 0:
            current_image_idx -= 1
    
        # Botão para avançar
        if st.button('Avançar') and current_image_idx < len(image_paths) - 1:
            current_image_idx += 1
    
        # Atualiza o índice da imagem na sessão do Streamlit
        st.session_state['current_image_idx'] = current_image_idx
        st.header('', divider='blue') 
    
        st.header('Redes sociais') 
        st.subheader('Intragram:')
        st.text('@aaaldv.einsten @camc.einstein')
        st.subheader('E-mail para contato')
        st.text('relacionamentocorpoclinico@einstein.br')
        st.header('', divider='blue') 
        
        st.text('Projeto feito pelo Grupo 1')
        st.text('Catarina Ramos / Carolina Scilingo / Gustavo Chang / Lucas Sacca / Pedro Caldas / Yunes Natal')
        st.image(grupo)


# Placeholder para ação de logout (não fecha o servidor Streamlit)
if menu_id == 'Tabelas':
    exibir_df_dados()
    col1, col2, col3 = st.columns([10,1,10])
    with col1:
        exibir_df_dados_selecionados()
        
    with col3:
        exibir_df_unidade_bac()


# Primeira subdivisão dos gráficos
if menu_id == 'subid11':
    exibir_grafico_antibiograma_bac('scatter')
    

# Segunda subdivisão dos gráficos    
if menu_id == 'subid12':
    exibir_grafico_antibiograma_bac('bar')


if menu_id == 'Mapa da Rede':
    exibir_mapa_unidade_bac()
    #exibir_df_unidade_bac()
        
    
