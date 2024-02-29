import streamlit as st
from matplotlib import pyplot as plt
import numpy as np
 
try: 
    # Creating dataset
    cars = ['Expenses','Income']
     
    data = [st.session_state["expx_data_df"]['Amount'].sum(), st.session_state["inc_data_df"]['Total Price(N)'].sum()]
     
    # Creating plot
    fig = plt.figure(figsize=(10, 7))
    plt.pie(data, labels=cars)
     
    st.pyplot(fig)

except KeyError:
    st.switch_page('Home.py')