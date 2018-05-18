import sys
import socket

"""
Se establece el texto que aparecerá en el caso de un usage error
"""
USAGE = 'python3 client.py'
USAGE += '<ip|host> <port> <register> <sip_address> <expires_value>'
"""
Se extrae de los comandos introducidos en la ejecución los datos
necesarios para la comunicacion con el servidor
"""
if len(sys.argv) != 6:
    sys.exit('Usage: ' + USAGE)
else:
    try:
        SERVER = sys.argv[1]
        PORT = int(sys.argv[2])
        METODO = str.upper(sys.argv[3])
        USER = sys.argv[4]
        EXPIRES = int(sys.argv[5])
        REGISTERSIP = METODO + ' sip:' + USER + ' SIP/2.0\r\n'
        EXPIRESSIP = 'Expires: ' + str(EXPIRES) + '\r\n\r\n'
    except IndexError:
        sys.exit('Usage: ' + USAGE)

"""
Si se trata de un mensaje del tipo register, lo envia
"""
if METODO == 'REGISTER':
    LINE = REGISTERSIP + EXPIRESSIP
else:
    sys.exit('Usage: ' + USAGE)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    print("Sending:", METODO, 'SIP')
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print('Received -- ', data.decode('utf-8'))

print("Socket terminado.")
