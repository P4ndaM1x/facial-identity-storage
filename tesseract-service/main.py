from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    if len(request.files) < 1:
        return "No file part", 400

    file = list(request.files.values())[0]

    if file:
        filename = 'temp_image.png'
        file.save(filename)

        output = subprocess.run(['tesseract', filename, 'stdout'], capture_output=True, text=True)
        os.remove(filename)
        return jsonify({'text': output.stdout.strip()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)