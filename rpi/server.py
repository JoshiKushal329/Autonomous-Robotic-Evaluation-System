"""
Web server for Raspberry Pi Answer Sheet Checker
Provides REST API and web UI for grading
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict

from pipeline import RPiPipeline


# Initialize Flask app
app = Flask(__name__, 
            template_folder=str(Path(__file__).parent / "templates"),
            static_folder=str(Path(__file__).parent / "static"))

# Configuration
UPLOAD_FOLDER = Path(__file__).parent / "uploads"
RESULTS_FOLDER = Path(__file__).parent / "results"
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp', 'tiff'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create folders
UPLOAD_FOLDER.mkdir(exist_ok=True)
RESULTS_FOLDER.mkdir(exist_ok=True)

# Initialize pipeline
pipeline = RPiPipeline()

# Session storage
sessions = {}


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/upload', methods=['POST'])
def upload_image():
    """Upload image for grading"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename}"
        filepath = UPLOAD_FOLDER / filename
        
        file.save(str(filepath))
        
        return jsonify({
            "success": True,
            "filename": filename,
            "path": str(filepath)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/grade', methods=['POST'])
def grade():
    """Grade answer sheet"""
    try:
        data = request.json
        
        if not data or 'image_path' not in data or 'answer_key' not in data:
            return jsonify({"error": "Missing image_path or answer_key"}), 400
        
        image_path = data['image_path']
        answer_key = data['answer_key']
        
        if not isinstance(answer_key, list):
            return jsonify({"error": "answer_key must be a list"}), 400
        
        # Validate file exists
        if not os.path.exists(image_path):
            return jsonify({"error": f"Image not found: {image_path}"}), 404
        
        # Run pipeline
        results = pipeline.full_pipeline(image_path, answer_key)
        
        # Save results
        result_filename = f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        result_path = RESULTS_FOLDER / result_filename
        
        with open(result_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        return jsonify({
            "success": True,
            "results": results,
            "result_file": result_filename
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/results/<filename>', methods=['GET'])
def get_result(filename: str):
    """Retrieve grading results"""
    try:
        result_path = RESULTS_FOLDER / secure_filename(filename)
        
        if not result_path.exists():
            return jsonify({"error": "Result not found"}), 404
        
        with open(result_path, 'r') as f:
            results = json.load(f)
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/results', methods=['GET'])
def list_results():
    """List all grading results"""
    try:
        results = []
        
        for file in sorted(RESULTS_FOLDER.glob("*.json"), reverse=True):
            with open(file, 'r') as f:
                data = json.load(f)
            
            results.append({
                "filename": file.name,
                "timestamp": file.stat().st_mtime,
                "summary": data.get("summary", {})
            })
        
        return jsonify({
            "success": True,
            "results": results
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/images', methods=['GET'])
def list_images():
    """List uploaded images"""
    try:
        images = []
        
        for file in sorted(UPLOAD_FOLDER.glob("*"), reverse=True):
            if allowed_file(file.name):
                images.append({
                    "filename": file.name,
                    "timestamp": file.stat().st_mtime,
                    "size": file.stat().st_size
                })
        
        return jsonify({
            "success": True,
            "images": images
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/image/<filename>', methods=['GET'])
def download_image(filename: str):
    """Download uploaded image"""
    try:
        image_path = UPLOAD_FOLDER / secure_filename(filename)
        
        if not image_path.exists():
            return jsonify({"error": "Image not found"}), 404
        
        return send_file(str(image_path), as_attachment=True)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/version', methods=['GET'])
def version():
    """Get version info"""
    return jsonify({
        "app": "RPi Answer Sheet Checker",
        "version": "1.0.0",
        "python_version": "3.9+",
        "platform": "Raspberry Pi 4/5"
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    print("🌐 Starting RPi Answer Sheet Checker Web Server")
    print("📍 Address: http://localhost:5000")
    print("📱 Access from other devices: http://<rpi_ip>:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
