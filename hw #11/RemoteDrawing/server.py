from cv2 import IMREAD_COLOR, imdecode
from flask import Flask, Response, render_template, request
from jsonpickle import encode
from numpy import fromstring, uint8
from PIL import Image


app = Flask(__name__)


@app.route('/')
def show_canvas():
    return render_template('home.html', user_image='canvas.jpg')


@app.route('/', methods=['POST'])
def get_canvas():
    image = fromstring(request.data, uint8)
    image = imdecode(image, IMREAD_COLOR)

    response = {
        'message': f'image received. size={image.shape[1]}x{image.shape[0]}'
    }
    response_pickled = encode(response)

    image = Image.fromarray(image.astype('uint8'), 'RGB')
    image.save_canvas('static/images/canvas.jpg')

    return Response(
        response=response_pickled,
        status=200,
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
