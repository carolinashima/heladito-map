from json import tool
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
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

st.header(t["1_title"])
st.markdown(f'''
            {t["1_maintext"]}
''')

# load data from session state
df_shops = st.session_state['df_shops']
df_recs = st.session_state['df_recs']
center_baires = [-34.51503743529771, -58.489184953954116]
center_berlin = [52.50043422330395, 13.406035370951068]

# create map
center_point = st.radio(t["1_cityopt"], ["Buenos Aires","Berlin"])
if center_point == "Buenos Aires":
    ciudad = center_baires
elif center_point == "Berlin":
    ciudad = center_berlin
map = folium.Map(location = ciudad, zoom_start = 12)

# choose what to show
display_options = [t["1_showopt1"],t["1_showopt2"],t["1_showopt3"]]
selection = st.radio(
    t["1_show"],
    [t["1_showopt1"],t["1_showopt2"],t["1_showopt3"]]
)

if selection == t["1_showopt1"]:
    for _, row in df_recs.iterrows():
        location = pd.to_numeric(row['latitude']), pd.to_numeric(row['longitude'])
        folium.Marker(location, 
        popup=row['nombre'],
        tooltip=row['nombre'],
        icon=folium.Icon(icon='fa-ice-cream',prefix='fa',color='gray')).add_to(map)
        
    for _, row in df_shops.iterrows():
        location = pd.to_numeric(row['latitude']), pd.to_numeric(row['longitude'])
        if row['avg'] < 2:
            color = 'red'
        elif row['avg'] >= 2 and row['avg'] < 3:
            color = 'orange'
        elif row['avg'] >= 3 and row['avg'] < 4:
            color = 'blue'
        else:
            color = 'green'
        folium.Marker(location, 
        popup=row['nombre'] + ': ' + str(round(row['avg'],2)),
        tooltip=row['nombre'],
        icon=folium.Icon(icon='fa-ice-cream',prefix='fa',color=color)).add_to(map)

    
if selection == t["1_showopt2"]:
    for _, row in df_shops.iterrows():
        location = pd.to_numeric(row['latitude']), pd.to_numeric(row['longitude'])
        if row['avg'] < 2:
            color = 'red'
        elif row['avg'] >= 2 and row['avg'] < 3:
            color = 'orange'
        elif row['avg'] >= 3 and row['avg'] < 4:
            color = 'blue'
        else:
            color = 'green'
        folium.Marker(location, 
        popup=row['nombre'] + ': ' + str(round(row['avg'],2)),
        tooltip=row['nombre'],
        icon=folium.Icon(icon='fa-ice-cream',prefix='fa',color=color)).add_to(map)

elif selection == t["1_showopt3"]:
    for _, row in df_recs.iterrows():
        location = pd.to_numeric(row['latitude']), pd.to_numeric(row['longitude'])
        folium.Marker(location, 
        popup=row['nombre'] + ' (recomendado por ' + row['persona'] + ')',
        tooltip=row['nombre'],
        icon=folium.Icon(icon='fa-ice-cream',prefix='fa',color='gray')).add_to(map)

# render map
st_data = st_folium(map, width=725)
