import streamlit as st
from pages import home, big_balers, windrowers
from multipage import MultiPage

# Dashboard Config
st.set_page_config(
    page_title="BRIM Dashboard",
    page_icon="/Users/mac/Desktop/BRIM-DATA/UCC_DASHBOARD/data/brim_logo.png",
    layout="wide"
)

# Create an instance of the app
app = MultiPage()

# Add all your applications (pages) here
app.add_page("All Data", home.app)
app.add_page("Big Balers", big_balers.app)
app.add_page('Windrowers', windrowers.app)

# The main app
app.run()
