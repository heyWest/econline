import os
import secrets
from PIL import Image
from econline import app


def save_picture(candidate_name,form_picture):
    random_hex = secrets.token_hex(3)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = candidate_name + random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/candidate_pictures', picture_fn)
    form_picture.save(picture_path)
    
    output_size = (500, 500) #minimizing the size of the image so it isn't saved so large in the database
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn