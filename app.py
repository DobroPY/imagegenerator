
from flask import Flask, request, jsonify
from image_generator import generate_advertisement_collage
import base64
from io import BytesIO

app = Flask(__name__)


@app.route('/')
def home():
    return app.send_static_file('index.html')


@app.route('/generate-collage', methods=['POST'])
def generate_collage():
    data = request.json
    base_prompt = data['base_prompt']
    scenes = int(data['scenes'])  # Convert 'scenes' from string to integer
    collage = generate_advertisement_collage(base_prompt, scenes)

    if collage:
        buffered = BytesIO()
        collage.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return jsonify({'image': img_str})
    else:
        return jsonify({'error': 'Could not generate collage'}), 500

if __name__ == '__main__':
    app.run(debug=True)