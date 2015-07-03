#!/usr/bin/env python2.7

#
import logging
import os
import redis

from flask import Flask, Response, json, render_template, url_for


keys = ["Door_garageentryclosed", "Door_frontclosed"]

app = Flask(__name__, static_url_path='')
app.redis = redis.StrictRedis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, db=0)


@app.route("/doors.json")
def doors():
    values = app.redis.mget(keys)
    data = dict(dict(zip(keys, values)))
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp

@app.route("/house.json")
def house():
    sensorTypes={ 'Door':{}, 'Motion':{}, 'Doorbell':{}}
    data = {}

    for sensortype in keys:
        newbucket = sensortype.split('_')[0]
        newkey = sensortype.split('_')[1]

        #grab the first part of the key

        value=app.redis.mget(sensortype)
        #if not sensorTypes[newbucket]:
        sensorTypes[newbucket].update( {  newkey: value[0]})

        logging.debug('redis has %s for %s' % (value[0], newkey))

        logging.debug('%s' % sensorTypes)


    #data = dict(dict(zip(keys, values)))
    resp = Response(json.dumps(sensorTypes), status=200, mimetype='application/json')
    return resp


#TODO: read a heartbeat key from redis and display under /montor/ping

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
