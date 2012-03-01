# -*- coding: utf-8 -*-
from ws4py.client.threadedclient import WebSocketClient

class EchoClient(WebSocketClient):
    def opened(self):
        self.send("ls")

    def closed(self, code, reason):
        print "Closed down", code, reason

    def received_message(self, m):
        print "=> %d %s" % (len(m), str(m))
	response = raw_input("Type a Response: ")
	self.send(response)


if __name__ == '__main__':
    try:
        ws = EchoClient('http://localhost:8888/command', protocols=['http-only', 'chat'])
        ws.connect()
    except KeyboardInterrupt:
        ws.close()
