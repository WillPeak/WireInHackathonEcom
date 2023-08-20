import streamlit as st
import pandas as pd
from adapters.api import get_products

def usernameCallback():
    st.session_state.disabled = True

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.username = ""

if st.session_state.disabled == False:
    username = st.text_input(
        'Username',
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        key="username",
        on_change=usernameCallback
    )

if st.session_state.disabled == True:

    if st.session_state.username != "":

        products = get_products(st.session_state.username).sort_values(['score'], ascending=False)

        image_link = "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png"

        st.write("""
        # Advanced E-Commerce.com
        """)

        st.write("Profile page: " + st.session_state.username)

        col_count = 3  
        cols = st.columns(col_count)

        i = 0
        for j in range(len(products)):
            with st.container():
                with cols[i]:
                    st.write(products['name'].values[j])
                    st.image(image_link, width=200)

                if i == col_count-1:
                    i = 0
                else:
                    i += 1
