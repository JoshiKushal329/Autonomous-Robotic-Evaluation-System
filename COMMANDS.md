# ⚡ Quick Command Reference

## 🚀 Installation (First Time)

```bash
# 1. Navigate to project
cd /path/to/AnswerSheetChecker

# 2. Create virtual environment
python3 -m venv test

# 3. Activate
source test/bin/activate  # Linux/Mac
# or
test\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify (should see ✓)
python -c "from src.ocr.text_extractor import TextExtractor; print('✓ Ready')"
```

---

## 🎯 Basic Usage

```bash
# 1. Activate environment
source test/bin/activate

# 2. Edit configuration
nano grade_image.py
# Change:
#   Line 12: image_path = 'your_image.jpg'
#   Lines 35-40: answer_key = [...]

# 3. Run grading
python grade_image.py

# 4. Review output (Q1-Q5 results with similarity %)
```

---

## 🔧 Configuration Commands

### Change Similarity Threshold (Strict Grading)
```bash
# Edit grade_image.py
# Change line 44 from:
#   matcher = SimilarityMatcher(answer_key, similarity_threshold=0.70)
# To (example - 90% required):
#   matcher = SimilarityMatcher(answer_key, similarity_threshold=0.90)
```

### Change Image Path
```bash
# Edit grade_image.py line 12:
image_path = 'my_answer_sheet.jpg'
```

### Modify Answer Key
```bash
# Edit grade_image.py lines 35-40:
answer_key = [
    "Your answer 1",
    "Your answer 2",
    "Your answer 3",
]
```

### Customize Stop Words
```bash
# Edit src/grading/similarity_matcher.py
# STOP_WORDS = {'a', 'an', ...}  # Add/remove words
```

---

## 🔄 Batch Processing

### Process All JPGs in Directory
```bash
#!/bin/bash
for img in *.jpg; do
    echo "Processing $img..."
    cp grade_image.py temp_grade.py
    sed -i "s/'unnamed.jpg'/'$img'/" temp_grade.py
    python temp_grade.py > "results_$img.txt"
    rm temp_grade.py
done
```

### Process with Custom Threshold
```bash
#!/bin/bash
for img in *.jpg; do
    python3 << PYTHON
import cv2
from src.ocr.text_extractor import TextExtractor
from src.grading.similarity_matcher import SimilarityMatcher

image = cv2.imread('$img')
extractor = TextExtractor()
lines = extractor.extract_text(image)

answers = ["Answer 1", "Answer 2", "Answer 3"]
matcher = SimilarityMatcher(answers, similarity_threshold=0.80)

for i, line in enumerate(lines[:len(answers)]):
    score = matcher.match(line)
    print(f"Q{i+1}: {score*100:.1f}% {'PASS' if score >= 0.80 else 'FAIL'}")
PYTHON
done
```

---

## 🛠️ Maintenance Commands

### Reinstall Everything (Clean Slate)
```bash
# Deactivate if active
deactivate

# Remove old venv
rm -rf test

# Create new
python3 -m venv test
source test/bin/activate
pip install -r requirements.txt
```

### Clear Cached Models
```bash
# Remove HuggingFace cache
rm -rf ~/.cache/huggingface/

# Next run will redownload (normal)
```

### Check Dependencies
```bash
pip list
# Should show: torch, transformers, opencv-python, scikit-learn, pillow, numpy
```

### Update Dependencies (if needed)
```bash
pip install -r requirements.txt --upgrade
```

---

## 🐛 Troubleshooting Commands

### Test TrOCR Model
```bash
python3 << PYTHON
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
print("Loading TrOCR...")
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
print("✓ TrOCR loaded successfully")
PYTHON
```

### Test Image Loading
```bash
python3 << PYTHON
import cv2
img = cv2.imread('unnamed.jpg')
print(f"Image shape: {img.shape}")
print(f"Image dtype: {img.dtype}")
PYTHON
```

### Test Text Extraction
```bash
python3 << PYTHON
import cv2
from src.ocr.text_extractor import TextExtractor

image = cv2.imread('unnamed.jpg')
extractor = TextExtractor()
lines = extractor.extract_text(image)
for i, line in enumerate(lines):
    print(f"Line {i+1}: {line[:60]}...")
PYTHON
```

### Test Similarity Matching
```bash
python3 << PYTHON
from src.grading.similarity_matcher import SimilarityMatcher

expected = "Photosynthesis converts light energy into chemical energy"
student = "Photosynthesis converts light energy to chemical energy"

matcher = SimilarityMatcher([expected])
score = matcher.match(student)
print(f"Similarity: {score*100:.1f}%")
PYTHON
```

---

## 📊 Check Project Status

### View Project Statistics
```bash
# Code line count
wc -l grade_image.py src/**/*.py

# File sizes
ls -lh *.md *.txt *.py

# Dependency count
pip list | wc -l
```

### Verify All Files
```bash
# Check required files exist
ls -1 README.md SETUP.md grade_image.py requirements.txt
ls -1 src/ocr/text_extractor.py src/grading/similarity_matcher.py
```

---

## 📝 Edit Commands (Examples)

### Using nano (Linux/Mac)
```bash
nano grade_image.py
# Edit, then Ctrl+O (save), Ctrl+X (exit)

nano src/grading/similarity_matcher.py
# Edit stop words
```

### Using vim (Linux/Mac)
```bash
vim grade_image.py
# i (insert), edit, ESC, :wq (save & exit)
```

### Using VS Code
```bash
code grade_image.py
# Edit, save (Ctrl+S)
```

### Using Windows Notepad
```bash
notepad grade_image.py
# Edit, save, exit
```

---

## 🚀 Advanced Usage

### Custom Stop Words
```python
from src.grading.similarity_matcher import SimilarityMatcher

# Create custom stop words
custom_stops = {'the', 'a', 'is', 'are', 'and'}

# Modify class before using
SimilarityMatcher.STOP_WORDS = custom_stops

# Use matcher
matcher = SimilarityMatcher(["Answer 1", "Answer 2"])
```

### Direct API Usage
```python
import cv2
from src.ocr.text_extractor import TextExtractor
from src.grading.similarity_matcher import SimilarityMatcher

# Load image
image = cv2.imread('answer_sheet.jpg')

# Extract
extractor = TextExtractor()
texts = extractor.extract_text(image)

# Match
answers = ["Expected 1", "Expected 2", "Expected 3"]
matcher = SimilarityMatcher(answers, similarity_threshold=0.75)

# Grade
for i, text in enumerate(texts[:len(answers)]):
    score = matcher.match(text)
    status = "✓" if matcher.is_correct(text) else "✗"
    print(f"Q{i+1}: {score*100:.1f}% {status}")
```

---

## 📋 Environment Variables

### Disable TensorFlow Warnings
```bash
export TF_ENABLE_ONEDNN_OPTS=0
python grade_image.py
```

### Set Python Path
```bash
export PYTHONPATH=/path/to/AnswerSheetChecker:$PYTHONPATH
python grade_image.py
```

---

## ✅ Checklist Commands

### Pre-Usage Checklist
```bash
# 1. Activate environment
source test/bin/activate

# 2. Check Python version
python --version  # Should be 3.11+

# 3. Check dependencies
pip list | grep -E "torch|transformers|opencv|scikit"

# 4. Verify imports
python -c "from src.ocr.text_extractor import TextExtractor; from src.grading.similarity_matcher import SimilarityMatcher; print('✓ All imports OK')"

# 5. Check image exists
ls -l unnamed.jpg  # or your image file

# 6. Verify grade_image.py config
grep "image_path\|answer_key" grade_image.py

# 7. Run test
python grade_image.py
```

---

## 📞 Quick Help

```bash
# Read documentation
cat README.md          # Full guide
cat SETUP.md           # Installation
cat INDEX.md           # Navigation
cat PROJECT_COMPLETION.md  # Project status

# List commands
type -a python         # Find python
which python3.11       # Specific version
command -v pip         # Check pip

# Directory structure
tree -L 2              # Show tree (if installed)
find . -name "*.py"    # Find Python files
```

---

## 🎉 Ready to Go!

```bash
# One-liner to activate and run
source test/bin/activate && python grade_image.py
```

For more help, see:
- **README.md** - Comprehensive guide
- **SETUP.md** - Installation help
- **INDEX.md** - Documentation index
- **PROJECT_COMPLETION.md** - Project details

---

**Last Updated**: December 4, 2025  
**Status**: ✅ Complete
