#!/usr/bin/env python
import random
import socket
import time

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
      print

      handle_connection(c)

def handle_connection(conn):
   conn.send('HTTP/1.0 200 OK\r\n')
   conn.send('Content-type: text/html\r\n')
   conn.send('\r\n')
   request = (conn.recv(1000)).split()

   if len(request):
      method = request[0]
      loc = request[1]
      if method == 'POST':
         handle_post(conn)
      else:
         if loc == '/':
            menu = '<h1>/home</h1>' + \
                   '<ul>' + \
                   '<li><a href="./content">content</a></li>' + \
                   '<li><a href="./file">file</a></li>' + \
                   '<li><a href="./image">image</a></li>' + \
                   '</ul>'
            conn.send(menu)
         elif loc == '/content':
            content_html(conn)
         elif loc == '/file':
            file_html(conn)
         elif loc == '/image':
            image_html(conn)

   conn.close()

def handle_post(conn):
   print 'this is a POST method!!'
   conn.send('<h1>this is a post method</h1>')

def content_html(conn):
   conn.send('<h1>/content</h1>')

def file_html(conn):
   conn.send('<h1>/file</h1>')

def image_html(conn):
   conn.send('<h1>/image</h1>')


if __name__ == '__main__':
   main()