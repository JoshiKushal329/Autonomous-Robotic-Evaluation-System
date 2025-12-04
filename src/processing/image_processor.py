"""Image preprocessing: Skew correction, denoise, contrast, binarization"""
import cv2
import numpy as np


class ImageProcessor:
    """Preprocesses handwritten answer sheet images"""
    
    def preprocess(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for OCR: denoise + enhance contrast (skip binarization)"""
        # Denoise
        image = cv2.bilateralFilter(image, 9, 75, 75)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Enhance contrast (skip harsh binarization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        return enhanced
    
    def _skew_correction(self, image: np.ndarray) -> np.ndarray:
        """Detect and correct image skew"""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=50, maxLineGap=10)
            
            if lines is None or len(lines) == 0:
                return image
            
            # Calculate median angle from detected lines
            angles = [np.degrees(np.arctan2(y2 - y1, x2 - x1)) for x1, y1, x2, y2 in lines[:, 0]]
            median_angle = np.median(angles)
            
            # Rotate image
            h, w = image.shape[:2]
            M = cv2.getRotationMatrix2D((w // 2, h // 2), median_angle, 1.0)
            return cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        except:
            return image
