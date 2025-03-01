import streamlit as st
import pandas as pd
from datetime import datetime
from utils import get_data, put_data
import numpy as np

#consider using records per year/half month/quarter/season
#consider gathering data about the rain, sun irridiance, soil information and herbs
#consider with market bought what
#consider the sources of our inputs with prices

try:
    
    if "pro_list_table" not in st.session_state:   
        st.session_state['pro_list_table'] = {}
    
    # if "exp_list_table" not in st.session_state:
    #     st.session_state['exp_list_table'] = {}
    
    st.session_state['dt'] = datetime.now()#.isoformat()
    
    st.header("Farm Setup")
    
    def update_product_table():
        if len(st.session_state.prolistTable['deleted_rows']) > 0:
            st.session_state["data_df"].drop(st.session_state.prolistTable['deleted_rows'], inplace=True)
            put_data('FarmSetup_ProductList', st.session_state["data_df"].to_dict("records"))
    
    
    with st.status("", expanded=True) as status:
        product, expense = st.tabs(['Farm Products/Services', 'Farm Expenses'])
        with product:
            main, cat = st.columns([0.60,0.40])
            with cat:
                with st.container(border=True):
                    dis, but = st.columns([0.70, 0.25])
                    with dis:
                        st.subheader("Product Categories")
                    with but:
                        if st.button("Save", key="pro_cat"):
                            put_data('FarmSetup_ProductCat', st.session_state["data_df_cat"].to_dict("records"))
                                        
                    st.session_state["data_df_cat"] = pd.DataFrame(get_data('FarmSetup_ProductCat'))
                    
                    if st.session_state["data_df_cat"].empty:
        
                        st.session_state["data_df_cat"] = pd.DataFrame(
                            {
                                "Category":[""],
                                "Product": [""],
                                "Type": [""]
                            }
                        )
        
                    st.session_state["data_df_cat"] = st.data_editor(
                        st.session_state["data_df_cat"],
                        column_config={
                            "Type":  st.column_config.TextColumn(),
                            "Category":  st.column_config.TextColumn(required=True),
                            "Product":  st.column_config.TextColumn(required=True)
                        },
                        num_rows="dynamic",
                        key = "pro_cat_table"
        
                    )
        
        
            with main:
                with st.container(border=True):
                    dis, but = st.columns([0.85, 0.15])
                    
                    interface = st.radio("",['Button Interface','Table Interface'],horizontal=True)
                    
                    with dis:
                        st.subheader("Product List")
                    with but:
                        if st.button("Save", key="pro_list_but"):
                            if interface == 'Button Interface':
                                st.session_state["data_df"].loc[len(st.session_state["data_df"])] = st.session_state['pro_list_table']
                            put_data('FarmSetup_ProductList', st.session_state["data_df"].to_dict("records"))
        
                    if interface == 'Table Interface':
                        
                        st.session_state["data_df"] = pd.DataFrame(get_data('FarmSetup_ProductList'))
                        
                        if st.session_state["data_df"].empty:
            
                            st.session_state["data_df"] = pd.DataFrame(
                                {
                                    "Category": [""],
                                    "Product": [""],
                                    "Type": [""],
                                    "Weight(kg)": [None],
                                    "Units":[None],
                                    "Unit Price":[0.0],
                                    'Date':[st.session_state['dt']],
                                    'Note':[""]
                                    # "Unit Price (N)": [""]
                                }
                            )
            
                        st.session_state["data_df"] = st.data_editor(
                            st.session_state["data_df"],
                            column_config={
                                "Category":  st.column_config.SelectboxColumn(required=True, options=set(st.session_state["data_df_cat"]['Category'].tolist())),
                                "Product":  st.column_config.SelectboxColumn(required=True, options=set(st.session_state["data_df_cat"]['Product'].tolist())),
                                "Type":  st.column_config.SelectboxColumn(required=True, options=set(st.session_state["data_df_cat"]['Type'].tolist())),
                                "Weight(kg)": st.column_config.NumberColumn(default=None),
                                "Units": st.column_config.NumberColumn(default=None),
                                "Unit Price":st.column_config.NumberColumn(default=0.0),
                                "Date": st.column_config.DateColumn(required=True, default=datetime.date(datetime.now())),
                                # "Note": st.column_config.TextColumn()
                            },
                            
                            num_rows="dynamic",
                            key="prolistTable",
                            on_change=update_product_table
                        )
                
#                         st.subheader("Product List After Transactions")
                
#                         or_df = st.session_state["data_df"][pd.to_datetime(st.session_state["data_df"]['Date']).dt.date == datetime.date(datetime.now())]
#                         co_df = st.session_state["tran_data_df"][pd.to_datetime(st.session_state["tran_data_df"]['Date']).dt.date == datetime.date(datetime.now())]
#                         co_df['Units'] *= -1
#                         co_df['Weight(kg)'] *= -1
#                         pp_df = pd.concat([or_df.loc[:,('Category', 'Product', 'Type', 'Weight(kg)','Units')], co_df.loc[:,('Category', 'Product', 'Type', 'Weight(kg)','Units')]])
#                         st.dataframe(pp_df.groupby(['Category', 'Product', 'Type']).sum())
        
                    else:
                        b_df = st.session_state["data_df_cat"]
                        category = st.selectbox("select the product category", set(b_df['Category'].tolist()))
                        product = st.selectbox("select the product", set(b_df.loc[b_df['Category']==category]['Product'].tolist()))
                        type = st.selectbox("select the product type if available", set(b_df.loc[(b_df['Category']==category)&(b_df['Product']==product)]['Type'].tolist()))
                        weight = st.number_input("Enter the products weight in kg")
                        unit = st.number_input("Number of units available")
                        unit_price = st.number_input("Enter the price for a single unit")
                        date = st.date_input(label="Enter start date") 
                        time = datetime.time(datetime.now())#st.time_input('', value="now", disabled=True)
                        dt = datetime.combine(date, time)#.isoformat()
                        note = st.text_area("Enter extra information")
                        
                        st.session_state['pro_list_table'] = {'Category': category, 'Product': product, 'Type': type, 'Weight(kg)': weight,'Units': unit, "Unit Price":unit_price,'Date':st.session_state['dt'], 'Note': note, "Date":dt}
        
        
        with expense:
            m1, cat, m2 = st.columns([0.25,0.50,0.25])
            with cat:
                with st.container(border=True):
                    dis, but = st.columns([0.80, 0.20])
                    with dis:
                        st.subheader("Expenses Categories")
                    with but:
                        if st.button("Save", key="exp cat"):
                            put_data('FarmSetup_ExpensesCat', st.session_state["exp_data_df_cat"].to_dict("records"))
                                
                    st.session_state["exp_data_df_cat"] = pd.DataFrame(get_data('FarmSetup_ExpensesCat'))
                    
                    if st.session_state["exp_data_df_cat"].empty:
            
                        st.session_state["exp_data_df_cat"] = pd.DataFrame(
                            {
                                "Category": [""],
                                "Expenses": [""],
                                "Type": [""]
                            }
                        )
            
                    st.session_state["exp_data_df_cat"] = st.data_editor(
                        st.session_state["exp_data_df_cat"],
                        column_config={
                            "Type":  st.column_config.TextColumn(),
                            "Category":  st.column_config.TextColumn(required=True),
                            "Expenses":  st.column_config.TextColumn(required=True)
                        },
                        num_rows="dynamic",
                        key="exp_cat_table"
            
                    )
                
        # st.subheader("Product List After Transactions")
                
        # or_df = st.session_state["data_df"][pd.to_datetime(st.session_state["data_df"]['Date']).dt.date == datetime.date(datetime.now())]
        # co_df = st.session_state["tran_data_df"][pd.to_datetime(st.session_state["tran_data_df"]['Date']).dt.date == datetime.date(datetime.now())]
        # co_df['Units'] *= -1
        # co_df['Weight(kg)'] *= -1
        # pp_df = pd.concat([or_df.loc[:,('Category', 'Product', 'Type', 'Weight(kg)','Units')], co_df.loc[:,('Category', 'Product', 'Type', 'Weight(kg)','Units')]])
        # st.dataframe(pp_df.groupby(['Category', 'Product', 'Type']).sum())

except KeyError:
    st.switch_page('Home.py')
    
        # with main:
        #     with st.container(border=True):
        #         dis, but = st.columns([0.85, 0.15])
    
        #         interface = st.radio("",['Button Interface','Table Interface'],horizontal=True, key="exp_radio")
                
        #         with dis:
        #             st.subheader("List of Expenses")
        #         with but:
        #             if st.button("Save", key="exp list"):
        #                 if interface == 'Button Interface':
        #                     st.session_state["exp_data_df"].loc[len(st.session_state["exp_data_df"])] = st.session_state['exp_list_table']
        #                 put_data('FarmSetup_ExpensesList', st.session_state["exp_data_df"].to_dict("records"))
    
        #         if interface == 'Table Interface':
                    
        #             st.session_state["exp_data_df"] = pd.DataFrame(get_data('FarmSetup_ExpensesList'))
                    
        #             if st.session_state["exp_data_df"].empty:
        #                 st.session_state["exp_data_df"] = pd.DataFrame(
        #                     {
        #                         "Category": [""],
        #                         "Expenses":[""],
        #                         "Type": [""],
        #                         # "Direction": [""], #is it going out or coming in to pay for the machines/other capital expenditures
        #                         "Date":[st.session_state['dt']],
        #                         "Note": [""]
        #                     }
        #                 )
        
        #             st.session_state["exp_data_df"] = st.data_editor(
        #                 st.session_state["exp_data_df"],
        #                 column_config={
        #                     "Category":  st.column_config.SelectboxColumn(required=True, options=set(st.session_state["exp_data_df_cat"]['Category'].tolist())),
        #                     "Type":  st.column_config.SelectboxColumn(required=True, options=set(st.session_state["exp_data_df_cat"]['Type'].tolist())),
        #                     "Expenses":  st.column_config.SelectboxColumn(required=True, options=set(st.session_state["exp_data_df_cat"]['Expenses'].tolist())),
        #                     "Note": st.column_config.TextColumn(required=True),
        #                     "Date": st.column_config.DateColumn(required=True, default=datetime.date(datetime.now()))
        #                 },
        #                 num_rows="dynamic",
        #                 key="explistTable",
        #                 on_change=update_expenses_table
        #             )
        #         else:
        #             b_df = st.session_state["exp_data_df_cat"]
        #             category = st.selectbox("select the expenses category", set(b_df['Category'].tolist()))
        #             expenses = st.selectbox("select the expenses", set(b_df.loc[b_df['Category']==category]['Expenses'].tolist()))
        #             type = st.selectbox("select the expenses type if available", set(b_df.loc[(b_df['Category']==category)&(b_df['Expenses']==expenses)]['Type'].tolist()))
        #             note = st.text_area("Enter extra information", key='exp_text_area')
                    
        #             st.session_state['exp_list_table'] = {'Category': category, 'Expenses': expenses, 'Type': type, 'Date':st.session_state['dt'], 'Note': note}
        
       
    

