# image handling API
import sqlite3
import sys


class Image:
    filename = ''
    data = ''
    comments = []
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data
        self.comments = []




images = {}

def add_image(filename, data):
    # if images:
    #     image_num = max(images.keys()) + 1
    # else:
    #     image_num = 0

   
    # image = Image(filename, data)
    # images[image_num] = image
    # return image_num
    insert_image(filename, data)


def get_image(num):
    # return images[num]
    return retrieve_image(num)



def get_latest_image():
    # image_num = max(images.keys())
    # return images[image_num]
    return retrieve_image(-1)


def insert_image(filename, data):
    # connect to the already existing database
    db = sqlite3.connect('images.sqlite')

    # configure to allow binary insertions
    db.text_factory = bytes

    # insert!
    db.execute('INSERT INTO image_store (filename, image) \
        VALUES (?,?)', (filename, data))
    db.commit()



def retrieve_image(i):
    # connect to database
    db = sqlite3.connect('images.sqlite')
    
    # configure to retrieve bytes, not text
    db.text_factory = bytes

    # get a query handle (or "cursor")
    c = db.cursor()

    # select all of the images
    if i >= 0:
        c.execute('SELECT i, filename, image FROM image_store where i=(?)', (i,))
        print '---> getting ' + i
    else:
        c.execute('SELECT i, filename, image FROM image_store ORDER BY i DESC LIMIT 1')
        print '---> getting latest'

    # grab the first result (this will fail if no results!)
    try:
        i, filename, image = c.fetchone()
        return Image(filename, image)
    except:
        pass



def get_num_images():
    db = sqlite3.connect('images.sqlite')
    c = db.cursor()
    c.execute('SELECT i FROM image_store ORDER BY i DESC LIMIT 1')
    try:
        return int(c.fetchone()[0])
    except:
        return 0