import os
import uuid
import json
import tornado.ioloop
import tornado.web
from tornado import websocket
from MainHandler import MainHandler
from ClientHandler import ClientWSConnection
from ChannelHandler import ChannelHandler

if __name__ == "__main__":
    channel = ChannelHandler()
    app = tornado.web.Application([
        (r"/", MainHandler, {'channel_handler': channel}),
        (r"/ws/(.*)", ClientWSConnection, {'channel_handler': channel})],
        static_path=os.path.join(os.path.dirname(__file__), "static")
    )
    app.listen(1234)
    print 'SE Socket Started'
    print 'listening on 1234 ...'
    tornado.ioloop.IOLoop.instance().start()