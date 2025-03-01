import streamlit as st
from utils import init_connection, get_data
from datetime import datetime
import pandas as pd
from millify import prettify


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

try:

    with ana:
        with st.container(border=True):
            d = st.date_input("What record year are you interested in?", None)

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

    if 'tran_data_df' not in st.session_state:
        st.session_state["tran_data_df"] = pd.DataFrame(get_data('FarmTransaction'))
        
    with rec:    
        with st.container(border=True):
            home_tab, income_tab, expenses_tab, note_tab = st.tabs(['Home', 'Income', 'Expenses', 'Note'])

            with home_tab:
                pass

            with income_tab:
                try:
                    b_df = st.session_state["inc_data_df"]
                    xl = b_df['Category'].tolist()
                    xl.insert(0,"")
                    category = st.selectbox("select the expenses category", set(xl), key='inccC')
                    xl = b_df.loc[b_df['Category']==category]['Product'].tolist()
                    xl.insert(0,"")
                    prod = st.selectbox("select the product", set(xl), key='inccP')
                    xl = b_df.loc[(b_df['Category']==category)&(b_df['Product']==prod)]['Type'].tolist()
                    xl.insert(0,"")
                    types = st.selectbox("select the product type if available", set(xl), key='inccT')
                    
                    label = ""
                    
                    if category:
                        b_df = b_df[b_df['Category'].str.contains(category, na=False, regex=False)]
                        label = ""#":black_small_square:" + category + ":red[Cost]" + ":black_small_square:" 
                    if prod:
                        b_df = b_df[b_df['Product'].str.contains(prod, na=False, regex=False)]
                        label = ""#":black_small_square:" + prod + ":red[Cost]" + ":black_small_square:" 
                    if types:
                        b_df = b_df[b_df['Type'].str.contains(types, na=False, regex=False)]
                        label =  ""#":black_small_square:" + types + ":red[Cost]" + ":black_small_square:"
                        
                                            
                    col1, col2, col3 = st.columns(3)
                    
                    col2.metric(label=label, value=prettify(b_df['Total Price(N)'].sum()))
                except KeyError:
                    pass

            with expenses_tab:
                try:
                    b_df = st.session_state["expx_data_df"]#st.session_state["exp_data_df_cat"]
                    xl = b_df['Category'].tolist()
                    xl.insert(0,"")
                    category = st.selectbox("select the expenses category", set(xl))
                    xl = b_df.loc[b_df['Category']==category]['Expenses'].tolist()
                    xl.insert(0,"")
                    expenses = st.selectbox("select the expenses", set(xl))
                    xl = b_df.loc[(b_df['Category']==category)&(b_df['Expenses']==expenses)]['Type'].tolist()
                    xl.insert(0,"")
                    types = st.selectbox("select the expenses type if available", set(xl))
                    
                    label = ""
                    
                    if category:
                        b_df = b_df[b_df['Category'].str.contains(category, na=False, regex=False)]
                        label = ""#":black_small_square:" + category + ":red[Cost]" + ":black_small_square:" 
                    if expenses:
                        b_df = b_df[b_df['Expenses'].str.contains(expenses, na=False, regex=False)]
                        label = "" #":black_small_square:" + expenses + ":red[Cost]" + ":black_small_square:" 
                    if types:
                        b_df = b_df[b_df['Type'].str.contains(types, na=False, regex=False)]
                        label = ""#":black_small_square:" + types + ":red[Cost]" + ":black_small_square:"
                        
                                            
                    col1, col2, col3 = st.columns(3)
                    
                    col2.metric(label=label, value=prettify(b_df['Amount'].sum()))
                except KeyError:
                    pass

            with note_tab:
                pass
except AttributeError:
    st.warning('Enter the year and period of interest')
