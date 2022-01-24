import pygsheets
import pandas as pd
import os

dic = {
    'insights':0,
    'placement':1
}

directory = os.getcwd()
url = directory+ "/newapp/credentials_harshit.json"
gc = pygsheets.authorize(service_file= url )
sht = gc.open("spreadsheet")
def select_table(query):
    if 'placement' in query or 'platform' in query:
        sheet_name = 'placement'
        ws = sht[1]
        return pd.DataFrame(ws.get_all_records()), sheet_name
    else:
        sheet_name = 'insights'
        ws = sht[0]
        return pd.DataFrame(ws.get_all_records()), sheet_name