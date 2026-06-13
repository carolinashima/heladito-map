from types import CoroutineType
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from st_social_media_links import SocialMediaIcons
from datetime import datetime
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

social_media_icons.render(sidebar=True)

st.title(t['4_title'])
st.write(t['4_maintext'])

# connect to google sheets
conn = st.connection("gsheets", type=GSheetsConnection)

existing_data = conn.read(worksheet="form_input", usecols=list(range(4)))
existing_data = existing_data.dropna(how='all')

# form
with st.form(key = 'rec_form'):
    person    = st.text_input(label=t['4_form_name'])
    heladeria = st.text_input(label=t['4_form_shop'])
    #city      = st.text_input(label='Ciudad (y país, si no es en Argentina)')
    map       = st.text_input(label=t['4_form_maps'])
    text      = st.text_input(label=t['4_form_what'])
    add_it    = st.radio(
        t['4_form_add'],
        [t['4_form_add_yes'],
        t['4_form_add_no']],
        captions = [t['4_form_add_yes_sub'],
        t['4_form_add_no_sub']]
    )

    submit_button = st.form_submit_button(label=t['4_form_button'])
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
                        "map": map,
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