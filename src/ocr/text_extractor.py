"""Text extraction using TrOCR for handwritten text recognition"""
import numpy as np
from typing import List
import cv2
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel


class TextExtractor:
    """Extract handwritten text using TrOCR"""
    
    def __init__(self, languages: List[str] = ['en'], gpu: bool = False):
        """Initialize TrOCR"""
        self.processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
        self.model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
        self.device = "cuda" if gpu else "cpu"
        self.model.to(self.device)
    
    def extract_text(self, image: np.ndarray) -> List[str]:
        """Extract handwritten text lines from image"""
        try:
            # Detect text lines using horizontal line detection
            lines = self._detect_text_lines(image)
            
            text_lines = []
            for y_start, y_end in lines:
                # Extract line region
                line_image = image[y_start:y_end, :]
                
                # Recognize with TrOCR
                text = self._recognize_line(line_image)
                if text.strip():
                    text_lines.append(text)
            
            return text_lines
        except Exception as e:
            print(f"OCR error: {e}")
            return []
    
    def _detect_text_lines(self, image: np.ndarray) -> List[tuple]:
        """Detect horizontal text lines"""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
            
            # Binarize
            _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
            
            # Use smaller morphological kernel for text line detection
            kernel_height = max(3, gray.shape[0] // 30)  # Height of typical text
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, kernel_height))
            
            eroded = cv2.erode(binary, kernel, iterations=1)
            dilated = cv2.dilate(eroded, kernel, iterations=2)
            
            # Find contours
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            lines = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                # More permissive line height detection
                if h > 5:  # Very permissive
                    lines.append((y, y + h))
            
            # Sort and merge overlapping lines
            if lines:
                lines.sort()
                merged = [lines[0]]
                for start, end in lines[1:]:
                    if start <= merged[-1][1] + 3:  # Tight merge threshold
                        merged[-1] = (merged[-1][0], max(merged[-1][1], end))
                    else:
                        merged.append((start, end))
                return merged
            else:
                # Fallback: divide image into 5 parts
                h = image.shape[0]
                return [(i*h//5, (i+1)*h//5) for i in range(5)]
                
        except Exception as e:
            print(f"Line detection error: {e}")
            h = image.shape[0]
            return [(i*h//5, (i+1)*h//5) for i in range(5)]
    
    def _recognize_line(self, line_image: np.ndarray) -> str:
        """Recognize a single line using TrOCR"""
        try:
            # Convert to PIL Image
            if len(line_image.shape) == 3 and line_image.shape[2] == 3:
                line_image = cv2.cvtColor(line_image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(line_image)
            
            # TrOCR inference
            pixel_values = self.processor(images=pil_image, return_tensors="pt").pixel_values.to(self.device)
            generated_ids = self.model.generate(pixel_values, max_new_tokens=100)
            generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            return generated_text
        except Exception as e:
            return ""
