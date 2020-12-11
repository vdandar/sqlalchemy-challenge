
#%%
import pandas as pd
import numpy as np
import sqlalchemy
import json
from sqlalchemy import create_engine
from flask import Flask, jsonify
#%%
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
conn = engine.connect()
#%%
app = Flask(__name__)
#%%

@app.route('/api/v1.0/')
def welcome():
    return(
     f"Available Routes:<br/>"
     f"/api/v1.0/precipitation<br/>"
     f"/api/v1.0/stations<br/>"
     f"/api/v1.0/tobs<br/>"
     f"/api/v1.0/<start><br/>"
     f"/api/v1.0/<start>/<end><br/>"
    )

#%%
@app.route('/api/v1.0/precipitation')
def prcp():
    conn = engine.connect()
    query = f'''
        SELECT 
            date,
            prcp
        FROM
            measurement
        WHERE
            date >= (SELECT DATE(MAX(date),'-1 year') FROM measurement)
        GROUP BY
            date
        ORDER BY 
            date
    '''
    # Save the query results as a Pandas DataFrame and set the index to the date column
    prcp_df = pd.read_sql(query, conn)
    # Convert the date column to date
    prcp_df['date'] = pd.to_datetime(prcp_df['date'])
    # Sort the dataframe by date
    prcp_df.sort_values('date')
    prcp_json = prcp_df.to_json(orient='records', date_format = 'iso')
    conn.close()
    return prcp_json

#%%
@app.route('/api/v1.0/stations')
def station():
    conn = engine.connect()
    query = f'''
        select
          s.station as station_code, 
          s.name as station_name
        From 
            measurement m
        inner join station s
            on m.station=s.station
        Group BY
            s.station,
            s.name
    '''
    active_stations_df = pd.read_sql(query,conn)
    station_json = active_stations_df.to_json(orient='records')
    conn.close()
    return station_json
#%%
@app.route('/api/v1.0/tobs')
def tobs():
    conn = engine.connect()
    query=f'''
        SELECT
        date, tobs
        FROM
        measurement
        WHERE
        date >= (SELECT DATE(MAX(date),'-1 year') FROM measurement)
        and station = 'USC00519281'
    '''

    temps_obs_df=pd.read_sql(query,conn)  
    temps_obs_json = temps_obs_df.to_json(orient='records')
    conn.close()
    return temps_obs_json

#%%
@app.route('/api/v1.0/<start>')
def start(start):
    conn = engine.connect()
    query=f'''
        SELECT 
        min(tobs), 
        max(tobs), 
        avg(tobs) 
        from 
        measurement 
        where date = '{start}'
    '''
    start_df=pd.read_sql(query, conn) 
    start_json = start_df.to_json(orient='records')
    conn.close()
    return start_json
#%%
# http://localhost:5000//api/v1.0/2012-02-21/2012-02-28
@app.route('/api/v1.0/<start>/<end>')
def end(start, end):
    conn = engine.connect()
    query=f'''
        SELECT 
        min(tobs), 
        max(tobs), 
        avg(tobs) 
        from 
        measurement 
        where date between '{start}' and  '{end}'
    '''
    end_df=pd.read_sql(query, conn) 
    end_json = end_df.to_json(orient='records')
    conn.close()
    return end_json
#%%
if __name__ == '__main__':
    app.run(debug=True)    
#%%
'''
/api/v1.0/precipitation
Convert the query results to a dictionary using date as the key and prcp as the value.
Return the JSON representation of your dictionary.
/api/v1.0/stations
Return a JSON list of stations from the dataset.
## openb anacondo prompt
type python app.py
try it with local host
'''
