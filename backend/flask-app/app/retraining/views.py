import os
import shutil
import zipfile
from flask import jsonify, request, Blueprint
from werkzeug.utils import secure_filename
from app.auth.decorators import api_key_required
from app.card.model import load_cards, retrieve_validated_cards
from app.image.model import load_images

retraining_bp = Blueprint('retraining', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'zip'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@retraining_bp.route('/', methods=['GET'])
@api_key_required
def retrieve_data():
    cards = retrieve_validated_cards()
    return jsonify(cards)


@retraining_bp.route('/', methods=['POST'])
@api_key_required
def receive_data():
    data = request.get_json()
    try:
        response, status_code = load_cards(data)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@retraining_bp.route('/images', methods=['POST'])
@api_key_required
def receive_images():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        zip_filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(zip_filepath)

        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            extract_folder = os.path.join(UPLOAD_FOLDER, filename.rsplit('.', 1)[0])
            os.makedirs(extract_folder, exist_ok=True)
            zip_ref.extractall(extract_folder)

        extracted_files = os.listdir(extract_folder)

        image_files = [f for f in extracted_files if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        load_images(image_files)
        shutil.rmtree(extract_folder)

        return jsonify({'message': 'Files extracted successfully', 'files': image_files}), 200

    return jsonify({'error': 'Invalid file type'}), 415
