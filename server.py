#!/usr/bin/env python
import random
import socket
import time
import jinja2
import cgi
from StringIO import StringIO
from urlparse import urlparse, parse_qs

# { path : html response }
response = {
            '/'        : 'index.html',
            '/content' : 'content.html',
            '/file'    : 'file.html',
            '/image'   : 'image.html',
            '/form'    : 'form.html',
            '/submit'  : 'submit.html',
           }

def handle_connection(conn):
  # initialize jinja2 variables
  loader = jinja2.FileSystemLoader('./templates')
  env = jinja2.Environment(loader=loader)

  # recieve up to header
  request = conn.recv(1)
  while request[-4:] != '\r\n\r\n':
    request += conn.recv(1)

  # define request method, raw headers, path
  first_line, headers = request.split('\r\n', 1)
  first_line = first_line.split(' ')
  method = first_line[0]
  url = urlparse(first_line[1])
  path = url[2]

  # build a header dict
  h = store_header(headers)

  url_dict = parse_qs(url[4])
  content = ''

  if method == 'POST':
    content = get_content(conn, h)

  # cgi stuff
  environ = {}
  environ['REQUEST_METHOD'] = 'POST'
  form = cgi.FieldStorage(fp=StringIO(content), headers=h, environ=environ)
  url_dict.update(dict([(x, [form[x].value]) for x in form.keys()]))

  if path in response:
    template = env.get_template(response[path])
    resp = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
  else:
    template = env.get_template('404.html')
    url_dict['path'] = path
    resp = 'HTTP/1.0 404 Not Found\r\n\r\n'

  resp += template.render(url_dict)
  conn.send(resp)
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
