#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import optparse
import sys
from ws4py.client.threadedclient import WebSocketClient

__author__ = "f47h3r - Chase Schultz"

class runTime():
    
    def sendCommand(self,url,message,group='boxes'):
        params = urllib.urlencode({'message': message, 'group':group})
        try:
            f = urllib.urlopen(url, params)
        except IOError:
            raise IOError('Connection To Listener Terminated. Exiting.')
            sys.exit(1)
        f.read()
        f.close()
        pass

class WSShell(WebSocketClient):
    ip = ''
    port = ''
    runner = runTime();

    def opened(self):
        runner = runTime();
        message = raw_input('>')
        runner.sendCommand("http://"+self.ip+":"+self.port, message)
        pass

    def closed(self, code, reason):
        print "Closed down", code, reason

    def received_message(self, cmd):
        print "Command Output:\n%s \n\n Total Length: %d\n\n" % (str(cmd), len(cmd))
        message = raw_input('>')
        runner.sendCommand("http://"+self.ip+":"+self.port, message)

        

if __name__ == "__main__":
    usage = __doc__
    version= "0.01"
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
    runner = runTime();
    try:
        ws = WSShell('http://'+options.ip+':'+options.port+'/endpoint/shell/box1', protocols=['http-only', 'chat'])
        ws.ip = options.ip
        ws.port = options.port
        ws.connect()
    except KeyboardInterrupt:
        ws.close()