import streamlit as st
import pandas as pd
from datetime import datetime
from utils import get_data, put_data

st.session_state['dt'] = datetime.now()#.isoformat()
try:
    
    if 'note_table' not in st.session_state:
        st.session_state['note_table'] = {}
    
    def update_note_table():
        if len(st.session_state.noteTable['deleted_rows']) > 0:
            st.session_state["note_data_df"].drop(st.session_state.noteTable['deleted_rows'], inplace=True)
            put_data('FarmNotes', st.session_state["note_data_df"].to_dict("records"))
    
    with st.status("", expanded=True) as status:
        with st.container(border=True):
            dis, but = st.columns([0.85, 0.15])
        
            interface = st.radio("",['Button Interface','Table Interface'],horizontal=True, key="note_radio")
            
            with dis:
                st.subheader("Notes")
            with but:
                if st.button("Save", key="notes"):
                    if interface == 'Button Interface':
                        st.session_state["note_data_df"].loc[len(st.session_state["note_data_df"])] = st.session_state['note_table']
                    put_data('FarmNotes', st.session_state["note_data_df"].to_dict("records"))
                    st.session_state["note_text_area"] = ""
        
            if interface == 'Table Interface':
                
                st.session_state["note_data_df"] = pd.DataFrame(get_data('FarmNotes'))
                
                if st.session_state["note_data_df"].empty:
                    st.session_state["note_data_df"] = pd.DataFrame(
                        {
                            
                            "Date":[st.session_state['dt']],
                            "Note": [""]
                        }
                    )
        
                st.session_state["note_data_df"] = st.data_editor(
                    st.session_state["note_data_df"],
                    column_config={
                        "Note": st.column_config.TextColumn(required=True),
                        "Date": st.column_config.DateColumn(required=True, default=datetime.date(datetime.now())),
                    },
                    num_rows="dynamic",
                    key="noteTable",
                    on_change=update_note_table
                )
            else:
                date = st.date_input(label="Enter start date") 
                time = datetime.time(datetime.now())#st.time_input('', value="now", disabled=True)
                dt = datetime.combine(date, time)#.isoformat()
                note = st.text_area("Enter the needed information", key='note_text_area')
                
                st.session_state['note_table'] = {'Date':dt, 'Note': note}
except KeyError:
    st.switch_page('Home.py')