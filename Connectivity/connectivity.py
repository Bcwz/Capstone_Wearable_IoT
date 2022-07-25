import os
import socket

TIMEOUT = 2

class CONNECTIVITY:
    def check_connectivity(SERVER_IP, SERVER_PORT):
        print(SERVER_IP,SERVER_PORT)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(TIMEOUT)
            s.connect((SERVER_IP, SERVER_PORT))
            s.close()
            return True
        except:
            return False

