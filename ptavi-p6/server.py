#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import socketserver

USAGE_ERROR = 'Usage: python3 server.py IP port audio_file'
METHODS_ALLOWED = 'INVITE', 'ACK', 'BYE'

try:
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    if os.path.exists(sys.argv[3]):
        AUDIO_FILE = sys.argv[3]
    else:
        sys.exit('File not found')
except:
    sys.exit(USAGE_ERROR)

MP32RTP = './mp32rtp -i 127.0.0.1 -p 23032 < ' + AUDIO_FILE
OK = b'SIP/2.0 200 OK\r\n'
TRY_RING = b'SIP/2.0 100 Trying\r\nSIP/2.0 180 Ring\r\n'
BAD_REQUEST = b'SIP/2.0 400 Bad Request\r\n'
METHOD_NOT_ALLOWED = b'SIP/2.0 405 Method Not Allowed\r\n'


class RTPHandler(socketserver.DatagramRequestHandler):

    def handle(self):
        message = self.rfile.read()
        line = message.decode('utf-8').split()
        if len(line) == 3 and line[2] == 'SIP/2.0':
            method = line[0]
            if method in METHODS_ALLOWED:
                print(method + ' received')
                if method == 'INVITE':
                    self.wfile.write(TRY_RING + OK + b'\r\n')
                elif method == 'ACK':
                    os.system(MP32RTP)
                elif method == 'BYE':
                    self.wfile.write(OK + b'\r\n')
            else:
                self.wfile.write(METHOD_NOT_ALLOWED + b'\r\n')
        else:
            self.wfile.write(BAD_REQUEST + b'\r\n')

if __name__ == '__main__':
    server = socketserver.UDPServer((IP, PORT), RTPHandler)
    print('Listening...')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('End server')
