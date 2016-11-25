import os
import uuid
import json
import tornado.ioloop
import tornado.web
from tornado import websocket
from MainHandler import MainHandler
from ClientHandler import ClientWSConnection
from ChannelHandler import ChannelHandler
import tornado.options
import sys

if __name__ == "__main__":
    #tornado.options.options['log_file_prefix'].set('/var/log/socket.log')
    args = sys.argv
    args.append("--log_file_prefix=/var/log/socket.log")
    tornado.options.parse_command_line(args)
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
