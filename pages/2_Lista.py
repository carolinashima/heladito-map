import streamlit as st
from st_social_media_links import SocialMediaIcons

# page config
st.set_page_config(layout='wide',
initial_sidebar_state='expanded',
page_title='Heladito map',
page_icon='🍦')

st.sidebar.header('🍦 Heladito map')
st.sidebar.markdown('''
---
Made by Carolina L. Shimabukuro 👩🏻‍💻
''')
social_media_links = [
    "https://www.linkedin.com/in/carolina-shimabukuro/",
    "https://github.com/carolinashima"
]
colors = ["black","black"]
social_media_icons = SocialMediaIcons(social_media_links, colors)

social_media_icons.render(sidebar=True)

st.header('Lista completa')
selected_cols = ['fecha','nombre','local','gusto','rating','review','notas']
df_tracker = st.session_state['df_tracker'][selected_cols]
st.dataframe(df_tracker, hide_index=True,
column_config = {
    'fecha': 'Fecha',
    'nombre': 'Nombre',
    'local': 'Local',
    'gusto': 'Gusto',
    'rating': 'Rating',
    'review': 'Review',
    'notas': 'Notas'
    })

