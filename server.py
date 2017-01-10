import re
import os
import uuid
import json
import tornado.ioloop
import tornado.web
from tornado import websocket
from ViewData import ViewData
from MainHandler import MainHandler
from ChannelHandler import ChannelHandler
from ClientHandler import ClientWSConnection
from DataBaseConnections import MongoConnections
from AppsAuthentication import AppsAuthentication
# from EventController import EventController

channel = ChannelHandler()
collection = MongoConnections()

app = tornado.web.Application([
    (r"/", MainHandler, {'channel_handler': channel}),
    (r"/app", AppsAuthentication),
    # (r"/event", EventController),
    (r"/ws/(.*)", ClientWSConnection, {'channel_handler': channel}),
    (r'/show/(.*?)',ViewData,{'channel_handler':channel, 'collection': collection.Collection()}),
    ],
    static_path=os.path.join(os.path.dirname(__file__), "static")
)
app.listen(8888)
print 'SE Socket Started'
print 'listening on 8888 ...'
tornado.ioloop.IOLoop.instance().start()
