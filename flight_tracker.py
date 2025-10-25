import pandas as pd
import numpy as np
import os
import requests

class flight_tracker:
    def __init__(self, origin, destination, api_key_aviation_stack, api_key_flightera):
        self.origin = origin
        self.destination = destination
        self.api_aviation = api_key_aviation_stack
        self.api_flightera = api_key_flightera
    
   
    def list_flights(self):
        
        url = "http://api.aviationstack.com/v1/flights"

        params = {
            'access_key':self.api_aviation,
            'dep_iata': self.origin,
            'arr_iata':self.destination
        }

        response = requests.get(url, params=params)

        b = response.json()['data']

        out_list=[]

        for x in range(0,len(b)):
            time_depart = b[x]['departure']['scheduled']
            airport_depart_icao = b[x]['departure']['icao']
            airport_arrival_icao = b[x]['arrival']['icao']
            flight_no = b[x]['flight']['iata']

            out = {'flight_no':flight_no,
                'time_depart':time_depart,
                'airport_depart_icao':airport_depart_icao,
                'airport_arrival_icao':airport_arrival_icao
            }

            out_list.append(out)
        
        out_df = pd.DataFrame(out_list)
        out_df['time_depart'] = pd.to_datetime(out_df['time_depart']) 
        out_df['time_depart'] = out_df['time_depart'].dt.time
        out_df.drop_duplicates(inplace=True)
        out_df.sort_values('time_depart', inplace=True)
        out_df.reset_index(drop=True, inplace=True)

        return(out_df)

    def list_unique_flights(self):
        a = self.list_flights()
        b = set(a.flight_no.to_list())
        return(b)
    

    def get_delay_stat(self):

        df_flight = self.list_flights()

        url = "https://flightera-flight-data.p.rapidapi.com/flight/statistics"

        headers = {
            "x-rapidapi-host": "flightera-flight-data.p.rapidapi.com",
            "x-rapidapi-key" : self.api_flightera
            }
        
        out_list=[]
        
        for x in df_flight.itertuples():

            params = {
                "aptTo": x.airport_arrival_icao,
                "aptFrom": x.airport_depart_icao,
                "flnr": x.flight_no
                }

            response = requests.get(url, headers=headers, params = params)
            out_call = response.json()

            out_dict = ({key:dictionary[key] for dictionary in out_call for key in ['flnr', 'count_30d', 'delay_30d', 'cancelled_30d', 'avg_delay'] if key in dictionary})
            out_list.append(out_dict)
        
        out = pd.DataFrame(out_list)
        return(out)

