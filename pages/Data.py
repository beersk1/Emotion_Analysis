import streamlit as st
st.set_page_config(layout="wide")
import os 

# Function to load a text file based on the selected option
def load_text_file(option):
    script_directory = os.path.dirname(__file__)
    path = os.path.join(script_directory, "..")
    file_path = f"{path}/{option}.txt"
    with open(file_path, 'r') as file:
        content = ''.join([next(file) for _ in range(25)])  # Read the first 25 lines
    return content

# Streamlit App
st.title("Load Data Text Files")


# Dropdown menu with three options
selected_option = st.selectbox("Select an Option", ["train", "test", "val"])

# Display the selected option
st.write(f"You selected: {selected_option}")

# Load and display the text file content based on the selected option
if selected_option:
    text_content = load_text_file(selected_option)
    st.subheader("First 25 Lines of Text File")
    lines = text_content.split('\n')  # Split the content into lines
    for line in lines:
        st.write(line)
