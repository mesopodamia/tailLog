# coding=utf8
__author__ = '19564770@qq.com'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import tornado.web
from tornado import gen
import tornado.websocket
from tornado.web import RequestHandler
import tornado.ioloop
import tornado.options
import tornado.process
import tornado.iostream
from tornado.options import parse_command_line
from local_settings import SSH_PORT,SSH_USER,CMD
from local_settings import LISTEN_HOST,LISTEN_PORT

class IndexHandler(RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('./static/index.html')

class MainHandler(tornado.websocket.WebSocketHandler):
    connects = set()

    def open(self):
        logging.info("A Client Connected. ")
        self.connects.add(self)

    def on_message(self, message):
        if message:
            if '#' in message:
                ip = message.split("#")[0]
                log_path = message.split("#")[1]

                cmd = "/usr/bin/ssh -p {port} {user}@{ipaddr} {command} {logpath}" \
                    .format(user=SSH_USER, ipaddr=ip, port=SSH_PORT, command=CMD, logpath=log_path)

                self.p = tornado.process.Subprocess(
                    cmd,
                    stdout=tornado.process.Subprocess.STREAM,
                    stderr=tornado.process.Subprocess.STREAM,
                    shell=True)

                tornado.ioloop.IOLoop.current().add_callback(
                    lambda: self.tail(self.p.stdout))

                tornado.ioloop.IOLoop.current().add_callback(
                    lambda: self.tail(self.p.stderr))

                self.p.set_exit_callback(self.close)
            else:
                self.write_message(message)

    @gen.coroutine
    def tail(self, stream):
        try:
            while True:
                line = yield stream.read_until(b'\n')
                if line:
                    self.write_message(line.decode('utf-8'))
                else:
                    break
        except tornado.iostream.StreamClosedError:
            # Subprocess killed.
            pass
        finally:
            self.close()

    def on_close(self):
        logging.info("A Client Disconnect. ")
        self.p.proc.kill()
        self.connects.remove(self)

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/taillog', MainHandler),
])

if __name__ == '__main__':
    parse_command_line()
    app.listen(LISTEN_PORT,LISTEN_HOST)
    tornado.ioloop.IOLoop.instance().start()
