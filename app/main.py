import streamlit as st

banky_page = st.Page(
    "st_frontend.py", title="Table View", icon=":material/table:")

pg = st.navigation([banky_page])
st.set_page_config(page_title="AI in Academic and Popular Media",
                   page_icon=":material/interactive_space:")
pg.run()