#!/usr/bin/env python
import random
import socket
import time
<<<<<<< HEAD
from StringIO import StringIO
from urlparse import urlparse, parse_qs
from app import make_app


def handle_connection(conn):
  # a dict to store request data
  env = {}

  # recieve up to header
  request = conn.recv(1)
  while request[-4:] != '\r\n\r\n':
    request += conn.recv(1)

  # define request method, raw headers, path
  first_line, headers = request.split('\r\n', 1)
  first_line = first_line.split(' ')
  method = first_line[0]
  url = urlparse(first_line[1])
  path = 'home' if (url[2] == '/') else url[2]

  # build a header dict
  h = store_header(headers)

  path = urlparse(request.split(' ', 3)[1])
  env['REQUEST_METHOD'] = method
  env['PATH_INFO'] = path[2]
  env['QUERY_STRING'] = path[4]
  env['CONTENT_TYPE'] = 'text/html'
  env['CONTENT_LENGTH'] = 0

  def start_response(status, response_headers):
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')
        for pair in response_headers:
            key, header = pair
            conn.send(key + ': ' + header + '\r\n')
        conn.send('\r\n')

  content = ''
  if method == 'POST':
    env['CONTENT_LENGTH'] = h['content-length']
    env['CONTENT_TYPE'] = h['content-type']
    content = get_content(conn, h)


  env['wsgi.input'] = StringIO(content)
  ze_app = make_app()
  r = ze_app(env, start_response)
  for data in r:
    conn.send(data)

  conn.close()


def store_header(raw_headers):
  # map headers to a dict
  h = {}
  for line in raw_headers.split('\r\n')[:-2]:
    k, v = line.split(': ', 1)
    h[k.lower()] = v
  return h


def get_content(conn, headers):
  # receive the content portion
  content = ''
  length = int(headers['content-length'])
  while len(content) < length:
    content += conn.recv(1)
  return content


def main():
  s = socket.socket()         # Create a socket object
  host = socket.getfqdn()     # Get pathal machine name
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

if __name__ == '__main__':
  main()
=======

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
    c.send('HTTP/1.0 200 OK\r\n')
    c.send('Content-Type: text/html\r\n\r\n')
    c.send("<h1>Hello, world</h1> this is suhkang's Web server.")
    c.close()

>>>>>>> master
