#!/usr/bin/env python
import argparse
import random
import socket
import time
from StringIO import StringIO
from urlparse import urlparse, parse_qs
from app import make_my_app

import quixote
from quixote.demo import create_publisher
from quixote.demo.mini_demo import create_publisher
from quixote.demo.altdemo import create_publisher
#from wsgiref.validate import validator
from wsgiref.simple_server import make_server

import quotes
import chat
import cookieapp
import imageapp
imageapp.setup()



_the_app = None

# to run quixote

def make_app(app_name):

  global _the_app

  if _the_app is None:
    if app_name == 'altdemo':
      p = create_publisher()
    else:
      p = imageapp.create_publisher()
    _the_app = quixote.get_wsgi_app()

  return _the_app



def handle_connection(conn, host, port, app_name):
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
  env['HTTP_COOKIE'] = h['cookie'] if 'cookie' in h.keys() else ''

  # contruct env
  buf = StringIO(request)
  buf.readline()
  while True:
        line = buf.readline()
        if line == '\r\n' or line == '':
            break # empty line = end of headers section
        if ': ' in line:
            key, value = line.strip('\r\n').split(": ",1)
            key = key.upper().replace('-','_')
            env[key] = value


  if 'COOKIE' in env.keys():
    env['HTTP_COOKIE'] = env['COOKIE']


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

    #if 'content-type' not in h:
     # h['content-type'] = 'text/html'
    try:
      environ['CONTENT_TYPE'] = headers['content-type']
    except:
      pass
      
    #env['CONTENT_TYPE'] = h['content-type']

    content = get_content(conn, h)



  env['wsgi.input'] = StringIO(content)

  #if make_app == ''
  if app_name == 'myapp':
    ze_app = make_my_app()

  elif app_name == 'quotes':
    quotes_dir = './quotes/'
    ze_app = quotes.make_quotes_app(quotes_dir + 'quotes.txt', quotes_dir + 'html')
  elif app_name == 'chat':
    ze_app = chat.make_chat_app('./chat/html')
  elif app_name == 'cookie':
    ze_app = cookieapp.wsgi_app
  else:
    ze_app = make_app(app_name)


  r = ze_app(env, start_response)


  # validator
  # validator_app = validator(ze_app)
  # r = validator_app(env, start_response)

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


def get_args():
  app_list = ['altdemo', 'image', 'myapp', 'quotes', 'chat', 'cookie']
  parser = argparse.ArgumentParser()
  parser.add_argument('-A', action = "store",
                            dest = 'arg_app',
                            help = "The application to run")
  parser.add_argument('-p', action = "store",
                            default = 0,
                            dest = 'arg_port',
                            help = "The port to use (optional)",
                            required = False,
                            type = int)
  result = parser.parse_args()
  if result.arg_app not in app_list:
      print '\nError, that application does not exist\n'
      exit()
  return result.arg_app, result.arg_port


def main():

  app, port = get_args()
 

  s = socket.socket()         # Create a socket object
  host = socket.getfqdn()     # Get pathal machine name
  if (port == 0):
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


    handle_connection(c, host, port, app)
  
if __name__ == '__main__':
  main()
