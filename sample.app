#!/usr/bin/env python
"""
My attempt to create a securitypi app which would run on my RasberryPi and update a Redis instance.

Redis could be read by a simple flask api (included) or something else.

Include a callback ability to trigger external events, like IFTTT.

#TODO: allow for more than just doors.

Requires a running local redis and a working GPIO connection to at least one sensor.

"""

__author__ = 'Doug Chapman <prjctgeek@gmail.com'
__version__ = '0.2'

import logging
import time
import requests
from SecurityPi.Model import Model, House, Door


def door_callback(key=None, val=None):
    """
    Called by the House poller if the state changes.
    IFTTT Maker channel sample.
    """
    eventUrls = {}
    eventUrls['anyDoor'] = 'https://maker.ifttt.com/trigger/anyDoor/with/key/{{KEY}}

    #only Event on door closed False
    if val is False:
        requests.post(eventUrls['anyDoor'],data={'value1': key, 'value2':val})
        logging.info('***anydoor_callback fired: event to ifttt, key: %s val: %s' %(key,val))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    ourHouse = House()
    ourHouse.adddoor(Door('frontdoorclosed', pin=25, setevent=door_callback))
    ourHouse.adddoor(Door('garageentryclosed', pin=22, setevent=door_callback))
    
    while 1:
        ourHouse.poll()
        time.sleep(2)

