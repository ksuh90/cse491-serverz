class Style:
    filename = ''
    data = ''
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data

styles = {};

def add_style(filename, data):
    if styles:
        style_num = max(styles.keys()) + 1
    else:
        style_num = 0
        
    # images[image_num] = data
    # return image_num
    style = Style(filename, data)
    styles[style_num] = style
    return style_num

def get_style(num):
    return styles[num]


