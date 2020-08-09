import socket
import sys
host = ""
port = 9999
import json
import threading

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

addr = []

def send_data(server_data):
	"""This is for sending data to server"""
	val = 0
	while val !=len(server_data):
		val += conn.send(server_data)
		server_data = server_data[val:]

def connect(name):
	"""This is used to connect to server"""
	s.connect((host,port))
	name = name.encode('utf-8')
	content_length = str(len(name))
	header = {
	'address': 'Server',
	'content_length': content_length
	}
	header = json.dumps(header).encode('utf-8')
	header_length = str(len(header)).encode('utf-8')
	server_data = header_length + header + name
	s.send(server_data)
	header_length = int(s.recv(2).decode('utf-8'))
	header = b""
	for _ in header_length:
		header+=s.recv(1)
	header = header.decode('utf-8')
	header = json.loads(header)
	content_length = header.get('content_length')
	if name_length == 0:
		print("So sorry no online users")
		return
	connection_name = b""
	for _ in name_length:
		connection_name+=s.recv(1)
	connection_name = connection_name.decode('utf-8')
	print(f'You are now connected to {connection_name}\n')



def startchat():
	data = input()
	if data == 'quit':
		return 0
	data = data.encode('utf-8')
	content_length = len(data)
	header = {
	'content_length':content_length
	}
	header = json.dumps(header).encode('utf-8')
	header_length = str(len(header)).encode('utf-8')
	data_send = header_length+header+data
	send_data(data_send)
	return 1

def recv_data():
	header_length = s.recv(2)
	header_length = int(header_length.decode('utf-8'))
	header = b''
	for i in range(0,header_length):
		header += s.recv(1)
	header = json.loads(header.decode('utf-8'))
	recieved_from = header.get('sent_from')
	content_length = int(header.get('content_length'))
	data = b''
	for i in range(0, content_length):
		data += s.recv(1)
	data = data.decode('utf-8')
	print(f"{recieved_from}>")
	print(data)

def main():
	recieve = threading.thread(recv_data, daemon = True)
	print('Thank you for using the Chat Application\n')
	print("It's very secure and send's message directly to anonymous user. Without any kind of storage.\n")
	print('To quit please type "quit"')
	name = input('Enter your name')
	print("You are now being connected to random user...\n")
	connect(name)
	recieve.start()
	while True:
		val = startchat()
		if val ==0:
			break

main()