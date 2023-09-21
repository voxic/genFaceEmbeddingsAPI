from flask import Flask, request, jsonify, send_file
import face_recognition
import cv2
import numpy as np
from zipfile import ZipFile
from io import BytesIO

app = Flask(__name__)

@app.route('/get_encodings', methods=['POST'])
def get_encodings():
    # Get image from POST request
    print("Got a Request")
    file = request.files['file']
    if not file:
        return jsonify({"error": "No file provided"}), 400

    npimg = np.fromstring(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    
    if img is None:
        return jsonify({"error": "Invalid image format"}), 400

    # Convert BGR image to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Get encodings
    encodings = face_recognition.face_encodings(img_rgb)
    
    if len(encodings) == 0:
        return jsonify({"error": "No faces found in the image"}), 400

    return jsonify({"encodings": encodings[0].tolist()}), 200

@app.route('/test', methods=['GET'])
def test():
    return "Server is running!"


@app.route('/get_face', methods=['POST'])
def get_face():
    file = request.files['file']
    if not file:
        return jsonify({"error": "No file provided"}), 400

    npimg = np.fromstring(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"error": "Invalid image format"}), 400

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(img_rgb)
    if not face_locations:
        return jsonify({"error": "No faces found in the image"}), 400

    # Create an in-memory zip file
    mem_zip = BytesIO()

    with ZipFile(mem_zip, 'w') as zipf:
        for idx, (top, right, bottom, left) in enumerate(face_locations):
            face_image = img[top:bottom, left:right]

            # Convert the face_image to bytes
            retval, buffer = cv2.imencode('.jpg', face_image)
            face_image_bytes = buffer.tobytes()

            # Write the image bytes to the zip file with a unique name for each face
            zipf.writestr(f'face_{idx + 1}.jpg', face_image_bytes)

    mem_zip.seek(0)

    return send_file(mem_zip, as_attachment=True, download_name='faces.zip', mimetype='application/zip')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    print("Server running on port 5000")
