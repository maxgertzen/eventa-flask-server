import os


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in os.environ.get("ALLOWED_EXTENSIONS")
