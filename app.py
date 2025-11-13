import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='dist')
CORS(app)

UPLOADS_FOLDER = 'uploads'
if not os.path.exists(UPLOADS_FOLDER):
    os.makedirs(UPLOADS_FOLDER)

METADATA_FILE = os.path.join(UPLOADS_FOLDER, 'marksheets.json')
if not os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/save_marksheet', methods=['POST'])
def save_marksheet():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = file.filename
        file.save(os.path.join(UPLOADS_FOLDER, filename))
        
        class_name = request.form.get('class')
        faculty = request.form.get('faculty')
        section = request.form.get('section')
        
        with open(METADATA_FILE, 'r+') as f:
            metadata = json.load(f)
            metadata.append({
                'filename': filename,
                'class': class_name,
                'faculty': faculty,
                'section': section
            })
            f.seek(0)
            json.dump(metadata, f, indent=4)
            
        return jsonify({'message': 'File saved successfully'}), 200

@app.route('/api/get_marksheets', methods=['GET'])
def get_marksheets():
    with open(METADATA_FILE, 'r') as f:
        metadata = json.load(f)
    return jsonify(metadata)

@app.route('/api/get_marksheet/<filename>')
def get_marksheet(filename):
    return send_from_directory(UPLOADS_FOLDER, filename)

@app.route('/api/delete_marksheet/<filename>', methods=['DELETE'])
def delete_marksheet(filename):
    try:
        # Remove the file
        os.remove(os.path.join(UPLOADS_FOLDER, filename))
        
        # Remove the metadata
        with open(METADATA_FILE, 'r+') as f:
            metadata = json.load(f)
            metadata = [m for m in metadata if m['filename'] != filename]
            f.seek(0)
            f.truncate()
            json.dump(metadata, f, indent=4)
            
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/get_subjects', methods=['GET'])
def get_subjects():
    return send_from_directory('.', 'subjects_table.csv')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/healthz')
def health_check():
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)
