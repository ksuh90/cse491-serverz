import os
import cgi
import jinja2
from urlparse import parse_qs


# { path : html tpl }
response = {
            '/'        : 'index.html',
            '/content' : 'content.html',
            '/file'    : 'file.html',
            '/image'   : 'image.html',
            '/form'    : 'form.html',
            '/submit'  : 'submit.html',
            '/thumbnails' : 'thumbnails.html'
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

    # return the image on '/image'
    if args['path'] == '/image':
        path = './img/sparty.jpg'
        return get_image(path)


    # retun the text file on '/file'
    if args['path'] == '/file':
        return handle_text_file()

    if args['path'] == '/thumbnails':
        args = dict(names=get_contents('img'))

    if environ['PATH_INFO'][:5] == '/pics':
        return get_pics(environ['PATH_INFO'][5:])

    if environ['path'] == '/comment_process':
        #form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        title = str(form['title'].value)
        body = str(form['body'].value)

        #new_messages = self.get_messages_since(last_time)
        #xml = self.format_response(new_messages, time.time())

        # done; return whatever we've got.
        start_response("200 OK", [('Content-type', 'text/html')])
        print "HAHAHAHAHHAA"
         
        print 'title : ' + title
        print 'body : ' + body
        return 1
 

    return [bytes(template.render(args))]


def get_image(path):
    fp = open(path, 'rb')
    data = fp.read()
    fp.close()
    return data

def get_pics(path):
    return get_image('./img/' + path)


def handle_text_file():
    fp = open('./files/text.txt', 'rb')
    data = fp.read()
    fp.close()
    return data

def get_contents(dir):
    contents = []
    for file in sorted(os.listdir(dir)):
        contents.append(file)
    return contents


def make_my_app():
    return app