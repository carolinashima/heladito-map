import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_gsheets import GSheetsConnection
from st_social_media_links import SocialMediaIcons
from translations import translations
lang = st.session_state.get("lang", "es")
t = translations[lang]

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

st.subheader(t["0_subh"])

app_path = 'https://heladito-map.streamlit.app/'
page_file_path = 'pages/Recomendame.py'
page = page_file_path.split('/')[1][0:-3]

# make two columns
col1, col2 = st.columns([0.7, 0.3], gap = 'small')

with col1:
    st.markdown(f'''
        {t["0_text"]}
    ''',
    unsafe_allow_html=True)

with col2:
    st.image(".static/massera.png", t["0_imagecapt"])

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
df_shops = conn.read(worksheet="heladerias", usecols=list(range(8)))
st.session_state['df_shops'] = df_shops

# load recomendados tab
url_recs = st.secrets["recs"]
df_recs = conn.read(worksheet = "recomendados", usecols=list(range(8)))
st.session_state['df_recs'] = df_recs
