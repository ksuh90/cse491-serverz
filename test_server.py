import server

# global header string
header = 'HTTP/1.0 200 OK\r\n' + \
         'Content-type: text/html\r\n' + \
         '\r\n'

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

# Test a basic GET call.

def test_handle_index():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")

    expected_return = header + \
                      '<h1>/home</h1>' + \
                      '<ul>' + \
                      '<li><a href="./content">content</a></li>' + \
                      '<li><a href="./file">file</a></li>' + \
                      '<li><a href="./image">image</a></li>' + \
                      '<li><a href="./form">form</a></li>' + \
                      '</ul>'

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = header + '<h1>/content</h1>'

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = header + '<h1>/file</h1>'

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = header + '<h1>/image</h1>'

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_post():
    conn = FakeConnection("POST /image HTTP/1.0\r\n\r\n")
    expected_return = header + '<h1>this is a post method</h1>'

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    expected_return = header + \
                      '<h1>/form</h1>' + \
                      "<form action='/submit' method='GET'>" + \
                      "first name: <input type='text' name='firstname'></br>" + \
                      "last name: <input type='text' name='lastname'><br>" + \
                      "<input type='submit' value='Submitz'></br>" + \
                      "</form>"
    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_submit():
    expected_return = header + '<p>Hello Mr. KangOne Suh.</p>'
    # GET
    conn = FakeConnection('GET /submit?firstname=KangOne&lastname=Suh ' +\
                                  'HTTP/1.0\r\n\r\n')
    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

    # POST
    conn = FakeConnection('POST /submit HTTP/1.0\r\n\r\n' + \
                          'firstname=KangOne&lastname=Suh')
    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)