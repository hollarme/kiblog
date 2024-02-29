import streamlit as st
import pandas as pd
from datetime import datetime
from utils import get_data, put_data

st.session_state['dt'] = datetime.now()#.isoformat()
try:
    
    if 'opr_table' not in st.session_state:
        st.session_state['opr_table'] = {}
    
    def update_opr_table():
        if len(st.session_state.oprTable['deleted_rows']) > 0:
            st.session_state["opr_data_df"].drop(st.session_state.oprTable['deleted_rows'], inplace=True)
            put_data('FarmOperation', st.session_state["opr_data_df"].to_dict("records"))
    
    with st.status("", expanded=True) as status:
        main, cat = st.columns([0.70,0.30])
        with cat:
            with st.container(border=True):
                dis, but = st.columns([0.60, 0.40])
                with dis:
                    st.empty()
                with but:
                    if st.button("Save", key="lab_opr"):
                        # with st.spinner('Wait for it...'):
                        put_data('FarmLabourer', st.session_state["lab_data_df"].to_dict("records"))
                        put_data('FarmOperationList', st.session_state["op_data_df"].to_dict("records"))
        
                st.write("**List of Labourers**")
                st.session_state["lab_data_df"] = pd.DataFrame(get_data('FarmLabourer'))
                
                if st.session_state["lab_data_df"].empty:
        
                    st.session_state["lab_data_df"] = pd.DataFrame(
                        {
                            "Personnel":[""],
                            "Arrival Date": [st.session_state['dt']]
                        }
                    )
        
                st.session_state["lab_data_df"] = st.data_editor(
                    st.session_state["lab_data_df"],
                    column_config={
                        "Personnel":  st.column_config.TextColumn(),
                        "Arrival Date": st.column_config.DatetimeColumn(required=True, default=st.session_state['dt']),
                    },
                    num_rows="dynamic",
                    key = "labTable"
        
                )
        
                st.write("**Operation List**")
                st.session_state["op_data_df"] = pd.DataFrame(get_data('FarmOperationList'))
                
                if st.session_state["op_data_df"].empty:
        
                    st.session_state["op_data_df"] = pd.DataFrame(
                        {
                            "Operation":[""],
                            "Weight": [""]
                        }
                    )
        
                st.session_state["op_data_df"] = st.data_editor(
                    st.session_state["op_data_df"],
                    column_config={
                        "Operation": st.column_config.TextColumn(required=True),
                        "Weight": st.column_config.SelectboxColumn(required=True, options=["single","double"])
                    },
                    num_rows="dynamic",
                    key = "opTable"
        
                )
        with main:
            with st.container(border=True):
                dis, but = st.columns([0.85, 0.15])
            
                interface = st.radio("",['Button Interface','Table Interface'],horizontal=True, key="opr_radio")
                
                with dis:
                    st.subheader("Operations")
                with but:
                    if st.button("Save", key="notes"):
                        if interface == 'Button Interface':
                            st.session_state["opr_data_df"].loc[len(st.session_state["opr_data_df"])] = st.session_state['opr_table']
                        put_data('FarmOperation', st.session_state["opr_data_df"].to_dict("records"))
            
                if interface == 'Table Interface':
                    
                    st.session_state["opr_data_df"] = pd.DataFrame(get_data('FarmOperation'))
                    
                    if st.session_state["opr_data_df"].empty:
                        st.session_state["opr_data_df"] = pd.DataFrame(
                            {
                                "Operation": [""],
                                "Personnel": [""],
                                "Alapin": [0.0],
                                "Date":[st.session_state['dt']],
                                "Note": [""]
                            }
                        )
            
                    st.session_state["opr_data_df"] = st.data_editor(
                        st.session_state["opr_data_df"],
                        column_config={
                            "Personnel": st.column_config.TextColumn(required=True),
                            "Operation": st.column_config.TextColumn(required=True),
                            "Alapin": st.column_config.NumberColumn(required=True),
                            "Note": st.column_config.TextColumn(required=False),
                            "Date": st.column_config.DateColumn(required=True, default=datetime.date(datetime.now())),
                        },
                        num_rows="dynamic",
                        key="oprTable",
                        on_change=update_opr_table
                    )
                else:
                    personnel = st.selectbox("select the personnel name", set(st.session_state["lab_data_df"]['Personnel'].tolist()), key="pers")
                    operation = st.selectbox("select the operation", set(st.session_state["op_data_df"]['Operation'].tolist()), key="opr")
                    alapin = st.number_input("Enter the number of alapin done", value=0.0)
                    date = st.date_input(label="Enter start date") 
                    time = datetime.time(datetime.now())#st.time_input('', value="now", disabled=True)
                    dt = datetime.combine(date, time)#.isoformat()
                    note = st.text_area("Enter additional information", key='opr_text_area')

                    # st.write(dt)
                    
                    st.session_state['opr_table'] = {'Date':st.session_state['dt'], 'Note': note, "Personnel":personnel, "Operation":operation, "Alapin":alapin, "Date":dt}
                    
except KeyError:
    st.switch_page('Home.py')