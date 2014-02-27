#!/usr/bin/env python
import random
import socket
import time
from StringIO import StringIO
from urlparse import urlparse, parse_qs
from app import make_app

import quixote
from quixote.demo import create_publisher
#from quixote.demo.mini_demo import create_publisher
#from quixote.demo.altdemo import create_publisher
from wsgiref.validate import validator
from wsgiref.simple_server import make_server

_the_app = None

# to run quixote
'''
def make_app():
  global _the_app

  if _the_app is None:
    p = create_publisher()
    _the_app = quixote.get_wsgi_app()

  return _the_app
'''

def get_content(conn, headers):
  # receive the content portion
  content = ''
  length = int(headers['content-length'])
  while len(content) < length:
    content += conn.recv(1)
  return content


def store_header(raw_headers):
  # map headers to a dict
  h = {}
  for line in raw_headers.split('\r\n')[:-2]:
    k, v = line.split(': ', 1)
    h[k.lower()] = v

  return h


def handle_connection(conn):
  # a dict to store request data
  env = {}

  # recieve up to header
  request = conn.recv(1)
  while request[-4:] != '\r\n\r\n':
    request += conn.recv(1)

  
  first_line, headers = request.split('\r\n', 1)
  first_line = first_line.split(' ')

  # allocate request method, raw headers, path, scheme...
  method = first_line[0]
  url = urlparse(first_line[1])
  protocol = first_line[2]
  url_scheme = first_line[2].split('/')[0]
  path = 'home' if (url[2] == '/') else url[2]

  # build a header dict
  h = store_header(headers)

  path = urlparse(request.split(' ', 3)[1])
  
  # pre-construct env
  env['REQUEST_METHOD'] = method
  env['PATH_INFO'] = path[2]
  env['QUERY_STRING'] = path[4]
  env['CONTENT_TYPE'] = 'text/html'
  env['CONTENT_LENGTH'] = '0'
  env['SCRIPT_NAME'] = ''
  env['SERVER_NAME'] = host
  env['SERVER_PORT'] = str(port)
  env['SERVER_PROTOCOL'] = protocol
  env['wsgi.version'] = (1, 0)
  env['wsgi.errors'] = StringIO()
  env['wsgi.multithread'] = False
  env['wsgi.multiprocess'] = False
  env['wsgi.run_once'] = False
  env['wsgi.url_scheme'] = url_scheme.lower()

  # contruct env
  buf = StringIO(request)
  buf.readline()
  while True:
        line = buf.readline()
        if line == '\r\n' or line == '':
            break # end of header
        if ': ' in line:
            key, value = line.strip('\r\n').split(": ",1)
            key = key.upper().replace('-','_')
            env[key] = value

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

  # validator
  # validator_app = validator(ze_app)
  # r = validator_app(env, start_response)

  for data in r:
    conn.send(data)

  conn.close()


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
