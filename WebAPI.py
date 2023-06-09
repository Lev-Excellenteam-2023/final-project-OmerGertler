import datetime
import os
import uuid

from flask import Flask, render_template, request, jsonify, abort, json

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
uploaded_files = {}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    file = request.files['file']
    uid = str(uuid.uuid4())
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    original_filename = file.filename
    new_filename = f"{uid}_{timestamp}_{original_filename}"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
    uploaded_files[uid] = {'status': 'pending', 'explanation': None}
    response = {'uid': uid, 'message': 'File uploaded successfully!'}
    return jsonify(response)


@app.route('/status/<uid>', methods=['GET'])
def check_status(uid):
    if uid in uploaded_files:
        file_info = uploaded_files[uid]
        status = file_info['status']
        explanation = file_info['explanation']
        if status == 'pending':
            filename = None
            timestamp = None
            output = None
        else:
            # Extract the original filename and timestamp from the new filename
            filename, timestamp, _ = file_info['new_filename'].rsplit('_', 2)
            output_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}_{timestamp}_{uid}_output.json")
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    output = json.load(f)
            else:
                output = None

        response = {
            'status': status,
            'filename': filename,
            'timestamp': timestamp,
            'explanation': explanation,
            'output': output
        }
    else:
        abort(404)  # Return a 404 NOT FOUND response if the UID is not found

    return jsonify(response)


if __name__ == '__main__':
    app.run()
