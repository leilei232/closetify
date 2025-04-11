from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import uuid
from io import BytesIO


app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "static/uploads"
PROCESSED_FOLDER = "static/processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Serve the webpage
@app.route("/", methods=["GET"])
def index():
    return render_template("indextest.html")  # Ensure indextest.html is in the "templates" folder

@app.route('/upload', methods=['POST'])
def upload_file():
    
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No file part"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No selected file"}), 400

    # Generate unique filename
    filename = str(uuid.uuid4()) + ".png"
    upload_path = os.path.join(UPLOAD_FOLDER, filename)
    processed_path = os.path.join(PROCESSED_FOLDER, filename)

    # Save the uploaded image
    file.save(upload_path)

    # Open and remove background
    with Image.open(upload_path) as img:
        output = remove(img)
        output.save(processed_path, "PNG")  # Save as PNG to keep transparency

    return jsonify({"success": True, "image_url": "processed_image_url"})


if __name__ == '__main__':
    app.run(debug=True)
