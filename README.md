# Dockerized Face Recognition

This Dockerfile sets up an environment for running face recognition using Python 3.10.3 with some necessary dependencies. It installs Dlib, OpenCV, Flask, and other required packages for face recognition.

To start the container use

```bash
    docker/podman -d -p 5000:5000 <yourImage>
```

# Face Recognition API

This is a simple Flask-based API for face recognition. It exposes two endpoints: `/get_encodings` for generating face encodings from an image and `/test` to check if the server is running.

Use any tool (e.g., curl or Postman) to POST an image to
`http://127.0.0.1:5000/get_encodings`.  
 Here's an example using curl:

```bash
curl -X POST -F "file=@path_to_your_image.jpg" http://127.0.0.1:5000/get_encodings

```
