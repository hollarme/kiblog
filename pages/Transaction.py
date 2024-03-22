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
                        
                    t_df = st.session_state['pro_trans_table']
                    put_data('FarmTransaction', st.session_state["tran_data_df"].to_dict("records"))
                    st.session_state["Tweight"] = 0
                    st.session_state["Tunits"] = 0
                    st.session_state["Tunit_price"] = 0
                    st.session_state["Ttotal_price"] = 0
                    st.session_state["Tpaid"] = False
                    st.session_state["Tpaid_to"] = "Me"
                    st.session_state["Tmethod"] = "POS"
                    st.session_state["note_text_area"] = ""
                    # st.session_state["data_df"].loc[(st.session_state["data_df"]['Category']==t_df['Category'])&(st.session_state["data_df"]['Product']==t_df['Product'])&(st.session_state["data_df"]['Type']==t_df['Type']),'Units'] = st.session_state['pro_trans_table']['Units Left']
                    
        
            if interface=='Table Interface':
                b_df = st.session_state["data_df"]
                b_df = b_df[pd.to_datetime(b_df['Date']).dt.date == datetime.date(datetime.now())]
        
                st.session_state["tran_data_df"] = pd.DataFrame(get_data('FarmTransaction'))
        
                if st.session_state["tran_data_df"].empty:
                    st.session_state["tran_data_df"] = pd.DataFrame(
                        {
                            "Category": [""],
                            "Product": [""],
                            "Type": [""],
                            "Weight(kg)":[0],
                            "Units":[0],
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
                        "Weight(kg)":  st.column_config.NumberColumn(required=True, default=0),
                        "Unit Price(N)":  st.column_config.NumberColumn(required=True, default=0),
                        "Total Price(N)":  st.column_config.NumberColumn(required=True, default=0),
                        "Paid": st.column_config.CheckboxColumn(required=True, default=False),
                        "Payment Method":st.column_config.SelectboxColumn(required=True, options=('POS','Cash', 'Transfer')),
                        "Payment Received By":st.column_config.SelectboxColumn(required=True, options=('Me','Farm Fresh', 'Teas by Bella', 'Island Food Mart')),
                    },
                    
                    num_rows="fixed" if sortable else "dynamic",
                    key="TranslistTable",
                    on_change=update_transaction_table
                )
    
            elif interface == 'MitoSheet Interface':
                dataframe, code = spreadsheet(st.session_state["tran_data_df"])
                st.code(code)
        
            else:
                i_df = st.session_state["data_df"]
                i_df = i_df[pd.to_datetime(i_df['Date']).dt.date == datetime.date(datetime.now())]
                category = st.selectbox("select the product category", set(i_df['Category'].tolist()))
                product = st.selectbox("select the product", set(i_df.loc[i_df['Category']==category]['Product'].tolist()))
                types = st.selectbox("select the product type if available", set(i_df.loc[(i_df['Category']==category)&(i_df['Product']==product)]['Type'].tolist()))
                i_df.set_index(['Category', 'Product', 'Type'], inplace=True)
                weight = st.number_input("Enter the products weight in kg", value=0, key="Tweight")
                units = st.number_input("Number of units sold", value=0, key="Tunits")
                unit_price = st.number_input("Enter the unit price", value=i_df.loc[(category, product, types)]['Unit Price'] if category else 0, key="Tunit_price")
                total_price = st.number_input("Total price of the commodity", value=unit_price*weight if weight else unit_price*units, key="Ttotal_price")
                paid = st.checkbox("Has the product been paid for?", value=False, key="Tpaid")
                method = st.selectbox("Payment Method", ('POS','Cash', 'Transfer'), key="Tmethod")
                paid_to = st.selectbox("Payment Received By", ('Me','Farm Fresh', 'Teas by Bella', 'Island Food Mart'), key="Tpaid_to")
                date = st.date_input(label="Enter start date") 
                time = datetime.time(datetime.now())#st.time_input('', value="now", disabled=True)
                dt = datetime.combine(date, time)#.isoformat()
                note = st.text_area("Enter extra information", key="note_text_area")
                
                # units_left = i_df.loc[(category, product, types)]['Units'] - units
                
                st.session_state['pro_trans_table'] = {'Category': category, 'Product': product, 'Type': types, 'Weight(kg)': weight,'Units': units, 'Note': note, "Unit Price(N)": unit_price, "Total Price(N)": total_price, "Paid": paid, 'Date':dt, "Payment Received By": paid_to, "Payment Method": method}#, 'Units Left': units_left}

except KeyError:
    st.switch_page('Home.py')
    
    
# b_df = b_df[pd.to_datetime(b_df['Date']).dt.date == datetime.date(datetime.now())].set_index(['Category', 'Product', 'Type'])
# # st.write(b_df.set_index(['Category', 'Product', 'Type'], inplace=True))
# # st.write(b_df.query(f'Category =={category} & Product=={product} & Type=={types}'))
# st.write(b_df.loc[(category, product, types)]['Unit Price'])

# st.write(units)

# p_df = st.session_state["data_df"]
# p_df.loc[(p_df['Category']==category)&(p_df['Product']==product)&(p_df['Type']==types),'Units'] = 100
# st.write(p_df)