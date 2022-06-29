import os
import socket

class CONNECTIVITY:
    def check_connectivity(SERVER_IP, SERVER_PORT):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, SERVER_PORT))
            return True
        except Exception as e:
            print(e)
            return False

