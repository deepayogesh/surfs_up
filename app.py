# Import our code dependacies 
import datetime as dt
import pandas as pd
import numpy as np 
##  SQL Alchemy dependacies 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# # Import Flask Dependacies 
from flask import Flask, jsonify

# Set up Database   engin will allow you to access sQL Lite database 
engine = create_engine("sqlite:///hawaii.sqlite")   #  create_engine() function allows to access and query SQL Lite database file.

Base = automap_base()
#  now this Python Base.prepare Flask function allow to reflect on tables 
Base.prepare(engine, reflect = True)
Measurement = Base.classes.measurement     # variable for each class 
Station = Base.classes.station
session = Session(engine)            # create session link 

import app
print("example __name__ = %s", __name__)
if __name__ =="__main__":
    print("example is being run directly ")
else:
    print("example is being imported ")

#  __name__  variable set to __main__ we can run this
# Lets biuld Routes
#  routes should always go after app = Flask(__name__)    we have already done this step*************

#   starting point t tis root of routs 
app = Flask(__name__)
@app.route('/')
#   for Creating Routes /api/v1.0/   naming convetnion need to follow 
def welcome():
    return (
        '''
        Welcome to the Climet Analysis API!
        Available Routes:
        /api/v1.0/precipitation
        /api/v1.0/stations
        /api/v1.0/tobs
        /api/v1.0/temp/start/end
        ''')
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017,8,23)- dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip ={date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    results  = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations =stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year= dt.date(2017,8,23)- dt.timedelta(days=365)
    results =session.query(Measurement.tobs).\
        filter(Measurement.station =='USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps= list(np.ravel(results))
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start =None, end=None):
    sel =[func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    results =session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps= list(np.ravel(results))
    return jsonify(temps)    
 