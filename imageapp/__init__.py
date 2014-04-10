# __init__.py is the top level file in a Python package.
import os
import sqlite3

from quixote.publish import Publisher

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image, style

IMAGE_DB_FILE = 'images.sqlite'


def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 

def setup():                            # stuff that should be run once.
    html.init_templates()

    style_data = open('imageapp/style/style.css', 'rb').read()
    style.add_style('imageapp/style/style.css', style_data)

    if not os.path.exists(IMAGE_DB_FILE):
        create_database()

    insert_dice()


    # img_data = open('imageapp/tux.png', 'rb').read()
    # image.add_image('imageapp/tux.png', img_data)



def teardown():                         # stuff that should be run once.
    pass



def create_database():
    print 'creating database'
    db = sqlite3.connect('images.sqlite')
    db.execute('CREATE TABLE image_store (i INTEGER PRIMARY KEY, filename VARCHAR(255), image BLOB)');
    db.commit()
    db.close()





def retrieve_all_images():
    # connect to database
    db = sqlite3.connect('images.sqlite')
    
    # configure to retrieve bytes, not text
    db.text_factory = bytes

    # get a query handle (or "cursor")
    c = db.cursor()

    # select all of the images
    for row in c.execute('SELECT * FROM image_store ORDER BY i DESC'):
        open(row[1], 'w').write(row[2])




def insert_dice():
    # connect to the already existing database
    db = sqlite3.connect('images.sqlite')

    # configure to allow binary insertions
    db.text_factory = bytes

    # grab whatever it is you want to put in the database
    r = open('imageapp/dice.png', 'rb').read()

    # insert!
    db.execute('INSERT INTO image_store (filename,image) VALUES (?, ?)', ('dice.png',r))
    db.commit()


