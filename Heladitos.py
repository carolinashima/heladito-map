import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_gsheets import GSheetsConnection
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

# landing page content
st.title('''
Heladito map 🍦
''')
st.subheader('''
Tracker de helados que voy probando por ahí.
''')

app_path = 'https://heladito-map.streamlit.app/'
page_file_path = 'pages/Recomendame.py'
page = page_file_path.split('/')[1][0:-3]

# make two columns
col1, col2 = st.columns([0.7, 0.3], gap = 'small')

with col1:
    st.markdown(f'''
    Hola! Hice esta pequeña app para visualizar mejor las heladerías
    y helados que voy probando por ahí, como buena #GordaHeladitos.

    Si tenés ganas de recomendarme alguna heladería llená el formulario en
    <a href="{app_path}/{page}" target="_self">Recomendame</a>
    y agregaré tu sugerencia a mi mapita. Gracias! 🙌
    ''',
    unsafe_allow_html=True)

with col2:
    st.image(".static/massera.png",
    "El sueño de la piba: helado gigante 🤩. Massera en algún lugar de la costa atlántica, 15 de febrero de 1995.")

# load data
st.spinner("Connecting to Google Sheets...")

# load tracker tab
url_tracker = st.secrets["tracker"]
conn = st.connection("gsheets", type=GSheetsConnection)
df_tracker = conn.read(spreadsheet=url_tracker)
st.session_state['df_tracker'] = df_tracker

# load heladerias tab
url_shops = st.secrets["shops"]
conn = st.connection("gsheets", type=GSheetsConnection)
df_shops = conn.read(worksheet="heladerias", usecols=list(range(7)))
st.session_state['df_shops'] = df_shops

# load recomendados tab
url_recs = st.secrets["recs"]
df_recs = conn.read(worksheet = "recomendados", usecols=list(range(8)))
st.session_state['df_recs'] = df_recs
