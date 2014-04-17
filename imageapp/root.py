import quixote
from quixote.directory import Directory, export, subdir
from quixote.util import StaticFile
import os.path
import requests
import json

from . import html, image, style

class RootDirectory(Directory):
    _q_exports = []

    @export(name='')                    # this makes it public.
    def index(self):
        return html.render('index.html')

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(the_file.get_size())

        #image.add_image(data)
        image.add_image(the_file.base_filename, data)

        return quixote.redirect('./')

    @export(name='image')
    def image(self):
        return html.render('image.html')



    @export(name='image_count')
    def image_count(self):
        return image.get_num_images()



    @export(name='image_raw')
    def image_raw(self):

        response = quixote.get_response()
        request = quixote.get_request()

        try:
            i = int(request.form['num'])
        except:
            i = -1

        # img = retrieve_image(request)
        img = image.retrieve_image(i)

       
        filename = img.filename

        if filename.lower() in ('jpg', 'jpeg'):
            response.set_content_type('image/jpeg')
        elif filename.lower() in ('tif',' tiff'):
            response.set_content_type('image/tiff')
        else:
            response.set_content_type('image/png')
        return img.data


    @export(name='style')
    def style(self):

        response = quixote.get_response()
        request = quixote.get_request()

        style = retrieve_style(request)

        response.set_content_type('text/css')

        return style.data



    @export(name='list_of_images')
    def list_of_images(self):
        return html.render('list_of_images.html')



    @export(name='image_count')
    def image_count(self):
        return len(image.images)


    @export(name='add_comment')
    def add_comment(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            name = str(request.form['name'])
        except:
            name = 'no name'

        try:
            body = str(request.form['body'])
        except:
            body = ''

        image.add_comment(name, body)


    @export(name='get_comments')
    def get_comments(self):
        response = quixote.get_response()
        request = quixote.get_request()

        resp = requests.get(
            "https://cse491.cloudant.com/imageapp/comments",
            auth=('cse491', 'serverz491')
        )
        resp = json.loads(resp.text)
        
        out = ''

        for comment in resp['comments']:
            tr = '<tr><td>%s</td><td>%s</td></tr>' % (comment['name'], comment['body'])
            out += tr

        return out

        



def retrieve_image(request):
    try:
        img = image.get_image(int(request.form['num']))
    except:
        img = image.get_latest_image()

    return img


def retrieve_style(request):
    return style.get_style(0)





