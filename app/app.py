import streamlit as st
import numpy as np
import pandas as pd
from flight_tracker import flight_tracker
import os
from dotenv import load_dotenv

# load env variable
load_dotenv()

# call API keys
api_key_aviation_stack = os.environ("API_KEY_AVIATION_STACK")
api_key_flightera = os.environ("API_KEY_FLIGHTERA")

st.title('Find the best flight for your travel')

# type origin airport (iata)
st.text_input("Where are you flying from? (IATA code e.g. CGK, KUL)", key="airport_depart_iata")

# type destination airport (iata)
st.text_input("Where are you flying to? (IATA code e.g., CGK, KUL)", key="airport_arrival_iata")

f"You are flying from {st.session_state.airport_depart_iata} to {st.session_state.airport_arrival_iata}" if st.session_state.airport_depart_iata and st.session_state.airport_arrival_iata else st.write('*You have not selected an origin and destination airport*')

button_a = st.button('Search flights')

if button_a:
    ft = flight_tracker(
        origin=st.session_state.airport_depart_iata, 
        destination=st.session_state.airport_arrival_iata, 
        api_key_aviation_stack=api_key_aviation_stack, 
        api_key_flightera=api_key_flightera)

    a = ft.list_flights()
    c = ft.get_delay_stat().rename(columns = {'flnr':'flight_no'})

    d = pd.merge(a,c, on='flight_no', how='inner').rename(columns={
    'delay_30d':'delayed_last_30_days_pct',
    'cancelled_30d':'cancelled_last_30_days_pct',
    'avg_delay':'average_delay_mins'}).drop(columns=[
        'airport_depart_icao', 
        'airport_arrival_icao',
        'count_30d'])

    # convert to pct
    d['delayed_last_30_days_pct'] = d.delayed_last_30_days_pct*100
    d['cancelled_last_30_days_pct'] = d.cancelled_last_30_days_pct*100
    
    # best flight with no delay
    list_least_delay = d[d.delayed_last_30_days_pct == d.delayed_last_30_days_pct.min()].flight_no.to_list()
    list_least_delay_freq = d[d.flight_no.isin(list_least_delay)].delayed_last_30_days_pct.to_list()

    # worst flight with most frequent delay
    list_most_delay = d[d.delayed_last_30_days_pct == d.delayed_last_30_days_pct.max()].flight_no.to_list()
    list_most_delay_freq = d[d.flight_no.isin(list_most_delay)].delayed_last_30_days_pct.to_list()

    # output to streamlit
    st.write(f"best flight codes with least delay is/are {list_least_delay}, with delay frequency of {list_least_delay_freq} %.")

    st.write(f"worst flight codes with most delay is/are {list_most_delay}, with delay frequency of {list_most_delay_freq} %.")

    st.write(d)
    
    
