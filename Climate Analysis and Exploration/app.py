import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Database setup
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

#Save references to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#Session Link from Python to the DB
session = Session(engine)

#Flask Setup
app = Flask(__name__)

#Year ago definition
one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

#Flask Routes
@app.route("/")
def home():
    """List all avalible api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"api/v1.0/<start>/<end>"
    )

    @app.route("/api/v1.0/precipitation")
    def precipitation():
        prcp_recent_year = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > one_year_ago).all()

    session.close()

    #Create a dictionary for precipitation data
    precipitation_data = []
    for rain_data in prcp_recent_year:
        rain_data_dict = {}
        rain_data_dict["Date"] = rain_data.date
        rain_data_dict["Precipitation"] = rain_data.prcp
        precipitation_data.append(rain_data_dict)

        return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    list_all_stations = session.query(Station.id).count()

    return jsonify(list_all_stations)

session.close()

@app.route("/api/v1.0/tobs")
def temperature():
    temp_recent_year = session.query(Measurement.station, Measurement.tobs).\
    filter(Measurement.date > one_year_ago).all()

    return jsonify(temp_recent_year)

session.close()

@app.route("/api/v1.0/<start>")
def start_date(start):
    temperatures = session.query(func.min(Measurement.tobs),\
         session.query(func.max(Measurement.tobs), session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()

    return jsonify(temperatures)

session.close()

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    start_end = session.query(func.min(Measurement.tobs),\
         session.query(func.max(Measurement.tobs), session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end)\
        group_by(Measurement.date).all()

    return jsonify(start_end_date)

session.close()

if __name__ == "__main__":
    app.run(debug=True)



