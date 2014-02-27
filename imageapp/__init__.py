# __init__.py is the top level file in a Python package.

from quixote.publish import Publisher

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image

def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 
def setup():                            # stuff that should be run once.
    html.init_templates()

    image_dice = open('imageapp/dice.png', 'rb').read()
    image.add_image(image_dice)

    image_tux = open('imageapp/tux.png', 'rb').read()
    image.add_image(image_tux)

    

def teardown():                         # stuff that should be run once.
    pass