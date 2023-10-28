import streamlit as st
import os

st.set_page_config(layout="wide")

script_directory = os.path.dirname(__file__)
html_file_path = os.path.join(script_directory, "..", "EmotionAnalysis_HTML.html")

st.header("Jupyter Notebook")
# Read the HTML content from the file
with open(html_file_path,encoding="utf-8") as file:

    html_content = file.read()

# Display the HTML content
st.components.v1.html(html_content, width=1000, height=18000)