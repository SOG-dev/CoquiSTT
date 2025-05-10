from flask import Flask, request, jsonify
import os
import subprocess
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400

    file = request.files['file']
    filename = f"{uuid.uuid4()}.wav"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    model = 'models/model.tflite'
    scorer = 'models/scorer.scorer'

    try:
        result = subprocess.check_output([
            'stt', '--model', model, '--scorer', scorer, '--audio', filepath
        ])
        os.remove(filepath)
        return jsonify({'text': result.decode('utf-8').strip()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
