import streamlit as st
from page1 import main as page1
from page2 import main as page2
from page3 import main as page3
from page4 import main as page4

st.set_page_config(page_title="Multi-Page Streamlit App")

# Create a dictionary of page names and their respective functions
pages = {
    "Page 1": page1,
    "Page 2": page2,
    "Page 3": page3,
    "Page 4": page4,
}

# Add a sidebar for page selection
st.sidebar.title("Navigation")
selected_page = st.sidebar.selectbox("Go to", list(pages.keys()))

# Display the selected page
pages[selected_page]()
