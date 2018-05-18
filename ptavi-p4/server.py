#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import socketserver
from datetime import datetime, date, time, timedelta

"""
Se consigue el puerto en el que se atará el servidor mediante
el comando introducido al ejecutarlo
"""
USAGE = 'python3 server.py <port>'
if len(sys.argv) != 2:
    sys.exit('usage error: ' + USAGE)
else:
    try:
        PORT = int(sys.argv[1])
        FORMAT = '%H:%M:%S %d-%m-%Y'
    except:
        sys.exit('usage error: ' + USAGE)


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    dicc = {}

    def json2register(self):
        """
        Utilizar contenido de registered.json como diccionario
        """
        try:
            with open('registered.json', 'r') as jsonfile:
                """
                Si el fichero existe, se crea el diccionario
                con el contenido del fichero
                """
                self.dicc = json.load(jsonfile)
        except:
            """
            En cualquier otro caso, el diccionario se mantiene
            """
            pass

    def register2json(self):
        """
        Escribir diccionario en formato json
        en el fichero registered.json
        """
        with open('registered.json', 'w') as jsonfile:
            json.dump(self.dicc, jsonfile, indent=3)

    def handle(self):

        """
        Se crea el diccionario desde el fichero registered.json
        """
        self.json2register()
        user_dicc = {'address': '', 'expires': ''}
        IP = self.client_address[0]
        PORT = self.client_address[1]
        list = []
        for line in self.rfile:
            list.append(line.decode('utf-8'))
        message = list[0].split(' ')
        """
        Se comprueba que el primer campo sea REGISTER
        """
        if message[0] == 'REGISTER':
            user = message[1].split(':')[1]
            message = list[1].split()
            expires = message[1].split('\r\n')[0]
            """
            Se añade la informacion del usuario al diccionario
            """
            expires_date = datetime.now() + timedelta(seconds=int(expires))
            user_dicc['address'] = IP + ':' + str(PORT)
            user_dicc['expires'] = expires_date.strftime(FORMAT)
            """
            Si su expired es distinto de 0, el register lo guarda
            en el fichero registered.json
            Si su expired es 0, se elimina al cliente del diccionario
            y se guarda de nuevo en el fichero registered.json
            """
            if int(expires) == 0:
                """
                Se envia el mensaje SIP y se elimina al usuario
                """
                try:
                    del self.dicc[user]
                    self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
                except KeyError:
                    """
                    En el caso de que no este en el diccionario,
                    se continua
                    """
                    pass
            else:
                """
                Se añade el usuario al diccionario
                """
                self.dicc[user] = user_dicc
                self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
                """
                Se comprueba si algun cliente tiene la sesion caducada
                si la sesion ha caducado, se elimina al cliente y se
                modifica el fichero registered.json
                """
                Now = datetime.now().strftime(FORMAT)
                user_del = []
                for user in self.dicc:
                    if Now >= self.dicc[user]['expires']:
                        user_del.append(user)
                for user in user_del:
                    del self.dicc[user]
            self.register2json()

if __name__ == '__main__':
    """
    Se crea el servicio UDP en el puerto indicado por comando utilizando
    la clase SIPRegisterHandler
    """
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print('Starting server...\n')
    try:
        """
        Se crea el servidor
        """
        serv.serve_forever()
    except KeyboardInterrupt:
        print('End server')
