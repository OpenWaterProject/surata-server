import os
from flask import Flask, request, redirect, render_template
import twilio.twiml
import urllib2
import json
 
app = Flask(__name__)

    
@app.route('/')
def monkey():
    return render_template('index.html')
    
@app.route("/phant", methods=['GET', 'POST'])
def phant():
    """Respond to incoming calls with a simple text message."""


    body=request.values.get('Body')
    elements=body.split(",")
    temp=int(elements[2])/100.
    print temp 

    publicKey="QGXKjpvEpWH268W1NvWD"
    privateKey="JqAe046P4mhqgGbBZ8bE"
  
    sentence = 'https://data.sparkfun.com/input/'+str(publicKey)+'?private_key='+str(privateKey)+'&temp='+str(temp)
    print sentence

    url_response = urllib2.urlopen(sentence)
    print url_response
 
    #return 'hello' #not sure whether this is sending a text message back to user? 
 
@app.route('/map')
def mymap():
    
    #example for juan camilo's office
    
    mapLat=4.601693
    mapLon=-74.065961
    
    lat=4.601693
    lon=-74.065961
    
    phantKey='QGXKjpvEpWH268W1NvWD'
    phantURL='https://data.sparkfun.com/output/'+phantKey+'.json?page=1'
    
    response=urllib2.urlopen(phantURL)
    data=json.load(response)
    last_reading=data[0]
    temp=float(last_reading['temp'])
    print temp
    
    timeBits=last_reading['timestamp'].split('T')[1].split(':')
    hour=timeBits[0]+':'+timeBits[1]
    #print hour
    date=last_reading['timestamp'].split('T')[0]
    #print date
    
    point=lat,lon,temp,date,hour
    mapCenter=mapLat,mapLon
    
    return render_template('leaf.html',point=point,mapCenter=mapCenter)

@app.route("/crowd", methods=['GET', 'POST'])
def crowd():
    """Respond to incoming calls with a simple text message."""


    body=request.values.get('Body')
    elements=body.split(",")
    temp=int(elements[2])/100.
    print temp 
    
    sentence="https://stv1.crowdmap.com/api?task=report&incident_title='cats crossing the road'&incident_description='big cats'&incident_date='01/01/2010'&incident_hour='8'&incident_minute='3'&incident_am='am'&incident_category=1&latitude='7.19'&longitude='-72.95'&location_name='meow island'"
  
    url_response = urllib2.urlopen(sentence)
    print url_response
    
    return 'hello' 
    
    
#if __name__ == "__main__":
#    app.run(debug=True)

@app.route('/hello')
def hello():
    return 'Hello World'
    
@app.route('/crowdmap')
def crowdmap():
    return 'Hello map'
#app.run(host=os.environ['IP'],port=int(os.environ['PORT']))


app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT',8080)))
