"""
Camera capture module for Raspberry Pi
Supports both PiCamera and USB cameras
"""

import cv2
import numpy as np
from typing import Optional, Tuple
from pathlib import Path


class RPiCameraCapture:
    """
    Capture images from Raspberry Pi camera or USB camera
    Optimized for low-resource environments
    """
    
    def __init__(self, camera_id: int = 0, resolution: Tuple[int, int] = (1920, 1440)):
        """
        Initialize camera capture
        
        Args:
            camera_id: Camera device ID (0 for default, 1+ for USB)
            resolution: Target resolution (width, height)
        """
        self.camera_id = camera_id
        self.resolution = resolution
        self.cap = None
        self.connect()
    
    def connect(self) -> bool:
        """
        Initialize camera connection
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            
            if not self.cap.isOpened():
                print(f"❌ Failed to open camera {self.camera_id}")
                return False
            
            # Set resolution
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            
            # Set FPS to 30
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            # Disable auto-focus if available
            try:
                self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
            except:
                pass
            
            print(f"✓ Camera {self.camera_id} connected at {self.resolution}")
            return True
            
        except Exception as e:
            print(f"❌ Camera error: {e}")
            return False
    
    def capture(self, delay_ms: int = 500) -> Optional[np.ndarray]:
        """
        Capture single frame
        
        Args:
            delay_ms: Delay before capture (allows focus/exposure settle)
        
        Returns:
            np.ndarray: Frame or None if failed
        """
        if not self.cap or not self.cap.isOpened():
            print("❌ Camera not connected")
            return None
        
        try:
            import time
            time.sleep(delay_ms / 1000.0)
            
            ret, frame = self.cap.read()
            if not ret:
                print("❌ Failed to capture frame")
                return None
            
            return frame
            
        except Exception as e:
            print(f"❌ Capture error: {e}")
            return None
    
    def capture_preview(self, duration_sec: int = 5, show_fps: bool = True) -> Optional[np.ndarray]:
        """
        Show live preview and capture after duration
        
        Args:
            duration_sec: Preview duration in seconds
            show_fps: Show FPS counter
        
        Returns:
            np.ndarray: Final captured frame
        """
        if not self.cap or not self.cap.isOpened():
            print("❌ Camera not connected")
            return None
        
        import time
        start_time = time.time()
        frame_count = 0
        
        print(f"Preview for {duration_sec} seconds... Press 'q' to cancel")
        
        try:
            while time.time() - start_time < duration_sec:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                if show_fps:
                    elapsed = time.time() - start_time
                    fps = frame_count / elapsed if elapsed > 0 else 0
                    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                cv2.imshow('Preview', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cv2.destroyAllWindows()
            return frame
            
        except Exception as e:
            print(f"❌ Preview error: {e}")
            return None
    
    def capture_burst(self, num_frames: int = 5, delay_ms: int = 100) -> list:
        """
        Capture multiple frames for selection
        
        Args:
            num_frames: Number of frames to capture
            delay_ms: Delay between captures
        
        Returns:
            list: List of frames
        """
        frames = []
        
        for i in range(num_frames):
            frame = self.capture(delay_ms)
            if frame is not None:
                frames.append(frame)
                print(f"✓ Captured frame {i+1}/{num_frames}")
            else:
                print(f"❌ Failed to capture frame {i+1}/{num_frames}")
        
        return frames
    
    def save_frame(self, frame: np.ndarray, filename: str) -> bool:
        """
        Save frame to disk
        
        Args:
            frame: Image frame
            filename: Output filename
        
        Returns:
            bool: Success status
        """
        try:
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            success = cv2.imwrite(filename, frame)
            
            if success:
                print(f"✓ Saved: {filename}")
            else:
                print(f"❌ Failed to save: {filename}")
            
            return success
            
        except Exception as e:
            print(f"❌ Save error: {e}")
            return False
    
    def release(self):
        """Release camera resources"""
        if self.cap:
            self.cap.release()
            print("✓ Camera released")


def detect_available_cameras() -> list:
    """
    Detect available cameras on the system
    
    Returns:
        list: List of available camera indices
    """
    available = []
    
    for i in range(5):  # Check first 5 indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                available.append(i)
            cap.release()
    
    return available
