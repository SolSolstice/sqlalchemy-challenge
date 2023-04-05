# Import the dependencies.

from flask import Flask, jsonify
import numpy as np
from sqlalchemy import func, create_engine
import datetime as dt
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session




#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#set up automap base 
base = automap_base()
# reflect the tables

base.prepare(autoload_with=engine)

# reflect an existing database into a new model

measurement = base.classes.measurement
station = base.classes.station
# reflect the tables
session = Session(engine)

# Save references to each table

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



@app.route("/")  

def home():
    print ("server attempting to go to home page...")
                                     # prints in output console 
    return (f"Welcome to Matthew's Challenge-10 page. You are home!<br>"
            f"Current Routes:<br>"
            f"/<br>"
            f"/api/v1.0/precipitation<br>"
            f"/api/v1.0/stations<br>"
            f"/api/v1.0/temperatures observed<br>"
            f"/api/v1.0/start<br>"
            f"/api/v1.0/start/end<br>"
            )



@app.route("/api/v1.0/precipitation")

def precip():

# ====== precipitation info route ======

    last12mo = dt.date(2017,8,23) - dt.timedelta(days = 365)

    results = session.query(measurement.date,
                            measurement.prcp).\
                                filter(measurement.date >= last12mo).all()
    session.close()
    resultlist = []
    for result in results:
        precipdict = {}
        precipdict["date"] = result["date"]
        precipdict["prcp"] = result["prcp"]
        resultlist.append(precipdict)
    return jsonify(resultlist)

# ====== station info route ======

@app.route("/api/v1.0/stations")

def stations():
    session = Session(engine)
    station_results = session.query(station.station).all()
    session.close()
    all_stations = list(np.ravel(station_results))
    return jsonify(all_stations)


# ====== temperatures observed route =====
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    last12mo = dt.date(2017,8,23) - dt.timedelta(days = 365)
    temps_12mo = session.query(measurement.date,
                               measurement.tobs).filter(measurement.station == 'USC00519281').\
                                filter(measurement.date >= last12mo).all()
    session.close()

    resultlist = []
    for result in temps_12mo:
        tempsdict = {}
        tempsdict['date'] = result['date']
        tempsdict['tobs'] = result['tobs']
        resultlist.append(tempsdict)
    return jsonify(resultlist)


# ========= start date data only route =========

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)

    agg_list = [
        func.min(measurement.tobs),
        func.max(measurement.tobs),
        func.avg(measurement.tobs)
    ]

    startdate = dt.datetime.strptime(start,"%m%d%Y")

    agg_results = session.query(*agg_list).filter(measurement.date >= startdate).all()
    
    session.close()

    temps = list(np.ravel(agg_results))
    return jsonify(temps)

# ======== start & end date data route =======
@app.route("/api/v1.0/<start>/<end>")

def startend(start,end):
    session = Session(engine)
    se_aggs = [
        measurement.date,
        func.min(measurement.tobs),
        func.max(measurement.tobs),
        func.avg(measurement.tobs)
    ]
    startday = dt.datetime.strptime(start,"%m%d%Y")
    endday = dt.datetime.strptime(end,"%m%d%Y")

    se_results = session.query(*se_aggs).filter(measurement.date >= startday).\
                                                          filter(measurement.date <= endday).group_by(measurement.date)
  
    session.close()
  
    final_data = []

    for dates, mins, maxs, avgs in se_results:
        resultsdict = {}
        resultsdict["Date"] = dates
        resultsdict["Min"] = mins
        resultsdict["Max"] = maxs
        resultsdict["Avgs"] = avgs
        final_data.append(resultsdict)

    return jsonify(final_data)



if __name__ == "__main__":
    app.run(debug=True) 
#################################################
# Flask Routes
#################################################


