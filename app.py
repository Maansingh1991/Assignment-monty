from flask import Flask, request, jsonify
from routes.uploading_service import uploading_service_blueprint

app = Flask(__name__)
app.register_blueprint(uploading_service_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
