import streamlit as st
import pandas as pd
from datetime import datetime
from utils import get_data, put_data
# from mitosheet.streamlit.v1 import spreadsheet

st.session_state['dt'] = datetime.now()#.isoformat()

try:
    if 'pro_inc_table' not in st.session_state:
        st.session_state['pro_inc_table'] = {}
    
    def update_income_table(args):
        status = args
        status.update(label="uploading data...", state="running")
        if len(st.session_state.inclistTable['deleted_rows']) > 0:
            st.session_state["inc_data_df"].drop(st.session_state.inclistTable['deleted_rows'], inplace=True)
            put_data('FarmIncome', st.session_state["inc_data_df"].to_dict("records"))
        status.update(label="upload complete!", state="complete")
    
    with st.container(border=True):
        with st.status("", expanded=True) as status:
            dis, but = st.columns([0.9, 0.1])
    
            sortable = st.checkbox("Make table sortable?")
        
            interface = st.radio("",['Button Interface','Table Interface', 'MitoSheet Interface'],horizontal=True, key="inc_radio")
            
            with dis:
                st.subheader("Income from Product and Services")
            with but:
                if st.button("Save", key="pro_inc_but"):
                    status.update(label="uploading data...", state="running")
                    if interface == 'Button Interface':
                        st.session_state["inc_data_df"].loc[len(st.session_state["inc_data_df"])] = st.session_state['pro_inc_table']
                    put_data('FarmIncome', st.session_state["inc_data_df"].to_dict("records"))
                    status.update(label="upload complete!", state="complete")
                    st.session_state["weight"] = None
                    st.session_state["units"] = None
                    st.session_state["unit_price"] = None
                    st.session_state["total_price"] = 0
                    st.session_state["paid"] = False
                    st.session_state["inc_text_area"] = ""
                    
        
            if interface=='Table Interface':
        
                st.session_state["inc_data_df"] = pd.DataFrame(get_data('FarmIncome'))
        
                if st.session_state["inc_data_df"].empty:
                    st.session_state["inc_data_df"] = pd.DataFrame(
                        {
                            "Category": [""],
                            "Product": [""],
                            "Type": [""],
                            "Units Sold":[None],
                            "Weight(kg)":[None],
                            "Unit Price(N)": [None],
                            "Total Price(N)": [0],
                            'Date':[st.session_state['dt']],
                            "Paid":[None],
                            "Note": [""]
                        }
                    )
            
                st.session_state["inc_data_df"] = st.data_editor(
                    st.session_state["inc_data_df"],
                    column_config={
                        "Category":  st.column_config.SelectboxColumn(required=True, options=st.session_state["data_df_cat"]['Category'].tolist()),
                        "Product":  st.column_config.SelectboxColumn(required=True, options=st.session_state["data_df_cat"]['Product'].tolist()),
                        "Type":  st.column_config.SelectboxColumn(required=True, options=st.session_state["data_df_cat"]['Type'].tolist()),
                        "Date": st.column_config.DateColumn(required=True, default=datetime.date(datetime.now())),
                        "Units Sold":  st.column_config.NumberColumn(required=True, default=None),
                        "Weight(kg)":  st.column_config.NumberColumn(required=False, default=None),
                        "Unit Price(N)":  st.column_config.NumberColumn(required=True, default=None),
                        "Total Price(N)":  st.column_config.NumberColumn(required=True),
                        "Paid": st.column_config.CheckboxColumn(required=True, default=False)
                    },
                    
                    num_rows="fixed" if sortable else "dynamic",
                    key="inclistTable",
                    on_change=update_income_table,
                    args=[status]
                )

            elif interface == 'MitoSheet Interface':
                pass
                # dataframe, code = spreadsheet(st.session_state["inc_data_df"])
                # st.code(code)
        
            else:
                b_df = st.session_state["data_df_cat"]
                category = st.selectbox("select the product category", set(b_df['Category'].tolist()))
                product = st.selectbox("select the product", set(b_df.loc[b_df['Category']==category]['Product'].tolist()))
                types = st.selectbox("select the product type if available", set(b_df.loc[(b_df['Category']==category)&(b_df['Product']==product)]['Type'].tolist()))
                weight = st.number_input("Enter the products weight in kg", value=None, key="weight")
                units = st.number_input("Number of units sold", value=None, key="units")
                unit_price = st.number_input("Enter the unit price", value=None, key="unit_price")
                total_price = st.number_input("Total price of the commodity", key="total_price")
                paid = st.checkbox("Has the product been paid for?", value=False, key="paid")
                date = st.date_input(label="Enter start date") 
                time = datetime.time(datetime.now())#st.time_input('', value="now", disabled=True)
                dt = datetime.combine(date, time)#.isoformat()
                note = st.text_area("Enter extra information", key="inc_text_area")
                
                st.session_state['pro_inc_table'] = {'Category': category, 'Product': product, 'Type': types, 'Weight(kg)': weight,'Units Sold': units, 'Note': note, "Unit Price(N)": unit_price, "Total Price(N)": total_price, "Paid": paid, 'Date':dt}

except KeyError:
    st.switch_page('Home.py')
    
