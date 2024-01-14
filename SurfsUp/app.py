# Import the dependencies.

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from datetime import datetime, timedelta

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables

Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)




#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation:<br/>"
        f"/api/v1.0/stations:<br/>"
        f"/api/v1.0/tobs:<br/>"
        f"/api/v1.0/<start>:<br/>"
        f"/api/v1.0/<start>/<end>:<br/>"
        )
    )
    @app.route("/api/v1.0/stations")
def stations():
    """ Return a JSON list of stations from the dataset."""
    
    results = session.query(Station.station).all()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    """query for the dates and temperature observations from a year from the last data point."""
 
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    """* Return a JSON list of Temperature Observations (tobs) for the previous year."""
    tobs_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=last_year).order_by(Measurement.date).all()
    

    return jsonify(tobs_data)
    
    @app.route("/api/v1.0/<start>")
def calc_temps(start):
    """When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date."""
    
    start_date = dt.datetime.strptime(start,"%Y-%m-%d")

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature"""
    
    query_data = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
    filter(Measurement.date >= start_date).all()

    result = list(np.ravel(query_data))

    return jsonify(result)
    
@app.route("/api/v1.0/<start>/<end>")
def calc_temps2(start,end):
    """When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive."""
    
    start_date = dt.datetime.strptime(start,"%Y-%m-%d")
    end_date = dt.datetime.strptime(end,"%Y-%m-%d")

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature"""
    
    query_data = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
    filter(Measurement.date.between(start_date,end_date)).all()
    
    result = list(np.ravel(query_data))

    
    return jsonify(result)
    
    if __name__ == "__main__":
    app.run(debug=False)