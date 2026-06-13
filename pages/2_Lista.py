import streamlit as st
from st_social_media_links import SocialMediaIcons
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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

if lang == 'es':
    rev_col_name = 'review'
elif lang == 'en':
    rev_col_name = 'review_en'

selected_cols = ['fecha',
'nombre',
'local',
'gusto',
'rating',
'notas',
'tipo',
'category',
'base',
'cositos',
rev_col_name]

df_shops = st.session_state['df_shops']
df_tracker = st.session_state['df_tracker']
st.subheader(t["2_subh1"])
st.write(t["2_text"])

# select city
selected_city = st.selectbox(t["2_cityselect"], df_shops['city'].unique())
df_city = df_shops[df_shops['city'] == selected_city].copy()

# select shop
df_city['display_name'] = df_city['nombre'] + " (" + df_city['local'] + ")"
selected_shop = st.selectbox(t["2_shopselect"], df_city['display_name'].sort_values())

shop_row = df_city[df_city['display_name'] == selected_shop].iloc[0]

# filter entries
mask = (
    (df_tracker['nombre'] == shop_row['nombre']) &
    (df_tracker['local'] == shop_row['local'])
)
sabores = df_tracker[mask]

# aggregate
flavor_avg = (
    sabores.groupby(['nombre', 'local', 'gusto'])['rating']
    .mean()
    .reset_index()
    .rename(columns={'rating': 'avg_rating'})
    .sort_values('avg_rating', ascending=False)
)

# shop
st.markdown(f"### {shop_row['nombre']}")
st.caption(f'''{shop_row['local']} · {t["2_shopavg"]}: **{shop_row['avg']:.1f} / 5**''')
if pd.notna(shop_row.get('notas', '')) and shop_row['notas'] != '':
    st.write(f'''{t["2_notes"]}: {shop_row['notas']}''')


for _, f in flavor_avg.iterrows():
    estrellas = "★" * round(f['avg_rating']) + "☆" * (5 - round(f['avg_rating']))
    
    # get all entries for this flavor, sorted newest first
    entradas = (
        sabores[sabores['gusto'] == f['gusto']]
        .sort_values('fecha', ascending=False)
    )
    
    reviews_html = ""
    for _, e in entradas.iterrows():
        if pd.notna(e[rev_col_name]) and e[rev_col_name] != '':
            reviews_html += f"<p style='margin:2px 0; font-size:12px; color:#888;'><b>{e['fecha']}</b>: {e[rev_col_name]}</p>"
    
    st.markdown(f"""
    <div style="padding:8px 0; border-bottom:0.5px solid #eee;">
        <div style="display:flex; justify-content:space-between; align-items:baseline;">
            <b style="font-size:14px;">{f['gusto']}</b>
            <span style="color:#BA7517; font-size:14px; letter-spacing:1px;">{estrellas}</span>
        </div>
        {reviews_html}
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.header(t["2_subh2"])
sorted_df = st.session_state['df_tracker'][selected_cols].sort_values(by='fecha', ascending = False)
with st.expander(t["2_tabletitle"]):
    st.dataframe(sorted_df, hide_index=True,
    column_order = ('fecha','nombre','local','gusto','rating',rev_col_name,'notas'),
    column_config = {
        'fecha': 'Fecha',
        'nombre': 'Nombre',
        'local': 'Local',
        'gusto': 'Gusto',
        'rating': 'Rating',
        rev_col_name: 'Review',
        'notas': 'Notas'
        })
