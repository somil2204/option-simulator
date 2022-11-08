import pandas as pd
import streamlit as st
from os import listdir

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]






def highlight_cols(s):
    color = 'red'
    return 'color: %s' % color


def get_option_data(curent_time_data,candle_type):
    call_data = curent_time_data.filter(regex="C_"+candle_type)
    call_data.columns = [x[0:5] for x in call_data.columns.to_list()]
    put_data = curent_time_data.filter(regex="P_"+candle_type)
    put_data.columns = [x[0:5] for x in put_data.columns.to_list()]
    call_data = pd.melt(call_data,value_name="call_"+candle_type,var_name="strike")
    put_data = pd.melt(put_data,value_name="put_"+candle_type,var_name="strike")
    merged_data = call_data.merge(put_data,on="strike")
    return merged_data

#option_data = df.filter(regex="P_|C_")
def get_option_chain_at(t):
    curent_time_data = df.loc[df['time']==t]
    current_candle_time.header(t)
    index_value.header("Index value = {}".format(curent_time_data["close"].iloc[-1]))
    close_data = get_option_data(curent_time_data,"close")
    open_data = get_option_data(curent_time_data,"open")
    high_data = get_option_data(curent_time_data,"high")
    low_data = get_option_data(curent_time_data,"low")
    merge1 = close_data.merge(open_data,on="strike")
    merge2 = high_data.merge(low_data,on="strike")
    merged_data =merge1.merge(merge2,on="strike")
    merged_data = merged_data[["put_low","put_high","put_open","put_close","strike","call_close","call_open","call_high","call_low"]]
    
    merged_data = merged_data.style.applymap(highlight_cols, subset=['strike'])


    option_chain.dataframe(merged_data)

filename = st.sidebar.selectbox("Select Date",find_csv_filenames("data/"))


df= pd.read_csv("data/"+filename)

time_list = df['time'].to_list()
time_value = st.sidebar.selectbox("Select Time",sorted(time_list))
go_to = st.sidebar.button("GoTo")



submit1 =st.sidebar.button("Previous")
submit2 =st.sidebar.button("Next")



current_candle_time = st.empty()

index_value = st.empty()

option_chain = st.empty()





if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if go_to:
    st.session_state.current_index = time_list.index(time_value)
    get_option_chain_at(time_list[st.session_state.current_index])

if submit1:
    st.session_state.current_index -= 1
    
    get_option_chain_at(time_list[st.session_state.current_index])

if submit2:
    st.session_state.current_index += 1
    
    get_option_chain_at(time_list[st.session_state.current_index])