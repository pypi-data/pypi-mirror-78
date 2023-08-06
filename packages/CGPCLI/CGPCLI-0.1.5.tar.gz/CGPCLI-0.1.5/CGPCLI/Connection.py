import socket

from CGPCLI.Errors import FailedLogin, ConnectionTimeOut

def connect(host, port=106):
    '''Create a connection with CGP server via socket
    
    :host str
    :port int
    :rtype socket
    
    '''
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.settimeout(5.0)
        
        sock.send('HELP\n'.encode())
        
        read(sock)
        
        return sock
    except socket.error as e:
        raise e

def login(sock, username, pwd):
    '''Log in CGP Account. Raises an Exception on fail login
    
    :sock socket
    :username str
    :pwd str
    
    '''
    
    check = '515'
    while check != '200':
        sock.send((f'USER {username}\n').encode())
        check = read(sock)            

        sock.send((f'PASS {pwd}\n').encode())
        check = read(sock, get=True)['header'][:3]
        
        if check == '515':
            raise FailedLogin()

def disconnect(sock):
    '''Log in CGP Account
    
    :sock socket
    
    '''
    try:
        sock.send(('QUIT\n').encode())
    except ConnectionAbortedError:
        pass
    
    sock.close()

def read(sock, get=False):
    '''Metod that reads messages from server and returns dict containing server response
    if get parameter is set to True.
    
    Return examples:
    {"header": "200, "body": "OK"}
    {"header": "200 data follow", "body": str}
    
    :sock socket
    :get bool
    :rtype dict
    
    '''
    
    message = {}

    full = ''
    length = 1

    while True:
        try:
            msg = sock.recv(length)
            full += msg.decode()

            if full[-2:] == '\r\n':

                try:
                    if message['header'] != None:
                        message['body'] = full[:-2]
                        break

                except KeyError:
                    message['header'] = full[:-2]

                    length = 4096
                    full = ''

        except ConnectionAbortedError:
            disconnect(sock)
            raise ConnectionTimeOut()

        except socket.timeout:
            break

    if 'get':
        return message