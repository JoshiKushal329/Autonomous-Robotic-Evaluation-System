# 🍓 Raspberry Pi Answer Sheet Checker

Complete implementation of Answer Sheet Checker for Raspberry Pi 4 and 5 with camera support, web UI, and CLI.

## 📋 Table of Contents

- [Overview](#overview)
- [Hardware Requirements](#hardware-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This RPi implementation includes:

- **Camera Capture**: Support for PiCamera and USB cameras
- **Web UI**: Browser-based interface for image upload and grading
- **REST API**: Complete API for integration with other systems
- **CLI**: Command-line tool for automation and scripting
- **Optimized Pipeline**: Memory-efficient processing on RPi
- **Local Processing**: No cloud dependency, all processing on device

### What's Included

```
rpi/
├── __init__.py              # Package initialization
├── camera.py                # Camera capture module
├── pipeline.py              # Optimized grading pipeline
├── server.py                # Flask web server
├── cli.py                   # Command-line interface
├── requirements.txt         # Python dependencies
├── templates/
│   └── index.html          # Web UI
└── static/
    ├── style.css           # Styling
    └── app.js              # Frontend logic
```

## 🛠️ Hardware Requirements

### Minimum
- Raspberry Pi 4 (2GB RAM minimum, 4GB recommended)
- MicroSD card (16GB recommended, Class 10+)
- 5V/3A power supply
- Optional: Raspberry Pi Camera v2 or USB webcam

### Recommended
- Raspberry Pi 4 with 8GB RAM
- MicroSD card (32GB, Class 10+)
- Cooling fan or case with heatsink
- Optional: Raspberry Pi Camera v2 with wide-angle lens

## 💻 Installation

### 1. Install Raspberry Pi OS

```bash
# Use Raspberry Pi Imager to install latest Raspberry Pi OS
# Ensure camera interface is enabled in raspi-config
sudo raspi-config
# Enable Camera (Interface Options → Camera)
```

### 2. Clone Repository

```bash
cd ~
git clone https://github.com/JoshiKushal329/Autonomous-Robotic-Evaluation-System.git
cd Autonomous-Robotic-Evaluation-System
```

### 3. Create Virtual Environment

```bash
python3 -m venv rpi_env
source rpi_env/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### 4. Install Dependencies

```bash
cd rpi
pip install -r requirements.txt

# If picamera2 installation fails (not available in all environments):
pip install -r requirements.txt --ignore-installed picamera2
```

### 5. Verify Installation

```bash
python3 -c "import torch; import cv2; import flask; print('✓ All dependencies installed')"
```

## 🚀 Usage

### Option 1: Web Interface (Recommended)

```bash
# Activate virtual environment
source rpi_env/bin/activate

# Start web server
cd rpi
python3 server.py
```

Access the web UI:
- Local: http://localhost:5000
- Remote: http://<rpi_ip>:5000

**Steps:**
1. Upload answer sheet image
2. Enter answer key
3. Adjust grading threshold if needed
4. Click "Grade Answer Sheet"
5. View results and history

### Option 2: Command-Line Interface

```bash
# Basic usage with image
python3 cli.py --image answer.jpg --answers "Question 1" "Question 2" "Question 3"

# With camera capture
python3 cli.py --camera 0 --answers "Q1" "Q2" "Q3"

# With camera preview (5 seconds)
python3 cli.py --camera 0 --preview 5 --answers "Q1" "Q2" "Q3"

# Load answers from JSON file
python3 cli.py --image answer.jpg --answer-file answers.json

# Save results to file
python3 cli.py --image answer.jpg --answers "Q1" "Q2" --output results.json

# List available cameras
python3 cli.py --list-cameras
```

### Option 3: Python API

```python
from rpi.pipeline import RPiPipeline

# Initialize pipeline
pipeline = RPiPipeline(threshold=0.70)

# Grade an image
results = pipeline.full_pipeline(
    image_path='answer.jpg',
    answer_key=['Answer 1', 'Answer 2', 'Answer 3'],
    save_output='results.json'
)

print(f"Score: {results['summary']['percentage']:.1f}%")
```

### Option 4: Camera Integration

```python
from rpi.camera import RPiCameraCapture

# Initialize camera
camera = RPiCameraCapture(camera_id=0, resolution=(1920, 1440))

# Show preview and capture
frame = camera.capture_preview(duration_sec=3)
camera.save_frame(frame, 'answer_sheet.jpg')

# Or capture burst
frames = camera.capture_burst(num_frames=5)

camera.release()
```

## 🔌 API Reference

Base URL: `http://<rpi_ip>:5000/api`

### Health Check

```
GET /api/health
```

Response:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2025-12-05T10:30:00"
}
```

### Upload Image

```
POST /api/upload
Content-Type: multipart/form-data

Files:
  image: <binary image data>
```

Response:
```json
{
  "success": true,
  "filename": "20251205_103000_answer.jpg",
  "path": "/home/pi/rpi/uploads/20251205_103000_answer.jpg"
}
```

### Grade Answers

```
POST /api/grade
Content-Type: application/json

{
  "image_path": "/path/to/image.jpg",
  "answer_key": ["Answer 1", "Answer 2", "Answer 3"],
  "threshold": 0.70
}
```

Response:
```json
{
  "success": true,
  "results": {
    "1": {
      "expected": "Answer 1",
      "student": "Answer 1",
      "similarity": 0.95,
      "status": "✓ PASS"
    },
    "summary": {
      "total_questions": 3,
      "passed": 3,
      "percentage": 100.0,
      "threshold": 0.70
    }
  }
}
```

### Get Results

```
GET /api/results/<filename>
```

### List Results

```
GET /api/results
```

### List Images

```
GET /api/images
```

### Download Image

```
GET /api/image/<filename>
```

## 📝 Configuration

### Environment Variables

Create `.env` file in `rpi/` directory:

```env
# Server
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False

# Processing
MAX_IMAGE_WIDTH=1280
MAX_IMAGE_HEIGHT=960
GRADING_THRESHOLD=0.70

# Model
OCR_MODEL=microsoft/trocr-base-handwritten
```

### Answer Key Format

**JSON File Format:**

```json
{
  "answers": [
    "Photosynthesis is the process...",
    "Mitochondria is the powerhouse...",
    "DNA contains genetic information..."
  ]
}
```

or simply:

```json
[
  "Answer 1",
  "Answer 2",
  "Answer 3"
]
```

## ⚙️ Performance Tips

### Optimize Image Size

Larger images take longer to process. Recommended:
- Max width: 1280 pixels
- Max height: 960 pixels

```bash
# Use ImageMagick to resize
convert input.jpg -resize 1280x960 output.jpg
```

### Reduce Memory Usage

If experiencing out-of-memory errors:

1. Use smaller images
2. Reduce answer key size
3. Increase swap space:

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Enable GPU Acceleration (Pi 4 only)

For Pi 4 with GPU support:

```bash
pip install --upgrade torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

## 🔧 Troubleshooting

### Camera Not Found

**Error:** `Camera 0 connection failed`

**Solutions:**
- Check camera is properly connected
- Enable camera in `raspi-config`
- Try: `python3 cli.py --list-cameras`
- Test: `vcgencmd get_camera`

### Out of Memory

**Error:** `torch.cuda.OutOfMemoryError` or system freeze

**Solutions:**
- Reduce image size
- Use smaller model
- Increase swap space (see Performance Tips)
- Close other applications

### ImportError for picamera2

**Error:** `ModuleNotFoundError: No module named 'picamera2'`

**Solutions:**
- picamera2 only works on Raspberry Pi OS bullseye+
- For other systems, use OpenCV camera capture (already set)
- The system will fall back to cv2 automatically

### Slow Processing

**Issue:** Grading takes > 10 seconds per image

**Solutions:**
- Reduce image size
- Check CPU temperature: `vcgencmd measure_temp`
- Enable cooling solution
- Reduce number of answers
- Use faster internet if downloading models

### Web UI Not Loading

**Issue:** Can't connect to web interface

**Solutions:**
```bash
# Check if server is running
ps aux | grep "python3 server.py"

# Check firewall
sudo ufw allow 5000/tcp

# Try localhost first
curl http://localhost:5000/api/health

# Check port usage
sudo netstat -tulpn | grep 5000
```

## 📊 Performance Benchmarks (RPi 4 with 4GB RAM)

| Task | Time |
|------|------|
| Image loading | 0.2s |
| Text extraction (5 lines) | 2-3s |
| Grading (5 questions) | 0.1s |
| **Total per image** | **2.5-3.5s** |

## 🎓 Learning Resources

- [PyTorch on RPi](https://pytorch.org/get-started/locally/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Raspberry Pi Docs](https://www.raspberrypi.com/documentation/)
- [OpenCV Tutorials](https://docs.opencv.org/master/)

## 📄 License

Same as main project

## 🤝 Contributing

Contributions welcome! Please follow the same patterns as main codebase.

## 📞 Support

For issues:
1. Check Troubleshooting section
2. Review logs: `journalctl -u answer-sheet-checker.service`
3. Create GitHub issue with:
   - RPi model (4/5, RAM size)
   - Error message
   - Steps to reproduce

---

**Happy Grading on Raspberry Pi!** 🍓📚
