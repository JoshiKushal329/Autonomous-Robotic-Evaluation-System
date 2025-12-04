# Project Files Guide

## 📋 Quick Reference

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `README.md` | Main documentation | 350+ | ✅ Complete |
| `SETUP.md` | Installation guide | 120+ | ✅ Complete |
| `PROJECT_COMPLETION.md` | Project summary | 300+ | ✅ Complete |
| `grade_image.py` | Main executable | 48 | ✅ Production |
| `requirements.txt` | Dependencies | 6 | ✅ Minimal |
| `.gitignore` | Git ignore rules | 40 | ✅ Ready |

## 📂 Root-Level Files

### Documentation

#### `README.md` (9.5 KB)
- **Purpose**: Complete user guide
- **Contents**:
  - Features & quick start
  - Architecture explanation
  - Configuration guide
  - Troubleshooting
  - Usage examples
  - Known limitations
- **Read First**: Yes, start here

#### `SETUP.md` (3.6 KB)
- **Purpose**: Installation instructions
- **Contents**:
  - Prerequisites
  - Virtual environment setup
  - Dependency installation
  - Verification steps
  - Troubleshooting
- **When to Use**: During initial setup

#### `PROJECT_COMPLETION.md` (8 KB)
- **Purpose**: Project summary & status
- **Contents**:
  - Architecture overview
  - Feature list
  - Performance metrics
  - Customization examples
  - Future enhancements
- **When to Use**: Project review/reference

#### `PROJECT_FILES.md` (This file)
- **Purpose**: File directory & purposes
- **Contents**: File descriptions, purposes, update frequency

### Configuration

#### `requirements.txt` (107 bytes)
- **Purpose**: Python dependencies
- **Contents**:
  ```
  numpy==1.26.3
  opencv-python==4.8.0.74
  pillow==10.1.0
  scikit-learn==1.3.2
  torch==2.0.0
  transformers==4.30.0
  ```
- **Update Frequency**: Rarely (only if dependencies change)

#### `.gitignore` (700+ bytes)
- **Purpose**: Git ignore rules
- **Contents**: Ignore patterns for virtualenv, cache, images, etc.
- **Update Frequency**: Never (unless extending project)

### Executable

#### `grade_image.py` (1.7 KB, 48 lines)
- **Purpose**: Main entry point
- **What It Does**:
  1. Load answer sheet image
  2. Extract text lines via TrOCR
  3. Calculate similarity with answer key
  4. Display per-question results
- **Configuration**:
  - Line 12: `image_path = 'unnamed.jpg'`
  - Lines 35-40: `answer_key = [...]`
  - Line 44: `similarity_threshold=0.70`
- **Usage**: `python grade_image.py`
- **Update Frequency**: Only when customizing

## 📂 `src/` Directory (Core Logic)

### `src/ocr/` - Text Extraction

#### `__init__.py`
- **Purpose**: Python package marker
- **Content**: Empty or minimal imports
- **Update Frequency**: Never

#### `text_extractor.py` (4 KB, 120 lines)
- **Purpose**: Handwritten text extraction
- **Main Class**: `TextExtractor`
- **Key Methods**:
  - `__init__()`: Load TrOCR model
  - `extract_text()`: Main extraction pipeline
  - `_detect_text_lines()`: Find text regions
  - `_recognize_line()`: Per-line OCR
- **Model**: microsoft/trocr-base-handwritten (downloaded on first use)
- **Update Frequency**: Only for algorithm improvements

### `src/grading/` - Similarity Matching

#### `__init__.py`
- **Purpose**: Python package marker
- **Content**: Empty or minimal imports
- **Update Frequency**: Never

#### `similarity_matcher.py` (2 KB, 60 lines)
- **Purpose**: Answer similarity calculation
- **Main Class**: `SimilarityMatcher`
- **Key Features**:
  - 60+ stop words for filtering
  - TF-IDF vectorization
  - Cosine similarity scoring
- **Configuration**: `STOP_WORDS` set (customize if needed)
- **Update Frequency**: Only for tuning

### `src/processing/` - Image Utilities

#### `__init__.py`
- **Purpose**: Python package marker
- **Content**: Empty or minimal imports
- **Update Frequency**: Never

#### `image_processor.py` (1 KB, 45 lines)
- **Purpose**: Optional image preprocessing
- **Status**: Available but not used in default pipeline
- **Methods**: denoise(), enhance(), preprocess()
- **Update Frequency**: Rarely (advanced customization)

## 📂 `config/` Directory

#### `settings.py`
- **Purpose**: Global configuration (optional)
- **Status**: Not actively used
- **Future**: Can be extended for advanced settings

## 📂 `data/` Directory

#### `datasets/`
- **Purpose**: Training data storage (optional)
- **Status**: Empty, available for future use
- **Use Case**: Fine-tuning models, storing test datasets

## 📂 `test/` Directory

#### Virtual Environment
- **Purpose**: Isolated Python environment
- **Contents**: Python interpreter, installed packages
- **Size**: ~3 GB
- **Usage**: `source test/bin/activate`
- **Git Status**: Ignored (.gitignore)

## 📊 File Statistics

```
Total Project Files (excluding venv):
- Documentation: 4 files (README, SETUP, PROJECT_COMPLETION, PROJECT_FILES)
- Configuration: 2 files (requirements.txt, .gitignore)
- Executables: 1 file (grade_image.py)
- Source Code: 6 files (3 __init__.py + 3 module files)
- Optional: 2 files (settings.py, image_processor.py)

Code Distribution:
- grade_image.py: 48 lines (entry point)
- text_extractor.py: 120 lines (TrOCR)
- similarity_matcher.py: 60 lines (matching)
- image_processor.py: 45 lines (preprocessing)
- __init__ files: Minimal
Total: ~250 lines of core code
```

## 🔄 Workflow: Where Files Are Used

### User Workflow
1. Read: `SETUP.md` → Install
2. Edit: `grade_image.py` → Configure
3. Run: `grade_image.py` → Process
4. Reference: `README.md` → Troubleshoot

### During Execution
1. `grade_image.py` imports `TextExtractor`
2. `TextExtractor` loads TrOCR model (cached)
3. `TextExtractor` calls `text_extractor.py`
4. `grade_image.py` imports `SimilarityMatcher`
5. `SimilarityMatcher` processes results

### For Customization
- Adjust threshold: Edit `grade_image.py` line 44
- Change stop words: Edit `similarity_matcher.py` STOP_WORDS
- Modify preprocessing: Edit `text_extractor.py` _detect_text_lines()
- Use image processor: Uncomment in `grade_image.py`

## 🛠️ Maintenance

### What to Update
- **Never**: Virtual environment (`test/`), `__init__.py` files, `.gitignore`
- **Rarely**: `requirements.txt`, core algorithms
- **Sometimes**: Stop words, thresholds, answer keys
- **Regularly**: `image_path` in `grade_image.py`

### Backup Files
- Critical: `grade_image.py`, all `src/` files
- Reference: `README.md`, `SETUP.md`
- Can be regenerated: Virtual environment, cached models

### File Permissions
- Executable: `grade_image.py` should be runnable
- Readable: All `.py` and `.md` files
- Writable: Only `grade_image.py` (for customization)

## 📝 Adding New Files

If you extend the project:

1. **New OCR module**: Place in `src/ocr/`
2. **New classifier**: Place in `src/grading/`
3. **New utilities**: Place in `src/processing/`
4. **Update**: Add to `requirements.txt` if new dependencies
5. **Document**: Update `README.md` architecture section

---

**Last Updated**: December 4, 2025  
**Version**: 1.0.0  
**Status**: ✅ Complete
