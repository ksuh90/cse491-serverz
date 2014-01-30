#!/usr/bin/env python
import random
import socket
import time
import urlparse

# global header string
header = 'HTTP/1.0 200 OK\r\n' + \
         'Content-type: text/html\r\n' + \
         '\r\n'


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
   request = (conn.recv(1000))

   if len(request):
      f_line = request.splitlines()[0].split(' ')
      method = f_line[0]
      url = urlparse.urlparse(f_line[1])
      loc = url[2]
      if method == 'POST':
         if loc == '/submit':
            handle_submit(conn, request.split('\r\n')[-1])
         else:
            handle_post(conn, '')
      else:
         if loc == '/':
            index_html(conn, '')
         elif loc == '/content':
            content_html(conn, '')
         elif loc == '/file':
            file_html(conn, '')
         elif loc == '/image':
            image_html(conn, '')
         elif loc == '/form':
            form_html(conn, '')
         elif loc == '/submit':
            handle_submit(conn, url[4])

   conn.close()

def handle_submit(conn, url):
   q = url.split('&')
   firstname = q[0].split('=')[1]
   lastname = q[1].split('=')[1]
   conn.send(header + "<p>Hello Mr. %s %s.</p>" % (firstname, lastname))

def handle_post(conn, url):
   print 'this is a POST method!!'
   conn.send(header + '<h1>this is a post method</h1>')

def index_html(conn, url):
   conn.send(header + \
             '<h1>/home</h1>' + \
             '<ul>' + \
             '<li><a href="./content">content</a></li>' + \
             '<li><a href="./file">file</a></li>' + \
             '<li><a href="./image">image</a></li>' + \
             '<li><a href="./form">form</a></li>' + \
             '</ul>')

def content_html(conn, url):
   conn.send(header + '<h1>/content</h1>')

def file_html(conn, url):
   conn.send(header + '<h1>/file</h1>')

def image_html(conn, url):
   conn.send(header + '<h1>/image</h1>')

def form_html(conn, url):
   conn.send(header + '<h1>/form</h1>' + \
              "<form action='/submit' method='GET'>" + \
              "first name: <input type='text' name='firstname'></br>" + \
              "last name: <input type='text' name='lastname'><br>" + \
              "<input type='submit' value='Submitz'></br>" + \
              "</form>")

   
if __name__ == '__main__':
   main()
