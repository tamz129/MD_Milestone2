import streamlit as st
import eda
import prediction

st.set_page_config(
    layout='wide',
    initial_sidebar_state='expanded',
    page_title='Germany Used Car Price Prediction'
)

page = st.sidebar.selectbox('Pilih Halaman', ('EDA','Prediction'))
if page == 'EDA':
    eda.run()
else:
    prediction.run()