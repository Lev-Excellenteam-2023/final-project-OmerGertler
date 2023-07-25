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


def format_file_content(file_content):
    # Remove square brackets '[' and ']' from the string
    file_content = file_content.strip('[]')

    # Remove curly braces '{' and '}' from the string
    file_content = file_content.replace('{', '').replace('}', '')

    # Split the string into individual key-value pairs
    pairs = file_content.split(', ')

    # Format each key-value pair by moving to the next line after every '.'
    formatted_pairs = []
    for pair in pairs:
        if ': ' in pair:
            key, value = pair.split(': ', 1)
            formatted_value = value.replace('.', '.\n')
            formatted_pair = f"{key}: {formatted_value}"
            formatted_pairs.append(formatted_pair)

    # Join the formatted key-value pairs with a line break
    formatted_content = '\n'.join(formatted_pairs)

    return formatted_content


@app.route('/status/<uid>', methods=['GET'])
def check_status(uid):
    folder_path = os.path.join(os.getcwd(), 'outputs')
    matched_uids = [
        filename for filename in os.listdir(folder_path)
        if uid in filename and uid in filename.split('_', 1)[0]
    ]

    if matched_uids:
        matched_filename = matched_uids[0]

        # Extract the slide number from the filename
        slide_number = matched_filename.split('_')[0]

        # Read the file content from the file
        file_path = os.path.join(folder_path, matched_filename)
        with open(file_path, 'r') as f:
            file_content = f.read()

        formatted_content = format_file_content(file_content)

        return render_template('status.html', number=slide_number, formatted_content=formatted_content)
    else:
        abort(404)


if __name__ == '__main__':
    app.run()
