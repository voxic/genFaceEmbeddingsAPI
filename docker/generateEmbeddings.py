from flask import Flask, request, jsonify
import face_recognition
import cv2
import numpy as np

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    print("Server running on port 5000")
