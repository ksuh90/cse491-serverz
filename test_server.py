import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

def status_code(conn):
  return conn.sent[9:12]

def test_handle_index():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    assert status_code(conn) == '200', 'Got: %s' % (repr(conn.sent),)

def test_handle_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    assert status_code(conn) == '200', 'Got: %s' % (repr(conn.sent),)

def test_handle_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    assert status_code(conn) == '200', 'Got: %s' % (repr(conn.sent),)

def test_handle_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    assert status_code(conn) == '200', 'Got: %s' % (repr(conn.sent),)

def test_404():
    conn = FakeConnection("GET /foobar HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    assert status_code(conn) == '404', 'Got: %s' % (repr(conn.sent),)

def test_handle_submit():
  firstname = "K"
  lastname = "Suh"
  conn = FakeConnection("GET /submit?firstname={0}&lastname={1} \
                         HTTP/1.0\r\n\r\n".format(firstname, lastname))
  server.handle_connection(conn)
  assert status_code(conn) == '200', 'Got: %s' % (repr(conn.sent),)  


def test_post_404():
    conn = FakeConnection("POST /foobar HTTP/1.0\r\n" + \
                          "Content-Length: 0\r\n" + \
                          "Content-Type: application/x-www-form-urlencoded\r\n\r\n"
                         )
    server.handle_connection(conn)
    assert status_code(conn) == '404', 'Got: %s' % (repr(conn.sent),)

def test_submit_post_urlencoded():
    firstname = "K"
    lastname = "Suh"
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
                           "Content-Length: 24\r\n" + \
                           "Content-Type: application/x-www-form-urlencoded\r\n\r\n" + \
                           "firstname={0}&lastname={1}\r\n".format(firstname, lastname))

    server.handle_connection(conn)

    assert status_code(conn) == '200', 'Got: %s' % (repr(conn.sent),)

def test_submit_post_multipart():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
                          "Content-Length: 369\r\n" + \
                          "Content-Type: multipart/form-data; " + \
                          "boundary=32452685f36942178a5f36fd94e34b63\r\n\r\n" + \
                          "--32452685f36942178a5f36fd94e34b63\r\n" + \
                          "Content-Disposition: form-data; name=\"lastname\";" + \
                          " filename=\"lastname\"\r\n\r\n" + \
                          "K\r\n" + \
                          "--32452685f36942178a5f36fd94e34b63\r\n" + \
                          "Content-Disposition: form-data; name=\"firstname\";" + \
                          " filename=\"firstname\"\r\n\r\n" + \
                          "Suh\r\n" + \
                          "--32452685f36942178a5f36fd94e34b63\r\n" + \
                          "Content-Disposition: form-data; name=\"key\";" + \
                          " filename=\"key\"\r\n\r\n" + \
                          "value\r\n" + \
                          "--32452685f36942178a5f36fd94e34b63--\r\n"
                    )
    firstname = 'K'
    lastname = 'Suh'

    server.handle_connection(conn)

    assert status_code(conn) == '200', 'Got: %s' % (repr(conn.sent),)