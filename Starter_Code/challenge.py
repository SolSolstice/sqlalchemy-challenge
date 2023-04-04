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
            f"/start & end<br>"
            )

#results = session.query(measurement.date,measurement.prcp).filter(measurement.date >= last12mo).all()

#percep_12mo = session.query(measurement.date,measurement.prcp).filter(measurement.date >= last12mo)


          
# preciptation route -> route that calcs tobs from prev year 
    #                   -> jsonify results & display as return
@app.route("/precipitation")


def precip():
    return sel_list
   # session = Session(engine)
   # last12mo = dt.date(2017,8,23) - dt.timedelta(days = 365)

   # results = session.query(measurement.date,measurement.prcp).filter(measurement.date >= last12mo).all()
   # resultlist = []
   # for result in results:
   #     precipdict = {}
   #     precipdict["date"] = result["date"]
   #     precipdict["prcp"] = result["prcp"]
   #     resultlist.append(precipdict)
   #     return jsonify(precipdict)

 




# stations route -> query of all station in stations table 
    #               -> jsonify results & "unravel" using numpy 
# tobs -> calc previous year w/ time delta
#           -> calc out your measurements for 1 station over previous year

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


