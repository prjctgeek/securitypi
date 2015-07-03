
# SecurityPi

Prototype of event generation code for rasberry pi attached to my home security system wiring.  I used a prototype board to hook up some normally closed magnet switches to +5v and the GPIO pins of the 'Pi.

My goal was to start with events on the IFTTT App, then work towards more event based actions next, with either a local redis or a cloud based IoT service.


### Installation

On your raspberry pi running a Debian based distro:

    sudo apt-get install redis-server python-redis
    pip install -r requirements.txt
    cp sample.app app
    vim app

    

At a minimum you need to assign the GPIO pins to useful names:

    ourHouse.adddoor(Door('frontdoorclosed', pin=25, setevent=door_callback))

#### Running

        sudo ./app 

Root/fixing the permissions on /proc/mem is required for GPIO access.     
        

## Flask api

#### To start:

    ./SecurityPi/api.py &


####Sample access:

    curl -s  http://localhost:5000/house.json|python -mjson.tool
    {
        "Door": {
            "frontclosed": "True",
            "garageentryclosed": "True",
        },
        "Doorbell": {},
        "Motion": {}
    }

Sample door specific endpoint:


    curl -s  http://localhost:5000/doors.json|python -mjson.tool
    {
        "Door_frontclosed": "True",
        "Door_garageentryclosed": "True",
    }


---


### IFTTT

I started out thinking my local redis instance with pubsub events was the way to go,
but after playing with [IFTTT](http://www.ifttt.com) I'm not so sure.

#### Setup

On IFTTT, enable the Maker channel and setup an event, e.g.: `Doors`.

In the app file, update the eventUrls with the URL provided by _How to Trigger_ on the [setup page](https://ifttt.com/maker), something like:


    https://maker.ifttt.com/trigger/{eventName}/with/key/{YOUR KEY}


Of course you can re-write the callback function in the app file todo anything.

