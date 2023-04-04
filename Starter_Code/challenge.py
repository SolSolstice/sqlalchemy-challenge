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


last12mo = dt.date(2017,8,23) - dt.timedelta(days = 365)

sel_list = [measurement.date,measurement.prcp] 
#main home-> query for precip,station,tobs, starting day for tobs, starting & ending dates for tobs 
# starting & ending dates -> form of sttring . mm - dd -yyyy
@app.route("/")   
def home():
    print ("server attempting to go to home page...")
                                     # prints in output console 
    return (f"Welcome to Matthew's Challenge-10 page. You are home!<br>"
            f"Current Routes:<br>"
            f"/<br>"
            f"/precipitation<br>"
            f"/stations<br>"
            f"/temperatures observed<br>"
            f"/start<br>"
            f"/start & end<br>"
            )

#results = session.query(measurement.date,measurement.prcp).filter(measurement.date >= last12mo).all()

#percep_12mo = session.query(measurement.date,measurement.prcp).filter(measurement.date >= last12mo)


          
# preciptation route -> route that calcs tobs from prev year 
    #                   -> jsonify results & display as return
@app.route("/precipitation")


def precip():


    # Query for the date and precipitation for the last year
 
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



# stations route -> query of all station in stations table 
    #               -> jsonify results & "unravel" using numpy 
@app.route("/stations")

def stations():
    session = Session(engine)
    station_results = session.query(station.station).all()
    session.close()
    all_stations = list(np.ravel(station_results))
    return jsonify(all_stations)



# tobs -> calc previous year w/ time delta
#           -> calc out your measurements for 1 station over previous year
@app.route("/tobs")
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

    
@app.route("/start")
def start():
    session = Session(engine)
    last12mo = dt.date(2017,8,23) - dt.timedelta(days = 365)
    sel_list = [
        measurement.date,
        session.query(func.min(measurement.tobs)),
        session.query(func.max(measurement.tobs)),
        session.query(func.avg(measurement.tobs))
    ]
    start_aggs = session.query(*sel_list).filter(measurement.station == 'USC00519281').filter(measurement.date >= last12mo).all()

    #start_min = session.query(func.min(measurement.tobs).filter(measurement.station == 'USC00519281').\
    #                          filter(measurement.date >= last12mo).all()
    #start_max = session.query(func.max(measurement.tobs).filter(measurement.station == 'USC00519281').\
    #                          filter(measurement.date >= last12mo).all().all()
    #start_avg = session.query(func.avg(measurement.tobs).filter(measurement.station == 'USC00519281').\
    #                          filter(measurement.date >= last12mo).all().all()                            
                            
    session.close()

    #for result in resultlist: 
        #aggsdict = {}
        #aggsdict= result['tobs']
        #resultlist.append(aggsdict)
    return jsonify(start_aggs)





# combine start date (first variable) & start&end date (also variables)
    #     -> have func called to aggs (min, max, avg) of tobs 
    #    -> run query taht gets results 
    #   -> jsonify and display as return 

# start&end query might be a little tough 

#reference app.py 

if __name__ == "__main__":
    app.run(debug=True) 
#################################################
# Flask Routes
#################################################


