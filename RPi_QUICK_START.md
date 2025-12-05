# 🍓 RPi Quick Start Guide

Get Answer Sheet Checker running on Raspberry Pi in 15 minutes!

## 📋 Prerequisites

- Raspberry Pi 4 or 5 (4GB+ RAM recommended)
- MicroSD card (16GB+, Class 10+)
- Power supply (5V/3A+)
- Optional: USB camera or Raspberry Pi Camera v2
- Optional: Network connection (for remote access)

## ⚡ 5-Minute Setup

### Step 1: Clone Repository
```bash
cd ~
git clone https://github.com/JoshiKushal329/Autonomous-Robotic-Evaluation-System.git
cd Autonomous-Robotic-Evaluation-System
```

### Step 2: Run Setup
```bash
cd rpi
chmod +x setup.sh
./setup.sh
```

This will:
- Create virtual environment
- Install all dependencies
- Create necessary directories
- Verify camera (if available)

### Step 3: Start Server
```bash
source ../rpi_env/bin/activate
python3 server.py
```

Output should show:
```
🌐 Starting RPi Answer Sheet Checker Web Server
📍 Address: http://localhost:5000
📱 Access from other devices: http://<rpi_ip>:5000
```

### Step 4: Open in Browser
- **Local access:** http://localhost:5000
- **Remote access:** http://<your-rpi-ip>:5000

## 🎯 First Use

1. **Upload Image**
   - Click upload area
   - Select answer sheet image
   - Wait for confirmation

2. **Enter Answer Key**
   - Type expected answers
   - Click "+ Add Question" for more
   - Or load from file

3. **Grade**
   - Click "🚀 Grade Answer Sheet"
   - Wait 3-5 seconds
   - View results

## 💻 Command-Line Alternative

If you prefer terminal:

```bash
# Grade from image file
python3 cli.py --image answer.jpg --answers "Answer 1" "Answer 2" "Answer 3"

# Capture from camera and grade
python3 cli.py --camera 0 --preview 5 --answers "Q1" "Q2" "Q3"

# Load answers from JSON file
python3 cli.py --image answer.jpg --answer-file example_answers.json

# See all options
python3 cli.py --help
```

## 📸 Using Camera

### List Available Cameras
```bash
python3 cli.py --list-cameras
```

### Capture and Grade
```bash
python3 cli.py --camera 0 --preview 3 --answers "Q1" "Q2" "Q3"
```

Flags:
- `--camera 0` - Use camera device 0
- `--preview 3` - Show 3-second preview before capture
- `--answers ...` - Your answer key

## 📁 Where Are My Files?

After grading:
- **Uploaded images:** `rpi/uploads/`
- **Results JSON:** `rpi/results/`
- **Web accessible:** Via "History" tab in UI

## 🔧 Common Tasks

### Change Grading Threshold
```bash
# In web UI: Use slider in "Settings"
# In CLI: --threshold 0.75
# In code: RPiPipeline(threshold=0.75)
```

### Load Answer Key from File

Create `answers.json`:
```json
[
  "Answer to question 1",
  "Answer to question 2",
  "Answer to question 3"
]
```

Use it:
```bash
python3 cli.py --image answer.jpg --answer-file answers.json
```

### Save Results
```bash
python3 cli.py --image answer.jpg --answers "Q1" --output results.json
```

### Process Multiple Images
```bash
for img in images/*.jpg; do
  python3 cli.py --image "$img" --answer-file answers.json
done
```

## 🐛 Troubleshooting

### Can't connect to web UI
```bash
# Check if server is running
ps aux | grep server.py

# Verify port is available
sudo netstat -tulpn | grep 5000

# Try localhost first
curl http://localhost:5000/api/health
```

### Out of memory
```bash
# Reduce image size
convert big_image.jpg -resize 1280x960 small_image.jpg

# Or increase swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Camera not detected
```bash
# Verify camera is connected
vcgencmd get_camera

# Enable if needed
sudo raspi-config
# Interface Options → Camera → Enable
```

### Slow processing
- Reduce image size
- Close other applications
- Check CPU temp: `vcgencmd measure_temp`
- Add cooling fan if needed

## 📊 What to Expect

**Performance:** 2-4 seconds per image (includes OCR)

**Accuracy:** 85-95% on clear handwriting (depends on quality)

**Memory:** 500MB-2GB depending on image size

**CPU:** 60-100% during processing

## 🎓 Learning More

- **Full docs:** See `rpi/README.md`
- **API reference:** Check `rpi/README.md` → API Reference section
- **Code examples:** Look in `rpi/` directory
- **Troubleshooting:** `rpi/README.md` → Troubleshooting section

## 🚀 What's Next?

1. ✅ **Basic grading** - Done!
2. 🎯 **Batch processing** - Process multiple sheets
3. 🔗 **API integration** - Integrate with other systems
4. 📊 **Data analysis** - Track grading trends
5. 🌍 **Cloud sync** - Backup results online
6. 📱 **Mobile app** - Grade from phone

## 💡 Pro Tips

1. **Better OCR accuracy:**
   - Use high-quality images (at least 300 DPI)
   - Ensure good lighting
   - Black pen on white paper works best

2. **Faster processing:**
   - Use smaller images (1280×960 max)
   - Reduce number of answers
   - Close background apps

3. **Better grading:**
   - Increase threshold for strict grading (0.85-0.95)
   - Decrease for lenient grading (0.50-0.65)
   - Use meaningful word filtering (default enabled)

4. **Batch workflows:**
   - Create script to process multiple images
   - Save results to JSON for analysis
   - Run overnight for large batches

## 📞 Need Help?

1. Check `rpi/README.md` for detailed docs
2. Review error messages (very descriptive!)
3. Check Python logs for debugging
4. Visit GitHub issues for known problems

## ✨ Features You Now Have

✅ Live camera capture and grading  
✅ Web interface from any device  
✅ REST API for automation  
✅ Command-line tools  
✅ Batch processing  
✅ Results history  
✅ Customizable thresholds  
✅ Multi-format support (JPG, PNG, BMP)  
✅ Offline operation (no internet needed)  
✅ Mobile-responsive design  

---

**You're all set!** Start grading! 📚✅
