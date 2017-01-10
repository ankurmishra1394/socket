import os
import uuid
import json
import tornado.ioloop
import tornado.web
from tornado import websocket
import pymongo
import datetime

class ClientWSConnection(websocket.WebSocketHandler):
    def initialize(self, channel_handler):
        self.__channel_handler = channel_handler
        mongo = pymongo.MongoClient("localhost", 27017)
        self.db = mongo['server']
        self.collection = self.db['ClientMsg']     

    def open(self, client_id):
        self.__clientID = client_id
        self.__channel_handler.generate_connection(client_id, self)
        print "WebSocket opened. ClientID = %s" % self.__clientID

    def on_message(self, message):
        msg = json.loads(message)
        msg['username'] = self.__channel_handler.client_info[self.__clientID]['client']
        pmessage = json.dumps(msg)
        jsonload= json.loads(pmessage) 
        remote_connected = self.__channel_handler.channel_connection(self.__clientID)
        for conn in remote_connected:            
            conn.write_message(pmessage)
        self.DataBaseInsertion(pmessage)

    def on_close(self):
        print "WebSocket closed"
        self.__channel_handler.remove_client(self.__clientID)

    def DataBaseInsertion(self,pmessage):
        time = datetime.datetime.now()
        msg = json.loads(pmessage)
        # msg['created_at'] =  time

        msg['channel_name'] = self.__channel_handler.client_info[self.__clientID]['channel'] 
        pmessage = json.dumps(msg)
        jsonload= json.loads(pmessage) 
        try:
            self.collection.insert_one(jsonload)
        except Exception, e:
            print "Insertion error :" +str(e)
