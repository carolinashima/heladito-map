import streamlit as st
from st_social_media_links import SocialMediaIcons
import matplotlib.pyplot as plt
import datetime
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

st.subheader('Stats')
st.write(t['3_text1'])

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


# convert to datetime
sorted_df['fecha'] = pd.to_datetime(sorted_df['fecha'], format="%Y.%m.%d")
sorted_df['year'] = sorted_df['fecha'].dt.year
years = sorted(sorted_df['year'].unique())
options = [t['3_yearselect1']] + years

selected_year = st.selectbox(t['3_yearselect'], options)
if selected_year == t['3_yearselect1']:
    filtered_df = sorted_df
else:
    filtered_df = sorted_df[sorted_df['year'] == selected_year]

st.write(t['3_text2'])
# show some metrics: n gustos, n heladerias
n_heladerias = filtered_df['nombre'].nunique()
n_gustos     = filtered_df['gusto'].nunique()
# display in columns
col1, col2 = st.columns(2)
col1.metric(t['3_nshops'], n_heladerias)
col2.metric(t['3_nflavours'], n_gustos)

with st.expander(t['3_rank_title']):
    top_n = 10
    ranking = (
        filtered_df
        .groupby(["gusto","nombre"])["rating"]
        .mean()
        .reset_index()
        .sort_values(by='rating',ascending=False)
        .head(top_n)
    )
    
    st.write(t['3_rank_text'])
    for i, row in enumerate(ranking.itertuples(), start=1):
        st.write(
            f"{i}. **{row.gusto}** "
            f"({row.nombre}, {row.rating:.2f})"
        )
    
with st.expander(t['3_scoredistr']):
    st.write(t['3_scoredistr_text'])
    fig, ax = plt.subplots()
    bins = np.arange(1, 6, 0.5)
    ax.hist(filtered_df['rating'], bins=bins, color='thistle', align='mid', rwidth=0.8)
    ax.set_xlabel('Score')
    ax.set_ylabel('Count')
    plt.tight_layout()
    st.pyplot(fig)

with st.expander(t['3_creamsorbet']):
    counts = filtered_df['tipo'].value_counts()
    fig, ax = plt.subplots()
    ax.barh(counts.index, counts.values, color='thistle')
    ax.set_xlabel('Count')
    ax.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig)

with st.expander(t['3_category']):
    st.write(t['3_category_text'])
    counts = filtered_df['category'].value_counts()
    fig, ax = plt.subplots()
    ax.barh(counts.index, counts.values, color='thistle')
    ax.set_xlabel('Count')
    ax.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig)

with st.expander(t['3_baseflavour']):
    st.write(t['3_baseflavour_text'])
    counts = filtered_df['base'].value_counts().head(15)
    fig, ax = plt.subplots()
    ax.barh(counts.index, counts.values, color='thistle')
    ax.set_xlabel('Count')
    ax.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig)

with st.expander(t['3_extrastoppings']):
    st.write(t['3_extrastoppings_text'])
    counts = filtered_df['cositos'].value_counts().head(10)
    fig, ax = plt.subplots()
    ax.barh(counts.index, counts.values, color='thistle')
    #ax.set_xticks(range(0, max(counts.values) + 1))
    ax.set_xlabel('Count')
    ax.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig)