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
    
    #sensorKeys=['G2qNwyjYGaCjRJzRQNOz','JxKlvngEL0HO75NldW2a','DJ6Ro7ala1hlV6jXq5bb']
    sensorKeys=['JxKlvngEL0HO75NldW2a','DJ6Ro7ala1hlV6jXq5bb']
    sensorLats=[4.621691, 4.601692]
    sensorLons=[-74.064962,-74.075963]
    
    # print sensorKeys
    
    points=[]
    
    
   # for key in sensorKeys:
    for i in range(0,len(sensorKeys)):
        key=sensorKeys[i]
        lat=sensorLats[i]
        lon=sensorLons[i]
        phantURL='https://data.sparkfun.com/output/'+key+'.json?page=1'
        #print phantURL
        response=urllib2.urlopen(phantURL)
        #print response
        data=json.load(response)
        last_reading=data[0]
        temp=float(last_reading['temp'])
        timeBits=last_reading['timestamp'].split('T')[1].split(':')
        hour=timeBits[0]+':'+timeBits[1]
         #print hour
        date=last_reading['timestamp'].split('T')[0]
    
        batt=float(last_reading['batt'])
        conduct=float(last_reading['conduct'])
        point=[key,lat,lon,temp,batt,conduct, date, hour]
        points.append(point)
        
    print points
    
    phantKey='QGXKjpvEpWH268W1NvWD'
    phantURL='https://data.sparkfun.com/output/'+phantKey+'.json?page=1'
    
    response=urllib2.urlopen(phantURL)
    data=json.load(response)
    last_reading=data[0]
    temp=float(last_reading['temp'])
    #print temp
    
    timeBits=last_reading['timestamp'].split('T')[1].split(':')
    hour=timeBits[0]+':'+timeBits[1]
    #print hour
    date=last_reading['timestamp'].split('T')[0]
    #print date
    
    myPoint=lat,lon,temp,date,hour
    mapCenter=mapLat,mapLon
    
    return render_template('leaf.html',point=myPoint,mapCenter=mapCenter,points=points)

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

@app.route("/ping/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""
 
    resp = twilio.twiml.Response()
    resp.message("Hello, Mobile Monkey")
    return str(resp)


app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT',8080)))
