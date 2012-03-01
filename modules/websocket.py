import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import subprocess


class CommandHandler(tornado.websocket.WebSocketHandler):
    
    def __execute__(self, cmd, args=None):
            if args == None:
                command = cmd
            else:
                command = [cmd,args]
            proc = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdout = proc.stdout.read() + proc.stderr.read()
            return stdout
        
    def open(self):
        print 'new connection'
        self.write_message("Hello Client!")
        
    def on_message(self, message):
        print 'Command received:  %s' % message
        cmd = message
        output = self.__execute__(cmd, args=None)
        print 'Sending Output: %s' % output
        self.write_message(output)
        
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
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
