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

social_media_icons.render(sidebar=True, justify_content='start')

st.header('Lista completa')

st.write('''
Las filas sin fecha son mis favoritos de la vida. 🫶
''')

selected_cols = ['fecha','nombre','local','gusto','rating','review','notas']
sorted_df = st.session_state['df_tracker'][selected_cols].sort_values(by='fecha', ascending = False)
st.dataframe(sorted_df, hide_index=True,
column_config = {
    'fecha': 'Fecha',
    'nombre': 'Nombre',
    'local': 'Local',
    'gusto': 'Gusto',
    'rating': 'Rating',
    'review': 'Review',
    'notas': 'Notas'
    })

