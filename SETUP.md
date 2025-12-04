# Setup & Installation Guide

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Linux/Mac/Windows with ~5GB free disk space

## Step 1: Clone/Navigate to Project

```bash
cd /path/to/AnswerSheetChecker
```

## Step 2: Create Virtual Environment

```bash
python3 -m venv test
```

## Step 3: Activate Virtual Environment

**Linux/Mac:**
```bash
source test/bin/activate
```

**Windows:**
```bash
test\Scripts\activate
```

You should see `(test)` prefix in your terminal.

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `numpy` - Numerical computing
- `opencv-python` - Image processing
- `pillow` - Image I/O
- `scikit-learn` - TF-IDF & similarity
- `torch` - Deep learning framework
- `transformers` - TrOCR model

**First run takes ~2-3 minutes** as PyTorch/transformers are large packages.

## Step 5: Verify Installation

```bash
python -c "
from src.ocr.text_extractor import TextExtractor
from src.grading.similarity_matcher import SimilarityMatcher
print('✓ All imports successful')
"
```

If no errors, you're good to go!

## Step 6: Prepare Your First Image

1. Place a handwritten answer sheet image in the project root
2. Name it clearly (e.g., `answer_sheet.jpg`, `student1.png`)
3. Ensure image is clear, well-lit, and properly oriented

## Step 7: Configure & Run

Edit `grade_image.py`:

```python
# Line 12: Update image path
image_path = 'your_image.jpg'

# Lines 35-40: Update answer key
answer_key = [
    "Your answer 1",
    "Your answer 2",
    "Your answer 3",
    "Your answer 4",
    "Your answer 5"
]
```

Run:
```bash
python grade_image.py
```

## Troubleshooting Installation

### Error: `ModuleNotFoundError: No module named 'torch'`
```bash
pip install -r requirements.txt --force-reinstall
```

### Error: `Permission denied` on Linux/Mac
```bash
chmod +x test/bin/activate
source test/bin/activate
```

### Error: `python3: command not found`
Install Python 3.11+:
- **Ubuntu/Debian**: `sudo apt install python3.11 python3.11-venv`
- **macOS**: `brew install python@3.11`
- **Windows**: Download from https://python.org/

### Error: Virtual environment won't activate
Delete and recreate:
```bash
rm -rf test
python3 -m venv test
source test/bin/activate
pip install -r requirements.txt
```

### Slow first run (downloading TrOCR model)
**This is normal!** The TrOCR model (1.33GB) downloads on first use:
- Subsequent runs skip this download
- Model is cached in `~/.cache/huggingface/`

## Project Layout After Setup

```
AnswerSheetChecker/
├── test/                           # ✓ Virtual environment created
├── src/
│   ├── ocr/text_extractor.py       # ✓ Ready
│   ├── grading/similarity_matcher.py # ✓ Ready
│   └── processing/image_processor.py # ✓ Ready
├── grade_image.py                  # ✓ Configure this
├── requirements.txt                # ✓ Installed
└── README.md                       # ✓ Instructions
```

## Next Steps

1. **Run your first grade**: `python grade_image.py`
2. **Review results**: Check output for similarity scores
3. **Adjust threshold**: Edit `similarity_threshold=0.70` if needed
4. **Batch process**: Use shell loop for multiple images

## Deactivate Virtual Environment

When done, exit the virtual environment:
```bash
deactivate
```

## Reinstall Clean

If something breaks, start fresh:
```bash
rm -rf test
python3 -m venv test
source test/bin/activate
pip install -r requirements.txt
```

---

**Setup Complete!** You're ready to grade answer sheets. ✅

For usage help, see README.md
For configuration details, see grade_image.py comments
