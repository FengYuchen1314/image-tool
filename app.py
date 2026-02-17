import os
import uuid
import zipfile
import io
import time
from datetime import datetime
from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

SUPPORTED_FORMATS = {
    'JPEG': ['jpg', 'jpeg'],
    'PNG': ['png'],
    'WEBP': ['webp'],
    'BMP': ['bmp'],
    'GIF': ['gif'],
    'TIFF': ['tiff', 'tif']
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400

    files = request.files.getlist('image')
    if not files or len(files) == 0:
        return jsonify({'error': '未选择文件'}), 400

    uploaded_images = []
    errors = []

    for file in files:
        if file.filename == '':
            continue

        ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
        if ext not in [fmt.lower() for formats in SUPPORTED_FORMATS.values() for fmt in formats]:
            errors.append(f'{file.filename}: 不支持的格式')
            continue

        filename = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            img = Image.open(filepath)
            width, height = img.size
            file_size = os.path.getsize(filepath)

            uploaded_images.append({
                'success': True,
                'filename': filename,
                'original_name': file.filename,
                'width': width,
                'height': height,
                'format': img.format,
                'file_size': file_size
            })
        except Exception as e:
            errors.append(f'{file.filename}: 处理失败')

    if not uploaded_images and errors:
        return jsonify({'error': '; '.join(errors)}), 400

    return jsonify({
        'success': True,
        'images': uploaded_images,
        'errors': errors
    })


@app.route('/api/convert', methods=['POST'])
def convert_format():
    data = request.json
    files_data = data.get('files', [])
    target_format = data.get('format', 'JPEG').upper()
    quality = data.get('quality', 85)
    naming_method = data.get('naming_method', 'original')
    file_index = data.get('file_index', 0)
    total_files = data.get('total_files', 1)

    if not files_data:
        return jsonify({'error': '缺少文件名'}), 400

    if target_format != 'KEEP' and target_format not in SUPPORTED_FORMATS:
        return jsonify({'error': '不支持的目标格式'}), 400

    if not 1 <= quality <= 100:
        return jsonify({'error': '质量值必须在1-100之间'}), 400

    def generate_filename(index, original_name, fmt):
        ext = fmt.lower() if fmt else original_name.rsplit('.', 1)[-1] if '.' in original_name else 'jpg'
        
        if naming_method == 'original':
            base_name = original_name.rsplit('.', 1)[0] if '.' in original_name else original_name
            return f"{base_name}.{ext}"
        elif naming_method == 'timestamp':
            ts = int(time.time() * 1000)
            return f"{ts}.{ext}"
        elif naming_method == 'number':
            return f"img_{index + 1:03d}.{ext}"
        elif naming_method == 'uuid':
            return f"{uuid.uuid4()}.{ext}"
        else:
            return f"{uuid.uuid4()}.{ext}"

    converted_files = []
    errors = []

    for idx, file_info in enumerate(files_data):
        filename = file_info.get('filename')
        original_name = file_info.get('original_name', filename)
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            errors.append(f'{filename}: 文件不存在')
            continue

        try:
            img = Image.open(filepath)
            original_size = os.path.getsize(filepath)

            if target_format == 'KEEP':
                new_format = img.format
            else:
                if target_format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                new_format = target_format

            new_filename = generate_filename(file_index, original_name, new_format)
            new_filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

            save_kwargs = {'quality': quality, 'optimize': True}
            if new_format == 'PNG':
                save_kwargs = {'optimize': True, 'compress_level': 9}
            
            img.save(new_filepath, **save_kwargs)
            
            new_size = os.path.getsize(new_filepath)
            compression_ratio = round((1 - new_size / original_size) * 100, 2) if original_size > 0 else 0

            converted_files.append({
                'filename': new_filename,
                'original_name': new_filename,
                'format': new_format,
                'file_size': new_size,
                'original_size': original_size,
                'compression_ratio': compression_ratio
            })
        except Exception as e:
            errors.append(f'{filename}: 处理失败')

    return jsonify({
        'success': True,
        'files': converted_files,
        'errors': errors
    })


@app.route('/api/compress', methods=['POST'])
def compress_image():
    data = request.json
    filenames = data.get('filenames', [])
    quality = data.get('quality', 75)

    if not filenames:
        return jsonify({'error': '缺少文件名'}), 400

    if not 1 <= quality <= 100:
        return jsonify({'error': '质量值必须在1-100之间'}), 400

    compressed_files = []
    errors = []

    for filename in filenames:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            errors.append(f'{filename}: 文件不存在')
            continue

        try:
            img = Image.open(filepath)
            original_format = img.format
            original_size = os.path.getsize(filepath)

            if original_format == 'JPEG':
                img.save(filepath, quality=quality, optimize=True)
            elif original_format == 'PNG':
                img.save(filepath, optimize=True, compress_level=9)
            else:
                ext = filename.rsplit('.', 1)[-1] if '.' in filename else 'jpg'
                new_filename = f"compressed_{uuid.uuid4()}.{ext}"
                new_filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                img.save(new_filepath, quality=quality, optimize=True)
                filename = new_filename
                filepath = new_filepath

            new_size = os.path.getsize(filepath)
            compression_ratio = round((1 - new_size / original_size) * 100, 2) if original_size > 0 else 0

            compressed_files.append({
                'filename': filename,
                'original_name': filename,
                'original_size': original_size,
                'new_size': new_size,
                'compression_ratio': compression_ratio
            })
        except Exception as e:
            errors.append(f'{filename}: 压缩失败')

    return jsonify({
        'success': True,
        'files': compressed_files,
        'errors': errors
    })


@app.route('/api/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({'error': '文件不存在'}), 404
    return send_file(filepath, as_attachment=True)


@app.route('/api/download-batch', methods=['POST'])
def download_batch():
    data = request.json
    filenames = data.get('filenames', [])

    if not filenames:
        return jsonify({'error': '没有文件'}), 400

    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename in filenames:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(filepath):
                zf.write(filepath, filename)

    memory_file.seek(0)
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='processed_images.zip'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=30050, debug=True)
