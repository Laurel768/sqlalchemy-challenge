import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

from flask import Flask, jsonify

#database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


# #create app
app = Flask(__name__)

@app.route("/")
def webpage():
    return (
        f"<p>Hawaii weather API</p>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )
# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
        # Convert the Query Results to a Dictionary Using `date` as the Key and `prcp` as the Value
        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
        last_twelve_months = '2016-08-24'
        prcp_data = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= last_twelve_months).\
                order_by(Measurement.date).all()
        # Convert List of Tuples Into a Dictionary
        prcp_data_list = dict(prcp_data)
        # Return JSON Representation of Dictionary
        return jsonify(prcp_data_list)
        session.close()

# Station Route
@app.route("/api/v1.0/stations")
def stations():
        session = Session(engine)
        # Return a JSON List of Stations From the Dataset
        stations_all = session.query(Station.station, Station.name).all()
        # Convert List of Tuples Into Normal List
        station_list = list(stations_all)
        # Return JSON List of Stations from the Dataset
        return jsonify(station_list)
        session.close()

# TOBs Route
@app.route("/api/v1.0/tobs")
def tobs():

        session = Session(engine)
        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
        last_twelve_months = '2016-08-24'
        tobs_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= last_twelve_months).\
                order_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        tobs_data_list = list(tobs_data)
        # Return JSON List of Temperature Observations (tobs) for the Previous Year
        return jsonify(tobs_data_list)
        session.close()

# # Start Day Route
# @app.route("/api/v1.0/<start>")
# def start_day(start):
#         session = Session(engine)
#         start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#                 filter(Measurement.date >= start).\
#                 group_by(Measurement.date).all()
#                 # Convert List of Tuples Into Normal List
#                 start_day_list = list(start_day)
#                 # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range
#                 return jsonify(start_day_list)
#                 session.close()

# Start-End Day Route
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_day(start=None, end=None):
        if not end:
                start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
                # Convert List of Tuples Into Normal List
                start_day_list = list(start_day)
                # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range
                return jsonify(start_day_list)
                # session.close()
        else:
                start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
                # Convert List of Tuples Into Normal List
                start_end_day_list = list(start_end_day)
                return jsonify(start_day_list)
                # session.close()

        # # Convert List of Tuples Into Normal List
        # start_day_list = list(start_day)
        # session = Session(engine)
        # start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        #         filter(Measurement.date >= start).\
        #         group_by(Measurement.date).all()
        # # Convert List of Tuples Into Normal List
        # start_day_list = list(start_day)
        # # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range
        # return jsonify(start_day_list)
        # session.close()

# def start_end_day(start, end):
#         session = Session(engine)
#         start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#                 filter(Measurement.date >= start).\
#                 filter(Measurement.date <= end).\
#                 group_by(Measurement.date).all()
#         # Convert List of Tuples Into Normal List
#         start_end_day_list = list(start_end_day)
#         # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range
#         return jsonify(start_end_day_list)
#         session.close()


if __name__ == '__main__':
    app.run(debug=True)
