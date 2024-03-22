import streamlit as st
import pandas as pd
from datetime import datetime
from utils import get_data, put_data
from mitosheet.streamlit.v1 import spreadsheet

st.session_state['dt'] = datetime.now()#.isoformat()

try:

    if 'expx_list_table' not in st.session_state:
        st.session_state['expx_list_table'] = {}
    
    def update_expenses_table(args):
        status = args
        status.update(label="uploading data...", state="running")
        if len(st.session_state.explistTable['deleted_rows']) > 0:
            st.session_state["expx_data_df"].drop(st.session_state.explistTable['deleted_rows'], inplace=True)
            put_data('FarmExpenses', st.session_state["expx_data_df"].to_dict("records"))
        status.update(label="upload complete!", state="complete")
    
    
    with st.container(border=True):
        with st.status("", expanded=True) as status:
            dis, but = st.columns([0.90, 0.10])
    
            sortable = st.checkbox("Make table sortable?")
        
            interface = st.radio("",['Button Interface','Table Interface', 'MitoSheet Interface'],horizontal=True, key="expx_radio")
            
            with dis:
                st.subheader("List of Expenses")
            with but:
                if st.button("Save", key="exp list"):
                    status.update(label="uploading data...", state="running")
                    if interface == 'Button Interface':
                        st.session_state["expx_data_df"].loc[len(st.session_state["expx_data_df"])] = st.session_state['expx_list_table']
                    put_data('FarmExpenses', st.session_state["expx_data_df"].to_dict("records"))
                    status.update(label="upload complete!", state="complete")
                    st.session_state["amount"] = 0
                    st.session_state["exp_text_area"] = ""
                    
    
        
            if interface == 'Table Interface':
                
                st.session_state["expx_data_df"] = pd.DataFrame(get_data('FarmExpenses'))
                
                if st.session_state["expx_data_df"].empty:
                    st.session_state["expx_data_df"] = pd.DataFrame(
                        {
                            "Category": [""],
                            "Expenses":[""],
                            "Type": [""],
                            "Amount": [0],
                            "Direction": ["Out"], #is it going out or coming in to pay for the machines/other capital expenditures
                            "Date":[st.session_state['dt']],
                            "Note": [""]
                        }
                    )
        
                st.session_state["expx_data_df"] = st.data_editor(
                    st.session_state["expx_data_df"],
                    column_config={
                        "Category":  st.column_config.SelectboxColumn(required=True, options=set(st.session_state["exp_data_df_cat"]['Category'].tolist())),
                        "Type":  st.column_config.SelectboxColumn(required=True, options=set(st.session_state["exp_data_df_cat"]['Type'].tolist())),
                        "Expenses":  st.column_config.SelectboxColumn(required=True, options=set(st.session_state["exp_data_df_cat"]['Expenses'].tolist())),
                        "Note": st.column_config.TextColumn(required=True),
                        "Direction": st.column_config.SelectboxColumn(required=True, default="Out", options=['In', 'Out']),
                        "Date": st.column_config.DateColumn(required=True, default=datetime.date(datetime.now())),
                        "Amount": st.column_config.NumberColumn(required=True, default=0)
                    },
                    num_rows="fixed" if sortable else "dynamic",
                    key="explistTable",
                    on_change=update_expenses_table,
                    args=[status]
                )
            elif interface == 'MitoSheet Interface':
                dataframe, code = spreadsheet(st.session_state["expx_data_df"])
                st.code(code)
            else:
                b_df = st.session_state["exp_data_df_cat"]
                category = st.selectbox("select the expenses category", set(b_df['Category'].tolist()))
                expenses = st.selectbox("select the expenses", set(b_df.loc[b_df['Category']==category]['Expenses'].tolist()))
                types = st.selectbox("select the expenses type if available", set(b_df.loc[(b_df['Category']==category)&(b_df['Expenses']==expenses)]['Type'].tolist()))
                direction = st.selectbox('Is the money paid out or into the business?', options=['Out', 'In'])
                amount = st.number_input("Enter the worth of the expenses", value=0, key="amount")
                date = st.date_input(label="Enter start date") 
                time = datetime.time(datetime.now())#st.time_input('', value="now", disabled=True)
                dt = datetime.combine(date, time)#.isoformat()
                note = st.text_area("Enter extra information", key='exp_text_area')
                
                st.session_state['expx_list_table'] = {'Category': category, 'Expenses': expenses, 'Type': types, 'Date':st.session_state['dt'], 'Note': note, "Amount": amount, 'Direction': direction, 'Date': dt}

except KeyError:
    st.switch_page('Home.py')
