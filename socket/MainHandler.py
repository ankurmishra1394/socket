import sys, traceback
import json
import tornado.web
from tornado import websocket
from ClientHandler import ClientWSConnection

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, channel_handler):
        self.__channel_handler = channel_handler

    def get(self):
        try:
            client = self.get_argument("client")
            channel = self.get_argument("channel")
            client_id = self.__channel_handler.generate_channel(channel, client)
            self.render("templates/chat.html", clientid=client_id)
        except Exception, e:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
            self.render("templates/main.html")