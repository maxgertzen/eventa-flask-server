import os


def allowed_file(filename):
    print('inside allowed_file')
    print(filename)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
