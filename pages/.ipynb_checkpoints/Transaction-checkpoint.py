import streamlit as st
import pandas as pd
from datetime import datetime
from utils import get_data, put_data
from mitosheet.streamlit.v1 import spreadsheet

st.session_state['dt'] = datetime.now()#.isoformat()

try:
    if 'pro_trans_table' not in st.session_state:
        st.session_state['pro_trans_table'] = {}
    
    def update_transaction_table():
        if len(st.session_state.TranslistTable['deleted_rows']) > 0:
            st.session_state["tran_data_df"].drop(st.session_state.TranslistTable['deleted_rows'], inplace=True)
            put_data('FarmTransaction', st.session_state["tran_data_df"].to_dict("records"))
    
    with st.container(border=True):
        with st.status("", expanded=True) as status:
            dis, but = st.columns([0.9, 0.1])
    
            sortable = st.checkbox("Make table sortable?")
        
            interface = st.radio("",['Button Interface','Table Interface', 'MitoSheet Interface'],horizontal=True, key="trans_radio")
            
            with dis:
                st.subheader("Transactions from Product and Services")
            with but:
                if st.button("Save", key="pro_trans_but"):
                    if interface == 'Button Interface':
                        st.session_state["tran_data_df"].loc[len(st.session_state["tran_data_df"])] = st.session_state['pro_trans_table']
                    put_data('FarmTransaction', st.session_state["tran_data_df"].to_dict("records"))
        
            if interface=='Table Interface':
        
                st.session_state["tran_data_df"] = pd.DataFrame(get_data('FarmTransaction'))
        
                if st.session_state["tran_data_df"].empty:
                    b_df = st.session_state["data_df"]
                    b_df = b_df[pd.to_datetime(b_df['Date']).dt.date == datetime.date(datetime.now())]
                    st.session_state["tran_data_df"] = pd.DataFrame(
                        {
                            "Category": [""],
                            "Product": [""],
                            "Type": [""],
                            "Weight(kg)":[None],
                            "Units Sold":[0],
                            "Unit Price(N)": [0],
                            "Total Price(N)": [0],
                            'Date':[st.session_state['dt']],
                            "Paid":[None],
                            "Payment Method":[None],
                            "Payment Received By":[None],
                            "Note": [""]
                        }
                    )
            
                st.session_state["tran_data_df"] = st.data_editor(
                    st.session_state["tran_data_df"],
                    column_config={
                        "Category":  st.column_config.SelectboxColumn(required=True, options=set(b_df['Category'].tolist())),
                        "Product":  st.column_config.SelectboxColumn(required=True, options=set(b_df['Product'].tolist())),
                        "Type":  st.column_config.SelectboxColumn(required=True, options=set(b_df['Type'].tolist())),
                        "Date": st.column_config.DateColumn(required=True, default=datetime.date(datetime.now())),
                        "Units":  st.column_config.NumberColumn(required=True, default=0),
                        "Weight(kg)":  st.column_config.NumberColumn(required=False, default=0),
                        "Unit Price(N)":  st.column_config.NumberColumn(required=True, default=0),
                        "Total Price(N)":  st.column_config.NumberColumn(required=True, default=0),
                        "Paid": st.column_config.CheckboxColumn(required=True, default=False),
                        "Payment Method":st.column_config.SelectboxColumn(required=True, options=['POS','Cash', 'Transfer']),
                        "Payment Received By":st.column_config.SelectboxColumn(required=True, options=['Me','Farm Fresh', 'Teas by Bella', 'Island Food Mart']),
                    },
                    
                    num_rows="fixed" if sortable else "dynamic",
                    key="TranslistTable",
                    on_change=update_transaction_table
                )
    
            elif interface == 'MitoSheet Interface':
                dataframe, code = spreadsheet(st.session_state["tran_data_df"])
                st.code(code)
        
            else:
                b_df = st.session_state["data_df"]
                b_df = b_df[pd.to_datetime(b_df['Date']).dt.date == datetime.date(datetime.now())]
                category = st.selectbox("select the product category", set(b_df['Category'].tolist()))
                product = st.selectbox("select the product", set(b_df.loc[b_df['Category']==category]['Product'].tolist()))
                type = st.selectbox("select the product type if available", set(b_df.loc[(b_df['Category']==category)&(b_df['Product']==product)]['Type'].tolist()))
                weight = st.number_input("Enter the products weight in kg", value=None, key="Tweight")
                units = st.number_input("Number of units sold", key="Tunits")
                unit_price = st.number_input("Enter the unit price", value=b_df.loc[(b_df['Category']==category)&(b_df['Product']==product)&(b_df['Type']==type)]['Unit Price'] if category else 0, key="Tunit_price")
                total_price = st.number_input("Total price of the commodity", value=unit_price*units, key="Ttotal_price")
                paid = st.checkbox("Has the product been paid for?", value=False, key="Tpaid")
                method = st.selectbox("Payment Method", ['POS','Cash', 'Transfer']),
                paid_to = st.selectbox("Payment Received By", ['Me','Farm Fresh', 'Teas by Bella', 'Island Food Mart']),
                date = st.date_input(label="Enter start date") 
                time = datetime.time(datetime.now())#st.time_input('', value="now", disabled=True)
                dt = datetime.combine(date, time)#.isoformat()
                note = st.text_area("Enter extra information")
                
                st.session_state['pro_trans_table'] = {'Category': category, 'Product': product, 'Type': type, 'Weight(kg)': weight,'Units': units, 'Date':st.session_state['dt'], 'Note': note, "Unit Price(N)": unit_price, "Total Price(N)": total_price, "Paid": paid, 'Date':dt}

except KeyError:
    st.switch_page('Home.py')