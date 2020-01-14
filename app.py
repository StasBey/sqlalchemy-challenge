from flask import Flask, json, jsonify
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

# List all routes that are available.
@app.route("/")
def home():
    print("Available Routes")
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-01-01/<br/>"???????????
        f"/api/v1.0/2016-01-01/2016-12-31/"???????????????
    )

# Return the JSON representation of your dictionary
@app.route('/api/v1.0/precipitation/')
def precipitation():
    print("Precipitation Section")
    
    max_date = session.query(func.max(Measurement.date)).all()
    twelve_months_back = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    sel = [Measurement.date, Measurement.prcp]
    daily_precipitation = session.query(*sel).filter(Measurement.date >= twelve_months_back).all() 

    precipitation_dict = dict(daily_precipitation)
    print(f"Daily Precipitation - {precipitation_dict}")
    print("Out of Precipitation section.")
    return jsonify(daily_precipitation) 

# Return a JSON-list of stations from the dataset.
@app.route('/api/v1.0/stations/')
def stations():
    print("Stations section.")
    
    stations = session.query(Measurement.station).group_by(Measurement.station).order_by(Measurement.station).all()
    print()
    print("Stations List:")   
    for row in stations:
        print (row[0])
    print("Out of Stations section.")
    return jsonify(stations)

# Return a JSON list of Temperature Observations (tobs) for the previous year
@app.route('/api/v1.0/tobs/')
def tobs():
    print("TOBS section.")

    max_date = session.query(func.max(Measurement.date)).all()
    twelve_months_back = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    sel = [Measurement.date, Measurement.tobs]
    t_obs = session.query(*sel).filter(Measurement.date >= twelve_months_back).order_by(Measurement.date).all() 
    
    print()
    print("Temperature Results by Station")
    print(t_obs)
    print("Out of TOBS section.")
    return jsonify(t_obs)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start.
@app.route('/api/v1.0/<start_date>/')
def calc_start_temps(start_date):
    print("Start date section.")
    print(start_date)
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    start_temp = session.query(*sel).filter(Measurement.date >= start_date).all()

    print()
    print(f"Start date temperature {start_date}")
    print(start_temp)
    print("Out of Start Date section.")
    return jsonify(start_temp)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.
@app.route('/api/v1.0/<start_date>/<end_date>/')
def calc_start_end_temps(start_date, end_date):
    print("Start and End Date section.")
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    start_end_temp = session.query(*sel).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    print()
    print(f"Start date {start_date} and end date {end_date}" temperatures)
    print(start_end_temp)
    print("Out of Start and End Date section.")
    return jsonify(start_end_temp)

if __name__ == "__main__":
    app.run(debug=True)