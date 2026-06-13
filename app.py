import streamlit as st
from st_social_media_links import SocialMediaIcons

st.set_page_config(layout='wide',
initial_sidebar_state='expanded',
page_title='Heladito map',
page_icon='🍦')

st.title("🍦 Heladito map")

# language options on sidebar
lang_opt = ["🇦🇷", "🇬🇧"]
lang = st.sidebar.pills("Idioma/language", lang_opt)
lang = "es" if lang == "🇦🇷" else "en"
st.session_state["lang"] = lang

page_names = {
    "es": {"mapa": "Mapa", "lista": "Lista", "stats": "Stats", "rec": "Recomendame"},
    "en": {"mapa": "Map", "lista": "List", "stats": "Stats", "rec": "Recommend me"},
}
p = page_names[lang]

pg = st.navigation([
    st.Page("Heladitos.py", title="Heladitos", default=True),
    st.Page("pages/1_Mapa.py", title=p["mapa"]),
    st.Page("pages/2_Lista.py", title=p["lista"]),
    st.Page("pages/3_Stats.py", title=p["stats"]),
    st.Page("pages/4_Recomendame.py", title=p["rec"]),
])
pg.run()