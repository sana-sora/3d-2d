from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from datetime import datetime
from models.segmentation import segment_image
from models.mesh_generator import generate_mesh
from models.pattern import generate_pattern
from utils.pdf_generator import create_pattern_pdf
import traceback

app = Flask(__name__)
CORS(app)

# 設定
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health():
    """ヘルスチェック"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()}), 200

@app.route('/api/upload', methods=['POST'])
def upload_image():
    """画像をアップロード"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'ファイルが見つかりません'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'ファイルが選択されていません'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': '対応していないファイル形式です。PNG, JPG, GIFなどを使用してください'}), 400
        
        # ファイルを保存
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': filepath,
            'message': '画像がアップロードされました'
        }), 200
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/segment', methods=['POST'])
def segment():
    """セグメンテーション実行"""
    try:
        data = request.get_json()
        filename = data.get('filename')
        
        if not filename:
            return jsonify({'error': 'ファイル名が必要です'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'ファイルが見つかりません'}), 404
        
        # セグメンテーション実行
        mask_path = segment_image(filepath, app.config['RESULTS_FOLDER'])
        
        return jsonify({
            'success': True,
            'mask_filename': os.path.basename(mask_path),
            'message': 'セグメンテーションが完了しました'
        }), 200
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-mesh', methods=['POST'])
def generate_3d_mesh():
    """3Dメッシュ生成"""
    try:
        data = request.get_json()
        mask_filename = data.get('mask_filename')
        
        if not mask_filename:
            return jsonify({'error': 'マスクファイル名が必要です'}), 400
        
        mask_path = os.path.join(app.config['RESULTS_FOLDER'], mask_filename)
        
        if not os.path.exists(mask_path):
            return jsonify({'error': 'マスクファイルが見つかりません'}), 404
        
        # メッシュ生成
        mesh_path = generate_mesh(mask_path, app.config['RESULTS_FOLDER'])
        
        return jsonify({
            'success': True,
            'mesh_filename': os.path.basename(mesh_path),
            'message': '3Dメッシュが生成されました'
        }), 200
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-pattern', methods=['POST'])
def generate_2d_pattern():
    """2D型紙生成"""
    try:
        data = request.get_json()
        mesh_filename = data.get('mesh_filename')
        
        if not mesh_filename:
            return jsonify({'error': 'メッシュファイル名が必要です'}), 400
        
        mesh_path = os.path.join(app.config['RESULTS_FOLDER'], mesh_filename)
        
        if not os.path.exists(mesh_path):
            return jsonify({'error': 'メッシュファイルが見つかりません'}), 404
        
        # 型紙生成
        pattern_path = generate_pattern(mesh_path, app.config['RESULTS_FOLDER'])
        
        return jsonify({
            'success': True,
            'pattern_filename': os.path.basename(pattern_path),
            'message': '2D型紙が生成されました'
        }), 200
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    """PDF型紙生成"""
    try:
        data = request.get_json()
        pattern_filename = data.get('pattern_filename')
        
        if not pattern_filename:
            return jsonify({'error': 'パターンファイル名が必要です'}), 400
        
        pattern_path = os.path.join(app.config['RESULTS_FOLDER'], pattern_filename)
        
        if not os.path.exists(pattern_path):
            return jsonify({'error': 'パターンファイルが見つかりません'}), 404
        
        # PDF生成
        pdf_path = create_pattern_pdf(pattern_path, app.config['RESULTS_FOLDER'])
        
        return jsonify({
            'success': True,
            'pdf_filename': os.path.basename(pdf_path),
            'message': 'PDF型紙が生成されました'
        }), 200
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """ファイルダウンロード"""
    try:
        filepath = os.path.join(app.config['RESULTS_FOLDER'], filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'ファイルが見つかりません'}), 404
        
        return send_file(filepath, as_attachment=True)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
