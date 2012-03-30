#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import time
import optparse
import json

__author__ = "f47h3r - Chase Schultz"

listeners = {}
names = {}


class adminObject():
    def __init__(self, boxUUID, websocketInstance):
        self.uuid = boxUUID
        self.webSocket = websocketInstance

    def webSocket(self):
        return self.webSocket

    def uuid(self):
        return self.uuid


class commandStructureObject():
    def __init__(self, boxUUID, userName, websocketInstance):
        self.uuid = boxUUID
        self.webSocket = websocketInstance
        self.username = userName

    def webSocket(self):
        return self.webSocket

    def uuid(self):
        return self.uuid

    def username(self):
        return self.username


class PostHandler(tornado.web.RequestHandler):
    """
    Handles Posted Commands and Sends to Clients
    """
    def post(self):
        if 'message' in self.request.arguments:
            message = self.request.arguments['message'][0]
            group = self.request.arguments.get('group', ['default'])[0]
            print '%s:MESSAGE to %s:%s' % (time.time(), group, message)

            #For every Client Listener in the group specified in post data
            for client in listeners.get(group, []):
                client.write_message(message)

            websocket = listeners.get('admin', ['default'])[0].webSocket

            print 'THE WEBSOCKET = \n\n'
            print websocket
            websocket.write_message(message)
            return 'true'
        return 'false'


class SpawnClientSocket(tornado.web.RequestHandler):
    """
    Handles Spawn of Shells
    """
    def post(self):
        user = self.request.arguments['user'][0]

        #construct JSON Object
        data = [{'command':'spawnwebsocket', 'user':user}]
        jsonObject = json.dumps(data)

        for client in listeners.get('admin', ['default']):
            websocket = client.webSocket
            websocket.write_message(jsonObject)
        #websocket = listeners.get('admin',['default'])[0].webSocket

        #print 'THE WEBSOCKET = \n\n'
        #print websocket

        return 'true'


class DistributeHandler(tornado.websocket.WebSocketHandler):
    ''' Registers boxes to groups and manages websockets '''
    def open(self, params):
        print 'Parameters: %s' % str(params)
        group, uuid, name = params.split('/')
        self.group = group or 'default'
        self.uuid = uuid or 'fuck...no UUUID'
        self.name = name or 'anonymous'

        #If group isn't already in the list add it.
        if not self.group in listeners:
            listeners[self.group] = []

        if group == 'admin':
            listeners[group].append(adminObject(self.uuid, self))
            pass
        elif group == 'Windows' or group == 'Linux' or group == 'Darwin':
            listeners[group].append(commandStructureObject(self.uuid, self.name, self))
            pass
        else:
            # notify clients that a member has joined the groups
            for client in listeners.get(self.group, []):
                client.write_message('+' + self.name)

            #Append Websocket instance to group
            listeners[self.group].append(self)
        names[self] = self.name
        print '%s:CONNECT to %s from %s' % (time.time(), self.group, self.name)

    def on_message(self, message):
        ''' Sends Messages back to the shell interface '''
        print message
        for client in listeners.get("shell", []):
            client.write_message(message)
        pass

    def on_close(self):
        if self.group in listeners:
            listeners[self.group].remove(self)
        del names[self]
        # notify clients that a member has left the groups
        for client in listeners.get(self.group, []):
            client.write_message('-' + self.name)
        print '%s:DISCONNECT from %s' % (time.time(), self.group)
'''

#Example Websocket Code

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        self.write_message("Hello Client!")

    def on_message(self, message):
        print 'message received %s' % message
        response = raw_input('Type a response:')
        self.write_message(response)

    def on_close(self):
        print 'connection closed'

'''

if __name__ == "__main__":
    usage = __doc__
    version = "0.01"
    parser = optparse.OptionParser(usage, None, optparse.Option, version)
    parser.add_option('-p',
                      '--port',
                      default='9002',
                      dest='port',
                      help='Listener Port')
    parser.add_option('-l',
                      '--listen',
                      default='127.0.0.1',
                      dest='ip',
                      help='Listener IP address')
    (options, args) = parser.parse_args()
    application = tornado.web.Application([
#For Example
#    (r'/ws', WSHandler),
    (r'/', PostHandler),
    (r'/endpoint/(.*)', DistributeHandler),
    (r'/spawnshells', SpawnClientSocket)
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(int(options.port), address=options.ip)
    tornado.ioloop.IOLoop.instance().start()
