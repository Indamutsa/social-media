import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def save_picture(form_picture):
    #We get our random srtring of 8 bits
    random_hex = secrets.token_hex(8)

    # This will split the file name from the extension
    _, f_ext = os.path.splitext(form_picture.filename)

    #We add the random text to the filename without extension, this will help us avoid duplicates
    picture_fn = random_hex + f_ext

    # We define the picture path, and rewrite the image by giving the picture_fn name
    picture_path = os.path.join(current_app.root_path, 'static', picture_fn)

    #Resizing the picture
    output_size = (125, 125)
    
    i =Image.open(form_picture)

    #This is where we exactly resize the pic
    i.thumbnail(output_size)

    # We save it 
    i.save(picture_path)

    #We return it
    return picture_fn



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])

    msg.body = f''' To reset your password, visit the following link:
              {url_for('reset_token', token=token, _external=True)}

               If you did not make this request, ignore this message.
    '''

    mail.send(msg)