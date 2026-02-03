import streamlit as st
from st_social_media_links import SocialMediaIcons
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# plot settings
plt.rcParams.update({
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#DDDDDD",
    "axes.labelsize": 11,
    "axes.titlesize": 15,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "grid.alpha": 0.3,
})
plt.rcParams["font.family"] = "Helvetica"

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

sorted_df = st.session_state['df_tracker'][selected_cols].sort_values(by='fecha', ascending = False)
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

st.subheader('Stats')
st.write('''
Cuáles son mis gustos favoritos? Cuáles son los que más pido? La respuesta no los sorprenderá.
''')

# convert to datetime
sorted_df['fecha'] = pd.to_datetime(sorted_df['fecha'])
sorted_df['year'] = sorted_df['fecha'].dt.year
years = sorted(sorted_df['year'].unique())
options = ['Todos'] + years

selected_year = st.selectbox("Seleccioná un año:", options)
if selected_year == "Todos":
    filtered_df = sorted_df
else:
    filtered_df = sorted_df[sorted_df['year'] == selected_year]

st.write("""
A cuántas heladerías (sucursales agrupadas) fui y cuántos gustos diferentes pedí?
""")
# show some metrics: n gustos, n heladerias
n_heladerias = filtered_df['nombre'].nunique()
n_gustos     = filtered_df['gusto'].nunique()
# display in columns
col1, col2 = st.columns(2)
col1.metric("N° heladerías", n_heladerias)
col2.metric("N° gustos", n_gustos)

with st.expander("Ranking de gustos"):
    top_n = 10
    ranking = (
        filtered_df
        .groupby(["gusto","nombre"])["rating"]
        .mean()
        .reset_index()
        .sort_values(by='rating',ascending=False)
        .head(top_n)
    )
    
    st.write('''
    Cuáles fueron mis gustos favoritos? A igual puntaje, el orden es random!
    ''')
    for i, row in enumerate(ranking.itertuples(), start=1):
        st.write(
            f"{i}. **{row.gusto}** "
            f"({row.nombre}, {row.rating:.2f})"
        )
    
with st.expander("Distribución de puntajes"):
    st.write('''
    Del 1 al 5.
    ''')
    fig, ax = plt.subplots()
    bins = np.arange(1, 6, 0.5)
    ax.hist(filtered_df['rating'], bins=bins, color='thistle', align='mid', rwidth=0.8)
    ax.set_xlabel('Puntaje')
    ax.set_ylabel('Count')
    plt.tight_layout()
    st.pyplot(fig)

with st.expander("A la crema o al agua?"):
    st.write('''
        Puede ser que más de 1 fuera un mix.
    ''')
    counts = filtered_df['tipo'].value_counts()
    fig, ax = plt.subplots()
    ax.barh(counts.index, counts.values, color='thistle')
    #ax.set_xticks(range(0, max(counts.values) + 1))
    ax.set_xlabel('Count')
    ax.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig)

with st.expander("Categoría"):
    st.write('''
        Categorías típicas de heladería.
    ''')
    counts = filtered_df['category'].value_counts()
    fig, ax = plt.subplots()
    ax.barh(counts.index, counts.values, color='thistle')
    #ax.set_xticks(range(0, max(counts.values) + 1))
    ax.set_xlabel('Count')
    ax.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig)

with st.expander("Sabor base"):
    st.write('''
        El sabor con mayor porcentaje (a ojo) del gusto en cuestión.
        Algunos raris los pedí solo 1 vez así que solo muestro el top 15.
    ''')
    counts = filtered_df['base'].value_counts().head(15)
    fig, ax = plt.subplots()
    ax.barh(counts.index, counts.values, color='thistle')
    #ax.set_xticks(range(0, max(counts.values) + 1))
    ax.set_xlabel('Count')
    ax.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig)

with st.expander("Cositos extra dentro o sobre la crema"):
    st.write('''
        Puede ser que más de 1 fuera un mix.
        Solo el top 10!
    ''')
    counts = filtered_df['cositos'].value_counts().head(10)
    fig, ax = plt.subplots()
    ax.barh(counts.index, counts.values, color='thistle')
    #ax.set_xticks(range(0, max(counts.values) + 1))
    ax.set_xlabel('Count')
    ax.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig)
