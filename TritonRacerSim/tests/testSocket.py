import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 9091)
sock.connect(server_address)

#msg = b'{"msg_type" : "ping"}\n'
#car_config = b"""{"msg_type" : "car_config","body_style" : "car01","body_r" : "128","body_g" : "0","body_b" : "255","car_name" : "Your Name","font_size" : "100"}\n"""
msg = {"msg_type" : "get_protocol_version"}
msg = bytes(json.dumps(msg),'utf-8')

#sock.sendall(car_config)
sock.sendall(msg)

data_back = ''

while True:
    data = sock.recv(16)
    print (data.decode('utf-8'))


