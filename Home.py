import streamlit as st
from utils import init_connection, get_data
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Kib Tool", layout="wide") 

if 'client' not in st.session_state:
    st.session_state['client'] = init_connection()
    
if 'db' not in st.session_state:
    st.session_state['db'] = st.session_state['client'].kibtoolDB

if 'collection' not in st.session_state:
    st.session_state['collection'] = ''

if 'dt' not in st.session_state:
    st.session_state['dt'] = datetime.now()#.isoformat()

    
# def change_collection():
#     st.session_state['collection'] = st.session_state['db'][record]

rec, ana = st.columns([0.7,0.3])

with ana:
    with st.container(border=True):
        d = st.date_input("What record year are you interested in?", datetime.today())

        period = st.radio(
            "Over which period?",
            ["***Q1***", "***Q2***", "***Q3***", "***Q4***", "***H1***", "***H2***", "***Y***"],
            captions = ["Jan-Mar", "Apr-Jun", "Jul-Sept", "Oct-Dec", "Jan-Jun", "Jul-Dec", "Jan-Dec"], horizontal=True)

        record = f"record_{d.year}_{period.replace('*','')}"

        st.session_state['collection'] = record

if 'data_df' not in st.session_state:
    st.session_state["data_df"] = pd.DataFrame(get_data('FarmSetup_ProductList'))

if 'data_df_cat' not in st.session_state:
    st.session_state["data_df_cat"] = pd.DataFrame(get_data('FarmSetup_ProductCat'))
    
if 'exp_data_df_cat' not in st.session_state:
    st.session_state["exp_data_df_cat"] = pd.DataFrame(get_data('FarmSetup_ExpensesCat'))

if 'expx_data_df' not in st.session_state:
    st.session_state['expx_data_df'] = pd.DataFrame(get_data('FarmExpenses'))

if 'note_data_df' not in st.session_state:
    st.session_state['note_data_df'] = pd.DataFrame(get_data('FarmNotes'))

if 'opr_data_df' not in st.session_state:
    st.session_state['opr_data_df'] = pd.DataFrame(get_data('FarmOperation'))

if 'op_data_df' not in st.session_state:
    st.session_state['op_data_df'] = pd.DataFrame(get_data('FarmOperationList'))

if 'lab_data_df' not in st.session_state:
    st.session_state['lab_data_df'] = pd.DataFrame(get_data('FarmLabourer'))

if 'inc_data_df' not in st.session_state:
    st.session_state['inc_data_df'] = pd.DataFrame(get_data('FarmIncome'))
    
with rec:    
    with st.container(border=True):
        home_tab, income_tab, expenses_tab, note_tab = st.tabs(['Home', 'Income', 'Expenses', 'Note'])

        with home_tab:
            pass

        with income_tab:
            pass

        with expenses_tab:
            pass

        with note_tab:
            pass

