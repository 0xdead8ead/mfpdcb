import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import subprocess
import time
import urllib


listeners = {}
names = {}

class PostHandler(tornado.web.RequestHandler):
    """
    Handles Posted Commands and Sends to Clients
    """
    def post(self):
        if 'message' in self.request.arguments:
            message = self.request.arguments['message'][0]
            group = self.request.arguments.get('group',['default'])[0]
            print '%s:MESSAGE to %s:%s' % (time.time(), group, message)
            for client in listeners.get(group,[]): client.write_message(message)
            return 'true'
        return 'false'
    
class DistributeHandler(tornado.websocket.WebSocketHandler):
    def open(self,params):
        print 'Parameters: %s' % str(params)
        group,name = params.split('/')
        self.group = group or 'default'
        self.name = name or 'anonymous'
        if not self.group in listeners: listeners[self.group]=[]
        # notify clients that a member has joined the groups
        for client in listeners.get(self.group,[]): 
            client.write_message('+'+self.name)
        listeners[self.group].append(self)
        names[self] = self.name
        print '%s:CONNECT to %s from %s' % (time.time(), self.group, self.name)
        
    def on_message(self, message):
        print message
        for client in listeners.get("shell",[]): 
            client.write_message(message)
        pass
    
    def on_close(self):
        if self.group in listeners: listeners[self.group].remove(self)
        del names[self]
        # notify clients that a member has left the groups
        for client in listeners.get(self.group,[]): client.write_message('-'+self.name)
        print '%s:DISCONNECT from %s' % (time.time(), self.group)

class CommandHandler(tornado.websocket.WebSocketHandler):
    
    def __sendCommand__(self,url,message,group='boxes'):
        params = urllib.urlencode({'message': message, 'group':group})
        f = urllib.urlopen(url, params)
        data= f.read()
        f.close()
        return data
        
    def open(self):
        print 'new connection'
        self.write_message("Welcome to the Shell...\n")
        
    def on_message(self, message):
        print 'Command received:  %s' % message
        self.__sendCommand__("http://127.0.0.1:9002", message)
        
    def on_close(self):
        print 'connection closed'

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


application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/command', CommandHandler),
    (r'/', PostHandler),
    (r'/endpoint/(.*)', DistributeHandler),
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9002)
    tornado.ioloop.IOLoop.instance().start()
