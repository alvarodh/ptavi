#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import socket

USAGE_ERROR = 'Usage: python3 client.py method receiver@IP:SIPport'
METHODS = 'INVITE', 'ACK', 'BYE'

try:
    method = str.upper(sys.argv[1])
    sip_name = sys.argv[2].split('@')[0]
    sip_IP = sys.argv[2].split('@')[1].split(':')[0]
    sip_port = int(sys.argv[2].split(':')[1])
except:
    sys.exit(USAGE_ERROR)

mess = ' sip:' + sip_name + '@' + sip_IP + ':' + str(sip_port)
LINE = method + mess + ' SIP/2.0\r\n'

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((sip_IP, sip_port))

    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)

    line = data.decode('utf-8').split('\r\n')
    if line[0].split()[-1] == 'Trying' and method == 'INVITE':
        print(line[0] + '\n' + line[1] + '\n' + line[2])
        my_socket.send(bytes(LINE.replace('INVITE', 'ACK'), 'utf-8') + b'\r\n')
    else:
        print(line[0])
