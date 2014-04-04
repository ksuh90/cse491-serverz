import quixote
from quixote.directory import Directory, export, subdir

from . import html, image

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



    @export(name='image_raw')
    def image_raw(self):

        response = quixote.get_response()
        request = quixote.get_request()

        img = retrieve_image(request)

        filename = img.filename
        if filename.lower() in ('jpg', 'jpeg'):
            response.set_content_type('image/jpeg')
        elif filename.lower() in ('tif',' tiff'):
            response.set_content_type('image/tiff')
        else:
            response.set_content_type('image/png')
        return img.data


    @export(name='list_of_images')
    def list_of_images(self):
        return html.render('list_of_images.html')



    @export(name='image_count')
    def image_count(self):
        return len(image.images)



def retrieve_image(request):
    try:
        img = image.get_image(int(request.form['num']))
    except:
        img = image.get_latest_image()

    return img