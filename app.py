import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from sqlalchemy import create_engine

from flask import Response,json

from flask import Flask, jsonify

#from flask_cors import CORS, cross_origin

from flask import Flask, render_template



engine = create_engine("postgresql://adojvxmfrwsgyy:14c495164667d4c88d2054b812e118e446a166ec9760da7f98c8855ee0e789cc@ec2-23-23-128-222.compute-1.amazonaws.com:5432/dd6qmuecuuhqju")



# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table

results = engine.execute("select * from netflix").fetchall()


data_list = []

for i in results:
    a = {"Show_id":i[1],"Type":i[2],"Title":i[3],"Director":i[4],"Cast":i[5],"Country_name":i[6],"Date_added":i[7],"Release_year":i[8],"Rating":i[9],"Duration":i[10],"Listed_in":i[11],"Description":i[12],"Country":i[13],"Latitude":i[14],"Longitude":i[15]}
    
    data_list.append(a)

titles = engine.execute("select * from vw_country_title_cnt")

title_list = []

for i in titles:
    b = {"Country":i[0], "Titles":i[1]}

    title_list.append(b)

director = engine.execute("select * from vw_director_title_cnt limit 20")

director_list = []

for i in director:
    c = {"Director":i[0], "Titles":i[1]}

    director_list.append(c)

type = engine.execute("SELECT type,COUNT(*) AS Title FROM netflix GROUP BY type")

type_list = []

for i in type:
    d = {"Type":i[0], "Titles":i[1]}

    type_list.append(d)


release = engine.execute("SELECT release_year, COUNT(*) AS Title FROM netflix GROUP BY release_year Order by release_year ASC")

release_list = []

for i in release:
    e = {"release_year":i[0], "Titles":i[1]}

    release_list.append(e)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/releaseyear")
def releaseyer():
    return render_template("releaseyear.html")

@app.route("/map")
def map():
    return render_template("map.html")

@app.route("/country")
def country():
    return render_template("country.html")

@app.route("/directors")
def directors():
    return render_template("directors.html")

@app.route("/test", methods=["GET"])
def welcome():
    """List all available api routes."""
    
    return (jsonify(data_list))

@app.route("/titles", methods=["GET"])
def New_Route():
    
    return (jsonify(title_list))

@app.route("/director", methods=["GET"])
def Second_Route():
    
    return (jsonify(director_list))

@app.route("/type", methods=["GET"])
def third_Route():

    return (jsonify(type_list))

@app.route("/release", methods=["GET"])
def fourth_Route():

    return (jsonify(release_list))

if __name__ == '__main__':
    app.run(debug=True)
