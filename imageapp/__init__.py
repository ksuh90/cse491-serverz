# __init__.py is the top level file in a Python package.

from quixote.publish import Publisher

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image
#import os

def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 

def setup():                            # stuff that should be run once.
    html.init_templates()

    img_data = open('imageapp/tux.png', 'rb').read()
    image.add_image('imageapp/tux.png', img_data)
    # for file in os.listdir('imageapp'):
    #     if file.endswith(".png"):
    #         img_data = open('imageapp/'+file).read()
    #         image.add_image(img_data)
    

def teardown():                         # stuff that should be run once.
    pass