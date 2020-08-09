import socket
import sys
import threading
host = ""
port = 9999
import random
from _thread import *
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(50)
connections = []
address = []
names = []

print_lock = threading.Lock()


def accept_connection():
	while True:
		conn, addr = s.accept()
		print_lock.acquire()
		print("Connected to ", addr)
		name_length = int(conn.recv(2).decode('utf-8'))
		name = b""
		for _ in name_length:
			name+=conn.recv(1)
		name = name.decode('utf-8')
		connections.append(conn)
		address.append(address)
		names.append(name)
		random = random.uniform(0, connections.length())
		addr = address[random]
		name = names[random]
		data = {
			'address':addr,
			'name':name
		}
		data = json.dumps(data)
		data = data.encode('utf-8')
		content_length = len(data)
		sent_header = {
		'sent_from':'Server',
		'content_length':content_length
		}
		sent_header = sent_header.encode('utf-8')
		header_length = str(len(sent_header)).encode('utf-8')
		client_data = header_length+sent_header+data
		send_data(conn, client_data)
		start_new_thread(load_header, (conn,))


def chat(addr, content_length):
	data = b''
	for i in range(0, content_length):
		data +=conn.recv(1)
	sent_header = {
		'sent_from':addr,
		'content_length':content_length
	}
	sent_header = json.dumps(sent_header).encode('utf-8')
	header_length = str(len(sent_header)).encode('utf-8')
	client_data = header_length + sent_header + data
	i = address.index(addr)
	conn = connections[i]
	send_data(conn, client_data)
	

def send_data(conn, client_data):
	val = 0
	while val !=len(client_data):
		val += conn.send(client_data)
		client_data = client_data[val:]


def list_conn(conn):
	data = "Active connections now:\n"
	for addr in address:
		data+=f"{addr}\n"
	data = data.encode('utf-8')
	content_length = len(data)
	sent_header = {
		'sent_from':"Server",
		"content_length": content_length
	}
	sent_header = json.dumps(sent_header).encode('utf-8')
	header_length = str(len(sent_header)).encode('utf-8')
	client_data = header_length + sent_header + data
	send_data(conn, client_data)


def load_header(conn):
	while True:
		"""Consider the header length value to be first one which is 2 bytes"""
		data = conn.recv(2)
		if not data:
			print_lock.release()
		val = int(data.decode('utf-8'))
		print("length here", val)
		data = b''
		for i in range(0, val):
			data+= conn.recv(1)
		data = (data.decode('utf-8'))
		#######Here I get the headers#########
		#It will contain the contacting information as well as content length etc#
		header = json.loads(data)
		to_send = header.get('address')	# The address
		content_length = header.get('content_length')
		content_type = headers.get('content_type', "")
		if content_type=='execute':
			list_conn(conn)
		else:
			chat(to_send, content_length)



if __name__ == '__main__':
	accept_thread = threading.Thread(target = accept_connection, daemon = True)
	process = threading.Thread(target= load_header, daemon=True)
	accept_thread.start()
	process.start()
	accept_thread.join()
	process.join()
	s.close()