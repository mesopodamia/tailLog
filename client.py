#!/usr/bin/python
# encoding=utf-8

from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect

class Client(object):

    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.connect()
        PeriodicCallback(self.keep_alive, 5000, io_loop=self.ioloop).start()
        self.ioloop.start()


    @gen.coroutine
    def connect(self):
        print("trying to connect")
        try:
            self.ws = yield websocket_connect(self.url)
        except:
            print("connection error")
        else:
            print("=connected=")
            self.run()

    @gen.coroutine
    def run(self):
        print "5"
        while True:
            msg = yield self.ws.read_message()
            # print "4"
            # print "- %s -" % msg
            if msg is None:
                print("connection closed")
                self.ws = None
                break


    def keep_alive(self):
        if self.ws is None:
            print "2"
            self.connect()
        else:
            print "3"
            self.ws.write_message("happy new year")


if __name__ == "__main__":
    client = Client("ws://192.168.104.35:3000/taillog", 5)