from flask import Flask, jsonify
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = 20, 10
import numpy as np
import pandas as pd
import datetime as dt


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
inspector = inspect(engine)
inspector.get_table_names()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

query1 = engine.execute('SELECT date , prcp FROM measurement').fetchall()

m_query1 = pd.DataFrame(query1)
m_query1 = m_query1.rename(columns={0: 'date', 1: 'prcp'})



app = Flask(__name__)

@app.route("/")
def homepage():
    return (
        f'/api/v1.0/precipitation<br>'
    f'/api/v1.0/stations<br>'
    f'/api/v1.0/tobs<br>'
    f'/api/v1.0/<start><br/>'
    f'/api/v1.0/<start>/<end><br/>')

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(Measurement.date,Measurement.prcp).order_by(Measurement.date.desc()).first()[0]
    last_year = str(dt.datetime.strptime(last_date,"%Y-%m-%d") - dt.timedelta(days=365))

    
    precipitation = session.query(Measurement.date, Measurement.prcp).\
		filter(Measurement.date >=last_year, Measurement.date <=last_date).\
		order_by(Measurement.date).all()
	
    precip_dict = {date: prcp for date, prcp in precipitation}
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Measurement.station).\
    	group_by(Measurement.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def temp_monthly():
    last_date = session.query(Measurement.date,Measurement.prcp).order_by(Measurement.date.desc()).first()[0]
    last_year = str(dt.datetime.strptime(last_date,"%Y-%m-%d") - dt.timedelta(days=365))

    last_year_tobs = session.query(Measurement.date, Measurement.station,Measurement.tobs).\
		filter(Measurement.date >=last_year, Measurement.date <=last_date).\
		order_by(Measurement.date,Measurement.station).all()

    temps = list(np.ravel(last_year_tobs))
    return jsonify(temps)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    select_stat = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*select_stat).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*select_stat).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)


if __name__ == "__main__":
    app.run(debug=True)