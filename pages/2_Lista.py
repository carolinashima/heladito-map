import streamlit as st
from st_social_media_links import SocialMediaIcons
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

selected_cols = ['fecha',
'nombre',
'local',
'gusto',
'rating',
'review',
'notas',
'tipo',
'category',
'base',
'cositos']

df_shops = st.session_state['df_shops']
df_tracker = st.session_state['df_tracker']
st.subheader("Heladerías")
st.write("""
Seleccioná una heladería para ver qué gustos pedí y qué me pareció en general.
""")

# select city
selected_city = st.selectbox("Ciudad", df_shops['city'].unique())
df_city = df_shops[df_shops['city'] == selected_city].copy()

# select shop
df_city['display_name'] = df_city['nombre'] + " (" + df_city['local'] + ")"
selected_shop = st.selectbox("Heladería", df_city['display_name'].sort_values())

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
st.caption(f"{shop_row['local']} · Promedio: **{shop_row['avg']:.1f} / 5**")
#if pd.notna(shop_row['notas']) and shop_row['notas'] != '':
if pd.notna(shop_row.get('notas', '')) and shop_row['notas'] != '':
    st.write(f"Notas: {shop_row['notas']}")


for _, f in flavor_avg.iterrows():
    estrellas = "★" * round(f['avg_rating']) + "☆" * (5 - round(f['avg_rating']))
    
    # Get all entries for this flavor, sorted newest first
    entradas = (
        sabores[sabores['gusto'] == f['gusto']]
        .sort_values('fecha', ascending=False)
    )
    
    reviews_html = ""
    for _, e in entradas.iterrows():
        if pd.notna(e['review']) and e['review'] != '':
            reviews_html += f"<p style='margin:2px 0; font-size:12px; color:#888;'><b>{e['fecha']}</b>: {e['review']}</p>"
    
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

st.header('Lista entera')
sorted_df = st.session_state['df_tracker'][selected_cols].sort_values(by='fecha', ascending = False)
with st.expander('Ver tabla'):
    st.dataframe(sorted_df, hide_index=True,
    column_order = ('fecha','nombre','local','gusto','rating','review','notas'),
    column_config = {
        'fecha': 'Fecha',
        'nombre': 'Nombre',
        'local': 'Local',
        'gusto': 'Gusto',
        'rating': 'Rating',
        'review': 'Review',
        'notas': 'Notas'
        })
