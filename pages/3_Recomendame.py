from types import CoroutineType
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from st_social_media_links import SocialMediaIcons
from datetime import datetime

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

st.title("Recomendame algo!")
st.write('''Si conocés alguna heladería/gustos que debería probar,
porfa llená el formulario así lo tengo en cuenta. Si no querés que figure
en el mapita porque te da vergüenza (e.g. me recomendás menta granizada
o quinotos al whisky), todo bien.

En lo posible dejame un link a Google Maps, Open Street Map, etc.! 🙏''')

# connect to google sheets
conn = st.connection("gsheets", type=GSheetsConnection)

existing_data = conn.read(worksheet="form_input", usecols=list(range(4)))
existing_data = existing_data.dropna(how='all')

#st.dataframe(existing_data) # print df

# form
with st.form(key = 'rec_form'):
    person    = st.text_input(label='Nombre (hacete cargo)')
    heladeria = st.text_input(label='Heladería *')
    city      = st.text_input(label='Ciudad (y país, si no es en Argentina)')
    text      = st.text_input(label='Qué me recomendás de este lugar? *')
    add_it    = st.radio(
        'Lo agrego al mapita de recomendaciones?',
        ["Sí",
        "No"],
        captions = ["Es una recomendación para el mundo entero! 🤗",
        "Me van a funar 🙈"]
    )

    submit_button = st.form_submit_button(label='Enviar')
    if submit_button:
        # check mandatory fields
        if not heladeria or not text:
            st.warning("Tenés que recomendar heladería y gusto che!")
            st.stop()
        else:
            time_now = datetime.now()
            # add the data by creating a new pandas df
            new_data = pd.DataFrame(
                [
                    {
                        "timestamp": time_now,
                        "person": person,
                        "heladeria": heladeria,
                        "city": city,
                        "text": text,
                        "add_it": add_it
                    }
                ]
            )

            # add to the existing data
            updated_data = pd.concat([existing_data, new_data],ignore_index=True)
            # update the sheet
            conn.update(worksheet="form_input", data = updated_data)
            st.write('Gracias por la recomendación! ❤️')