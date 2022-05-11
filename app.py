#Import necessary libraries

from flask import Flask, jsonify, render_template
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import sqlite3
import json
from collections import defaultdict


engine = create_engine("sqlite:///tailings/peizodata.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table named "node" and "sample" which both have Node_id
Node = Base.classes.node
Sample = Base.classes.sample

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#From the sample table
@app.route("/api/v1.0/sample/<Node_id>")
def samplelist(Node_id):
   # Create our session (link) from Python to the DB
   session = Session(engine)
   results= session.query(Sample.Node_id, Sample.sample_date,Sample.sample_values).filter(Sample.Node_id == Node_id).all()
   session.close()
  
   all_samples = []
   for Node_id, sample_date, sample_values in results:
      samples_dict = {}
      samples_dict["Node_id"] = Node_id
      samples_dict["Sample_date"] = sample_date
      samples_dict["sample_values"] = sample_values
      all_samples.append(samples_dict)

   dd = defaultdict(list)

   for d in (all_samples): # you can list as many input dicts as you want here
      for key, value in d.items():
        dd[key].append(value)
   
   #return jsonify(all_data)
   return jsonify(dd)


@app.route("/api/v1.0/nodes")
def nodelist():
   # Create our session (link) from Python to the DB
   session = Session(engine)
   results= session.query(Node.Node_id).all()
   
   session.close()

   all_names = list(np.ravel(results))

   return jsonify(all_names)

#From the node table
@app.route("/api/v1.0/Node_id/<Node_id>")
def nodes_by_Nodeid(Node_id):

   session = Session(engine)
   results= session.query(Node.Node_id, Node.Gateway_ID, Node.Model, Node.Piezometer_Channel, 
                          Node.Piezometer_ID, Node.Maxpressure,Node.Minimumpressure, Node.Latest_pressure, Node.Tip_Elevation, Node.Date_last_reading
                          	).filter(Node.Node_id == Node_id).all()
   
   session.close()

   samples_dict = {}
   for Node_id, Gateway_ID, Model, Piezometer_Channel,Piezometer_ID,Maxpressure,Minimumpressure,Latest_pressure,Tip_Elevation,Date_last_reading in results:
      samples_dict["Node_id"] = Node_id
      samples_dict["Gateway_ID"] = Gateway_ID
      samples_dict["Model"] = Model
      samples_dict["Piezometer_Channel"] = Piezometer_Channel
      samples_dict["Piezometer_ID"] = Piezometer_ID
      samples_dict["Maxpressure"] = Maxpressure
      samples_dict["Minimumpressure"] = Minimumpressure
      samples_dict["Latest_pressure"] = Latest_pressure
      samples_dict["Tip_Elevation"] = Tip_Elevation
      samples_dict["Date_last_reading"] = Date_last_reading
      
       
   return jsonify(samples_dict)

#Create route that renders three different html pages
@app.route("/Home")
def home():
   
   return render_template("homepage.html")

@app.route("/Findings")
def finding():
   
   return render_template("findings.html")

@app.route("/Map")
def map():
   
   return render_template("map.html")

#Create route that takes to the main page
@app.route("/")
def welcome():
    return (
        f"Welcome to the Monitoring of Tailings API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/sample/<Node_id><br/>"
        f"/api/v1.0/nodes<br/>"
        f"/api/v1.0/Node_id/<Node_id><br/>"
        f"/Home"
    )


if __name__ == "__main__":
    app.run(debug=True)