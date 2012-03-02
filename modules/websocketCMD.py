#!/usr/bin/env python

import urllib
from ws4py.client.threadedclient import WebSocketClient

class runTime():
    
    def sendCommand(self,url,message,group='boxes'):
        params = urllib.urlencode({'message': message, 'group':group})
        f = urllib.urlopen(url, params)
        data= f.read()
        f.close()
        return data

class WSShell(WebSocketClient):

    def opened(self):
        runner = runTime();
        message = raw_input('>')
        runner.sendCommand("http://127.0.0.1:9002", message)
        pass

    def closed(self, code, reason):
        print "Closed down", code, reason

    def received_message(self, cmd):
        print "Command Output:\n%s \n\n Total Length: %d\n\n" % (str(cmd), len(cmd))
        runner = runTime();
        message = raw_input('>')
        runner.sendCommand("http://127.0.0.1:9002", message)
        

if __name__ == "__main__":    
    runner = runTime();
    try:
        ws = WSShell('http://localhost:9002/endpoint/shell/box1', protocols=['http-only', 'chat'])
        ws.connect()
    except KeyboardInterrupt:
        ws.close()