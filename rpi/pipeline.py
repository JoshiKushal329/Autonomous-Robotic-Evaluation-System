"""
Optimized pipeline for Raspberry Pi
Uses quantized models and efficient processing
"""

import sys
import os
from pathlib import Path
import cv2
import numpy as np
from typing import List, Tuple, Dict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ocr.text_extractor import TextExtractor
from src.grading.similarity_matcher import SimilarityMatcher


class RPiPipeline:
    """
    Optimized grading pipeline for Raspberry Pi
    Handles camera capture → OCR → Grading with efficient processing
    """
    
    def __init__(self, model_name: str = "microsoft/trocr-base-handwritten", 
                 threshold: float = 0.70):
        """
        Initialize RPi pipeline
        
        Args:
            model_name: TrOCR model to use
            threshold: Grading threshold (0-1)
        """
        print("📱 Initializing RPi Pipeline...")
        
        self.threshold = threshold
        self.extractor = None
        self.matcher = SimilarityMatcher(threshold=threshold)
        self.answer_key = []
        
        try:
            self.extractor = TextExtractor(model_name=model_name)
            print("✓ TextExtractor initialized")
        except Exception as e:
            print(f"⚠️  TextExtractor initialization: {e}")
    
    def set_answer_key(self, answer_key: List[str]):
        """
        Set the answer key for grading
        
        Args:
            answer_key: List of correct answers
        """
        self.answer_key = answer_key
        print(f"✓ Answer key set ({len(answer_key)} questions)")
    
    def process_image(self, image_path: str) -> Tuple[List[str], bool]:
        """
        Extract text from image
        
        Args:
            image_path: Path to image file
        
        Returns:
            Tuple[extracted_text, success]
        """
        try:
            if not os.path.exists(image_path):
                print(f"❌ Image not found: {image_path}")
                return [], False
            
            print(f"📷 Loading image: {image_path}")
            image = cv2.imread(image_path)
            
            if image is None:
                print(f"❌ Failed to load image: {image_path}")
                return [], False
            
            # Get image info
            height, width = image.shape[:2]
            size_mb = os.path.getsize(image_path) / (1024 * 1024)
            print(f"   Size: {width}×{height} ({size_mb:.1f} MB)")
            
            # Extract text
            print("🔍 Extracting text...")
            extracted = self.extractor.extract_text(image)
            
            if not extracted:
                print("❌ No text extracted")
                return [], False
            
            print(f"✓ Extracted {len(extracted)} lines of text")
            for i, text in enumerate(extracted, 1):
                print(f"   Line {i}: {text[:50]}...")
            
            return extracted, True
            
        except Exception as e:
            print(f"❌ Processing error: {e}")
            import traceback
            traceback.print_exc()
            return [], False
    
    def grade_answers(self, extracted_text: List[str], 
                     verbose: bool = True) -> Dict[int, Dict]:
        """
        Grade extracted answers against key
        
        Args:
            extracted_text: List of extracted answers
            verbose: Print detailed output
        
        Returns:
            Dict with grading results
        """
        if not self.answer_key:
            print("❌ Answer key not set")
            return {}
        
        if not extracted_text:
            print("❌ No text to grade")
            return {}
        
        print("📊 Grading answers...")
        results = {}
        passed = 0
        total = min(len(extracted_text), len(self.answer_key))
        
        for i in range(total):
            student_answer = extracted_text[i] if i < len(extracted_text) else ""
            expected_answer = self.answer_key[i]
            
            # Get similarity score
            score = self.matcher.calculate_similarity(student_answer, expected_answer)
            passed_q = score >= self.threshold
            passed += int(passed_q)
            
            results[i + 1] = {
                "expected": expected_answer,
                "student": student_answer,
                "similarity": score,
                "status": "✓ PASS" if passed_q else "✗ FAIL"
            }
            
            if verbose:
                status_icon = "✅" if passed_q else "❌"
                print(f"\n{status_icon} Q{i+1}: {score*100:.1f}%")
                print(f"   Expected: {expected_answer[:60]}")
                print(f"   Student:  {student_answer[:60]}")
        
        # Summary
        percentage = (passed / total * 100) if total > 0 else 0
        print(f"\n📈 Summary: {passed}/{total} passed ({percentage:.1f}%)")
        
        results["summary"] = {
            "total_questions": total,
            "passed": passed,
            "percentage": percentage,
            "threshold": self.threshold
        }
        
        return results
    
    def full_pipeline(self, image_path: str, answer_key: List[str],
                     save_output: str = None) -> Dict:
        """
        Run complete pipeline: load → extract → grade
        
        Args:
            image_path: Path to answer sheet image
            answer_key: List of correct answers
            save_output: Optional path to save results JSON
        
        Returns:
            Dict with complete results
        """
        print("\n" + "="*60)
        print("🚀 STARTING ANSWER SHEET GRADING PIPELINE")
        print("="*60)
        
        # Set answer key
        self.set_answer_key(answer_key)
        
        # Extract text
        extracted, success = self.process_image(image_path)
        if not success:
            return {"error": "Failed to process image", "success": False}
        
        # Grade
        results = self.grade_answers(extracted, verbose=True)
        results["success"] = True
        results["image"] = image_path
        
        # Save results if requested
        if save_output:
            self._save_results(results, save_output)
        
        print("="*60)
        print("✓ Pipeline complete")
        print("="*60)
        
        return results
    
    def _save_results(self, results: Dict, output_path: str):
        """
        Save grading results to JSON
        
        Args:
            results: Grading results dictionary
            output_path: Path to save results
        """
        try:
            import json
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2)
            
            print(f"✓ Results saved: {output_path}")
            
        except Exception as e:
            print(f"⚠️  Failed to save results: {e}")


def optimize_image_for_rpi(image_path: str, max_width: int = 1280, 
                          max_height: int = 960) -> np.ndarray:
    """
    Optimize image size for RPi processing
    Reduces memory and processing time
    
    Args:
        image_path: Path to image
        max_width: Maximum width
        max_height: Maximum height
    
    Returns:
        np.ndarray: Resized image
    """
    image = cv2.imread(image_path)
    if image is None:
        return None
    
    height, width = image.shape[:2]
    
    # Calculate scaling factor
    scale = min(max_width / width, max_height / height)
    
    if scale < 1:
        new_width = int(width * scale)
        new_height = int(height * scale)
        image = cv2.resize(image, (new_width, new_height), 
                          interpolation=cv2.INTER_AREA)
        print(f"✓ Optimized: {width}×{height} → {new_width}×{new_height}")
    
    return image
