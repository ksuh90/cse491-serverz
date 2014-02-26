
import cgi
import jinja2
from urlparse import parse_qs


# { path : html form }
response = {
            '/'        : 'index.html',
            '/content' : 'content.html',
            '/file'    : 'file.html',
            '/image'   : 'image.html',
            '/form'    : 'form.html',
            '/submit'  : 'submit.html',
           }


def app(environ, start_response):
    # initialize jinja2 variables
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)

    # initialize header values
    status = '200 OK'

    response_headers = [('Content-type', 'text/html')]

    if environ['PATH_INFO'] in response:
        template = env.get_template(response[environ['PATH_INFO']])
        if environ['PATH_INFO'] == '/image':
            response_headers = [('Content-type', 'image/jpg')]
    else:
        status = '404 Not Found'
        template = env.get_template('404.html')

    # setting up template params
    x = parse_qs(environ['QUERY_STRING']).iteritems()
    args = {k : v[0] for k,v in x}
    args['path'] = environ['PATH_INFO']

    # handle POST method
    if environ['REQUEST_METHOD'] == 'POST':
        headers = {k[5:].lower().replace('_','-') : v \
                    for k,v in environ.iteritems() if(k.startswith('HTTP'))}
        headers['content-type'] = environ['CONTENT_TYPE']
        headers['content-length'] = environ['CONTENT_LENGTH']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], \
                                headers=headers, environ=environ)
        args.update({x : form[x].value for x in form.keys()})

    args = {unicode(k, "utf-8") : unicode(v, "utf-8") for k,v in args.iteritems()}
    
    start_response(status, response_headers)

    # retun the image when '/image'
    if args['path'] == '/image':
        return handle_image()

    return [bytes(template.render(args))]


def handle_image():
    fp = open('./img/sparty.jpg', 'rb')
    data = fp.read()
    fp.close()
    return data


def make_app():
    return app
