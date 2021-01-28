from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import psycopg2
from flask import Flask, render_template, jsonify
from flask_migrate import Migrate
from models import db, meetupCity, meetupEvents
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@127.0.0.1:5432/Meetup"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

engine=create_engine("postgresql://postgres:postgres@127.0.0.1:5432/Meetup") 

@app.route('/')
def home():

    return render_template('index.html')

@app.route('/heatMap')
def heatMap():
    session = Session(bind=engine)
    results=session.query(meetupEvents.event_lat, meetupEvents.event_lng).all()

    result_dict=[]
    for lat, lng in results:
        record={}
        record['lat']=lat
        record['lng']=lng
        result_dict.append(record)
    session.close()
    return jsonify(result_dict)

@app.route('/citydropDown')
@app.route('/citydropDown/<state>')
def citydropDown(state='All'):

    session = Session(bind=engine)
    if (state=='All'):
        results=session.query(meetupCity.city).\
            group_by(meetupCity.city).\
            order_by(meetupCity.city).all()
        result_dict=[]
        for city in results:
            record={}
            record['city']=city
            result_dict.append(record)
        session.close()
    else:
        results=session.query(meetupCity.city).\
            filter(meetupCity.state==state).\
            group_by(meetupCity.city).\
            order_by(meetupCity.city).all()

        result_dict=[]
        for city in results:
            record={}
            record['city']=city
            result_dict.append(record)
        session.close()        
    return jsonify(result_dict)    

@app.route('/categorydropDown')
def categorydropDown():

    session = Session(bind=engine)
    results=session.query(meetupEvents.category).\
        group_by(meetupEvents.category).\
        order_by(meetupEvents.category).all()
    result_dict=[]
    for category in results:
        record={}
        record['category']=category
        result_dict.append(record)
    session.close()
    return jsonify(result_dict)

@app.route('/eventInfo')
@app.route('/eventInfo/<state>/<city>/<category>')
def dataTable(state='All', city='All',category='All'):

    session = Session(bind=engine)

    if (state=='All' and city=='All' and category=='All'):
        results=session.query(meetupEvents.event_name, meetupEvents.group_name, meetupEvents.attendees,
             meetupEvents.category, meetupEvents.venue_event_link, meetupEvents.event_street, meetupEvents.google_map_link,
             meetupEvents.event_lat, meetupEvents.event_lng, meetupEvents.address).\
                join(meetupCity).\
                order_by(meetupCity.city).all()         

    elif (state!='All' and city=='All' and category=='All'):
        results=session.query(meetupEvents.event_name, meetupEvents.group_name, meetupEvents.attendees,
             meetupEvents.category, meetupEvents.venue_event_link, meetupEvents.event_street, meetupEvents.google_map_link,
             meetupEvents.event_lat, meetupEvents.event_lng, meetupEvents.address).\
                join(meetupCity).\
                filter(meetupCity.state==state).\
                order_by(meetupCity.city).all()

    elif (state!='All' and city!='All' and category=='All'):
        results=session.query(meetupEvents.event_name, meetupEvents.group_name, meetupEvents.attendees,
             meetupEvents.category, meetupEvents.venue_event_link, meetupEvents.event_street, meetupEvents.google_map_link,
             meetupEvents.event_lat, meetupEvents.event_lng, meetupEvents.address).\
                join(meetupCity).\
                filter(meetupCity.state==state and meetupCity.city==city).\
                order_by(meetupCity.city).all()

    elif (state!='All' and city!='All' and category!='All'):   
        results=session.query(meetupEvents.event_name, meetupEvents.group_name, meetupEvents.attendees,
             meetupEvents.category, meetupEvents.venue_event_link, meetupEvents.event_street, meetupEvents.google_map_link,
             meetupEvents.event_lat, meetupEvents.event_lng, meetupEvents.address).\
                join(meetupCity).\
                filter(meetupCity.state==state and meetupCity.city==city and meetupEvents.category==category).\
                order_by(meetupCity.city).all()

    elif (state=='All' and city!='All' and category=='All'):  
        results=session.query(meetupEvents.event_name, meetupEvents.group_name, meetupEvents.attendees,
             meetupEvents.category, meetupEvents.venue_event_link, meetupEvents.event_street, meetupEvents.google_map_link,
             meetupEvents.event_lat, meetupEvents.event_lng, meetupEvents.address).\
                join(meetupCity).\
                filter(meetupCity.city==city).\
                order_by(meetupCity.city).all() 

    elif (state=='All' and city!='All' and category!='All'):   
        results=session.query(meetupEvents.event_name, meetupEvents.group_name, meetupEvents.attendees,
             meetupEvents.category, meetupEvents.venue_event_link, meetupEvents.event_street, meetupEvents.google_map_link,
             meetupEvents.event_lat, meetupEvents.event_lng, meetupEvents.address).\
                join(meetupCity).\
                filter(meetupCity.city==city and meetupEvents.category==category).\
                order_by(meetupCity.city).all() 

    elif (state=='All' and city=='All' and category!='All'):   
        results=session.query(meetupEvents.event_name, meetupEvents.group_name, meetupEvents.attendees,
             meetupEvents.category, meetupEvents.venue_event_link, meetupEvents.event_street, meetupEvents.google_map_link,
             meetupEvents.event_lat, meetupEvents.event_lng, meetupEvents.address).\
                join(meetupCity).\
                filter(meetupEvents.category==category).\
                order_by(meetupCity.city).all()

    elif (state!='All' and city=='All' and category!='All'):   
        results=session.query(meetupEvents.event_name, meetupEvents.group_name, meetupEvents.attendees,
             meetupEvents.category, meetupEvents.venue_event_link, meetupEvents.event_street, meetupEvents.google_map_link,
             meetupEvents.event_lat, meetupEvents.event_lng, meetupEvents.address).\
                join(meetupCity).\
                filter(meetupCity==city and meetupEvents.category==category).\
                order_by(meetupCity.city).all()


    result_dict=[]
    for name, group, attendees, cat_gry, link, street, gmap, lat, lng, address in results:
        record={}
        record['name']=name
        record['group']=group
        record['attendees']=attendees
        record['city']=city
        record['state']=state
        record['category']=cat_gry
        record['link']=link
        record['street']=street
        record['gmap']=gmap
        record['lat']=lat
        record['lng']=lng
        record['address']=address
        result_dict.append(record)
    session.close()        
    return jsonify(result_dict)           

if __name__=="__main__":
    app.run(debug=True)