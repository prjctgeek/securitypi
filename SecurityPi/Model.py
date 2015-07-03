#!/usr/bin/env python2.7

import logging
import RPi.GPIO as GPIO
import redis
import sys



"""
Sample using redis to store state of door objects.

read: https://synack.me/blog/hack-1-a-simple-orm-for-python-and-redis

"""

log = logging.getLogger(__name__)


class Model(object):
    """
    Tie redis and gpio into a class model we can reuse.

    Takes an optional call back event that will be run on set, with the key and value
     as arguments.
    """
    db = redis.StrictRedis(host='localhost', port=6379, db=0)

    def __init__(self, name, pin=None, setevent=None):
        self.name = name
        self.key = '%s_%s' % (self.__class__.__name__, name)
        self.eventcallback = setevent
        self.last = None
        if pin:
            self.assignpin(pin=pin)
        return

    def assignpin(self, pin=None):
        #Unclear if this is generic enough for most uses.
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        return

    def delete(self):
        self.db.delete(self.key)

    def __str__(self):
        return self.key

    def __repr__(self):
        return '%s(\'%s\')' % (self.__class__.__name__, self.name)

    def __setstate(self, val=False):
        #State in this model is true/false
        if self.last is not bool(val):
            log.info('Updating redis key %s to %s with last value %s' % (self.key,bool(val),self.last))
            self.db.set(self.key, val)
            self.last = val
            self.db.expire(self.key, 60)
            if self.eventcallback:
                self.eventcallback(key=self.key, val=val)
        return

    def __readpin(self):
        tmp = bool(GPIO.input(self.pin))
        log.debug('Read pin %s with value %s' % (self.pin,tmp))
        return bool(tmp)

    def poll(self):
        self.__setstate(val=self.__readpin())
        return


class Door(Model):
    def is_closed(self):
        return self.db.get(self.key)


class PassiveIR(Model):
    def is_motion(self):
        return self.db.get(self.key)


class House(object):
    """
    Enclose our Door, etc... objects.
    TODO: Iterable?
    """
    def __init__(self):
        self.doors = {}
        self.pir = {}
        self.lights = {}
        return

    def adddoor(self, doorObj):
        self.doors[doorObj.key] = doorObj

    def addpir(self, pirObj):
        self.pir[pirObj.key] = pirObj

    def addlights(self, lightsObj):
        self.lights[lightsObj.key] = lightsObj

    def poll(self):
        for pirname in self.pir.keys():
            self.pir[pirname].poll()
        for doorname in self.doors.keys():
            self.doors[doorname].poll()

if __name__ == "__main__":
    sys.exit(-1)
