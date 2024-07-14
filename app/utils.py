import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'json'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(uploaded_file):
    filename = secure_filename(uploaded_file.name)
    save_path = os.path.join('uploads', filename)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return filename
