# Import the dependencies.
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home_page():
    """List all available api routes."""
    return (
        f"Available Routes for Hawaii Weather Data:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Temperatures for the most active stations over the last year: /api/v1.0/tobs<br/>"
        f"Temperature statistics from start date to most recent date: /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature statistics from start date to end date: /api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
    )

#--------------------------------------------------
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Create a query to pull only data from last 12 months
    one_year_precip = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").\
        order_by(Measurement.date).all()
    
    # Close Session
    session.close()

    # Create a dictionary from the year results and append to a list
    precipitation = []
    for date, prcp in one_year_precip:
        precip_dict = {}
        precip_dict["Date"] = date
        precip_dict["Precipitation"] = prcp
        precipitation.append(precip_dict)
    
    return jsonify(precipitation)

#--------------------------------------------------
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Create a query to pull the stations
    weather_stations = session.query(Station.station).all()

    # Close Session
    session.close()

    # Convert to a normal list and return in json format
    station_names = list(np.ravel(weather_stations))
    return jsonify(station_names)

#--------------------------------------------------
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Create a query to pull the temperature data from 
    # the most active weather station
    active_temp = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= "2016-08-23").all()
    
    # Close Session
    session.close()

    # Create a list for the temperature observations from the most active station
    temperatures = []
    for date, tobs in active_temp:
        temp_dict ={}
        temp_dict["Date"] = date
        temp_dict["Temperature"] = tobs
        temperatures.append(temp_dict)
    
    return jsonify(temperatures)

#--------------------------------------------------
@app.route("/api/v1.0/<start>")
def temp_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Create a query to find the minimum, average, and maximum temperatures for the specified date range
    start_temp = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    # Create a list for the temperature statistics
    temp_stats = []
    for min, max, avg in start_temp:
        temp_stat_dict = {}
        temp_stat_dict["Minimum"] = min
        temp_stat_dict["Maximum"] = max
        temp_stat_dict["Average"] = avg
        temp_stats.append(temp_stat_dict)

    return jsonify(temp_stats)

    # Close session
    session.close()

#--------------------------------------------------
@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Create a query to find the minimum, maximum, and average temperatures from the specified start date to the end date
    start_end_temp = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    # Close the session
    session.close()

    # Create a list to hold the temperature statistics from the selected date range 
    start_end_stats =[]
    for min, max, avg in start_end_temp:
        start_end_dict = {}
        start_end_dict["Minimum"] = min
        start_end_dict["Maximum"] = max
        start_end_dict["Average"] = avg
        start_end_stats.append(start_end_dict)

    return jsonify(start_end_stats)

if __name__ == '__main__':
    app.run(debug=True)        