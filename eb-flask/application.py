import os
from flask import Flask, request, jsonify, render_template
import numpy as np
import keras
from keras.preprocessing import image
from keras import backend as K

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = 'uploads'

model = None
graph = None


def load_model():
    global model
    global graph
    model = keras.models.load_model('static/models/sklesion_img.h5')
    graph = K.get_session().graph


dx = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']


def predict(image_path):
    K.clear_session()
    model = keras.models.load_model('static/models/sklesion_img.h5')
    print()
    image_size = (200, 200)
    img = image.load_img(image_path, target_size=image_size)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    predictions = list(model.predict(x)[0])

    return predictions


@application.route('/', methods=['GET', 'POST'])
def upload_file():

    data = {"success": False}

    if request.method == 'POST':
        print(request)

        if request.files.get('file'):
            file = request.files['file']

            filename = file.filename

            filepath = os.path.join(application.config['UPLOAD_FOLDER'], filename)

            file.save(filepath)

            image_size = (200, 200)
            predictions = predict(filepath)

            return jsonify([int(p) for p in predictions])
    #return '''
    #<!doctype html>
    #<title>Upload new File</title>
    #<h1>Upload new File</h1>
    #<form method=post enctype=multipart/form-data>
      #<p><input type=file name=file>
         #<input type=submit value=Upload>
    #</form>
    #'''

    return render_template("home.html")


if __name__ == '__main__':
    application.run(debug=True)