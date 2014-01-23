#!/usr/bin/env python
import random
import socket
import time

def handle_connection(conn):
	request = conn.recv(1000)
	request = request.split('\r\n')
	r_type = request[0].split(' ')
	
	type = r_type[0]
	
	if type == "GET":
		if r_type[1] == "/":
			conn.send("HTTP/1.0 200 OK\r\n")
			conn.send("Content-Type: text/html\r\n\r\n")
			conn.send("<html>\r\n")
			conn.send("<body>\r\n")
			conn.send("<h1>Hello World</h1>This is QSSS's web server\r\n")
			conn.send("a href='/content'>Content</a><br>")
			conn.send("a href='/files'>Files</a><br>")
			conn.send("a href='/images'>Images</a>")
			conn.send("</body>\r\n")
			conn.send("</html>\r\n")
		if r_type[1] == "/content":
			conn.send("HTTP/1.0 200 OK\r\n")
			conn.send("Content-Type: text/html\r\n\r\n")
			conn.send("<html>\r\n")
			conn.send("<body>\r\n")
			conn.send("<h1>Content</h1>")
			conn.send("Here is the content")
			conn.send("</body>\r\n")
			conn.send("</html>\r\n")
		if r_type[1] == "/files":
			conn.send("HTTP/1.0 200 OK\r\n")
			conn.send("Content-Type: text/html\r\n\r\n")
			conn.send("<html>\r\n")
			conn.send("<body>\r\n")
			conn.send("<h1>Files</h1>")
			conn.send("Here are the files")
			conn.send("</body>\r\n")
			conn.send("</html>\r\n")
		if r_type[1] == "/images":
			
			conn.send("HTTP/1.0 200 OK\r\n")
			conn.send("Content-Type: text/html\r\n\r\n")
			conn.send("<html>\r\n")
			conn.send("<body>\r\n")
			conn.send("<h1>Images</h1>")
			conn.send("Here are the images")
			conn.send("</body>\r\n")
			conn.send("</html>\r\n")
		else:
			conn.send("HTTP/1.0 404 Not Found\r\n")
			conn.send("Content-Type: text/html\r\n\r\n")
			conn.send("<html>\r\n")
			conn.send("<body>\r\n")
			conn.send("<h1>404</h1>")
			conn.send("Page not found")
			conn.send("</body>\r\n")
			conn.send("</html>\r\n")
	elif type == "POST":
		conn.send("HTTP/1.0 200 OK\r\n")
		conn.send("Content-Type: text/html\r\n\r\n")
		conn.send("<html>\r\n")
		conn.send("<body>\r\n")
		conn.send("<h1>Hello World</h1>")
		conn.send("</body>\r\n")
		conn.send("</html>\r\n")
	conn.close()
	
def main():
	s = socket.socket()         # Create a socket object
	host = socket.getfqdn() # Get local machine name
	port = random.randint(8000, 9999)
	s.bind((host, port))        # Bind to the port

	print 'Starting server on', host, port
	print 'The Web server URL for this would be http://%s:%d/' % (host, port)

	s.listen(5)                 # Now wait for client connection.
	print 'Entering infinite loop; hit CTRL-C to exit'


	while True:
		# Establish connection with client.    
		c, (client_host, client_port) = s.accept()
		print 'Got connection from', client_host, client_port
		handle_connection(s);
	
 

if	__name__ == '_main_':
	main()

