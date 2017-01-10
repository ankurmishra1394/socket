import os
import uuid
import json
import tornado.ioloop
import tornado.web
from tornado import websocket
from ChannelHandler import ChannelHandler
import pymongo
import re


class ViewData(tornado.web.RequestHandler):
	def initialize(self,channel_handler,collection):
		self.__channel_handler=channel_handler		
		self.collection = collection

	def get(self, channelname):

		try:
			# print channelname
			if channelname:				
				lists = list(self.collection.find({'channel_name':channelname}))
			else: 
				lists = list(self.collection.find())
			self.render("templates/chatShow.html",list = lists)
		except Exception, e:
			print "Show error :" +str(e)
		

