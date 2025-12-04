"""
Simple workflow: Preprocess Image → Extract Text → Check Similarity
"""
import cv2
from src.processing.image_processor import ImageProcessor
from src.ocr.text_extractor import TextExtractor
from src.grading.similarity_matcher import SimilarityMatcher

# ============================================
# STEP 1: LOAD IMAGE
# ============================================
image_path = 'unnamed.jpg'
image = cv2.imread(image_path)

if image is None:
    print("❌ Error: Image not found!")
    exit()

print(f"✓ Image loaded: shape={image.shape}")

# ============================================
# STEP 2: EXTRACT TEXT
# ============================================
extractor = TextExtractor(languages=['en'], gpu=False)
extracted_text = extractor.extract_text(image)
print(f"✓ Text extracted: {len(extracted_text)} lines")

# ============================================
# STEP 3: CHECK SIMILARITY WITH ANSWERS
# ============================================
answer_key = [
    "Photosynthesis converts light energy into chemical energy",
    "Cellular respiration releases energy from glucose",
    "Mitochondria are the powerhouse of the cell",
    "Photosynthesis occurs in the leaves of plants",
    "Stomata regulate gas exchange in plants"
]

matcher = SimilarityMatcher(answer_key, similarity_threshold=0.70)

print("\n=== SIMILARITY RESULTS ===\n")
for i, student_answer in enumerate(extracted_text[:len(answer_key)]):
    similarity = matcher.match(student_answer)
    status = "✓ PASS" if similarity >= 0.70 else "✗ FAIL"
    print(f"Q{i+1}: {similarity*100:.1f}% {status}")
    print(f"  Student: {student_answer[:60]}...")
    print(f"  Expected: {answer_key[i][:60]}...\n")
