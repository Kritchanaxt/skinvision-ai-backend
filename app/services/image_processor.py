"""
Image processing service using OpenCV and MediaPipe
"""
import cv2
import numpy as np
import mediapipe as mp
from PIL import Image
import os
from typing import Optional, Dict, List, Tuple, Any

from app.models.skin_analysis import FaceDetectionResult
from app.core.config import settings

class ImageProcessor:
    """Handle image preprocessing and face detection"""
    
    def __init__(self):
        # Initialize MediaPipe Face Detection
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Face detection model
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=0,  # 0 for short-range, 1 for full-range
            min_detection_confidence=settings.FACE_DETECTION_CONFIDENCE
        )
        
        # Face mesh for landmarks
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    async def process_image(self, image_path: str) -> np.ndarray:
        """
        Load and preprocess image for analysis
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Preprocessed image as numpy array
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Convert BGR to RGB (MediaPipe expects RGB)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Basic preprocessing
        processed_image = self._preprocess_image(image_rgb)
        
        return processed_image
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Apply preprocessing steps to the image
        
        Args:
            image: Input image in RGB format
            
        Returns:
            Preprocessed image
        """
        # Resize if too large (maintain aspect ratio)
        height, width = image.shape[:2]
        max_dimension = 1024
        
        if max(height, width) > max_dimension:
            if width > height:
                new_width = max_dimension
                new_height = int(height * (max_dimension / width))
            else:
                new_height = max_dimension
                new_width = int(width * (max_dimension / height))
            
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        # Enhance contrast and brightness
        image = self._enhance_image_quality(image)
        
        return image
    
    def _enhance_image_quality(self, image: np.ndarray) -> np.ndarray:
        """
        Enhance image quality for better analysis
        
        Args:
            image: Input image
            
        Returns:
            Enhanced image
        """
        # Convert to LAB color space for better processing
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge channels and convert back to RGB
        enhanced_lab = cv2.merge([l, a, b])
        enhanced_rgb = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
        
        return enhanced_rgb
    
    async def detect_face(self, image: np.ndarray) -> FaceDetectionResult:
        """
        Detect face in the image using MediaPipe
        
        Args:
            image: Input image in RGB format
            
        Returns:
            Face detection result
        """
        # Detect faces
        results = self.face_detection.process(image)
        
        if not results.detections:
            return FaceDetectionResult(
                face_detected=False,
                face_count=0
            )
        
        # Get the first (most confident) detection
        detection = results.detections[0]
        
        # Extract bounding box
        bbox = detection.location_data.relative_bounding_box
        height, width = image.shape[:2]
        
        face_bbox = {
            "x": bbox.xmin * width,
            "y": bbox.ymin * height,
            "width": bbox.width * width,
            "height": bbox.height * height,
            "confidence": detection.score[0]
        }
        
        # Get facial landmarks
        landmarks = await self._get_facial_landmarks(image)
        
        return FaceDetectionResult(
            face_detected=True,
            face_count=len(results.detections),
            face_bbox=face_bbox,
            landmarks=landmarks
        )
    
    async def _get_facial_landmarks(self, image: np.ndarray) -> Optional[List[Dict[str, float]]]:
        """
        Extract facial landmarks using MediaPipe Face Mesh
        
        Args:
            image: Input image in RGB format
            
        Returns:
            List of landmark coordinates or None
        """
        results = self.face_mesh.process(image)
        
        if not results.multi_face_landmarks:
            return None
        
        landmarks = []
        height, width = image.shape[:2]
        
        # Get landmarks from the first face
        face_landmarks = results.multi_face_landmarks[0]
        
        for idx, landmark in enumerate(face_landmarks.landmark):
            landmarks.append({
                "id": idx,
                "x": landmark.x * width,
                "y": landmark.y * height,
                "z": landmark.z
            })
        
        return landmarks
    
    def extract_face_region(self, image: np.ndarray, bbox: Dict[str, float]) -> np.ndarray:
        """
        Extract face region from image using bounding box
        
        Args:
            image: Input image
            bbox: Face bounding box coordinates
            
        Returns:
            Cropped face region
        """
        x = int(bbox["x"])
        y = int(bbox["y"])
        w = int(bbox["width"])
        h = int(bbox["height"])
        
        # Add padding around face
        padding = 20
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(image.shape[1] - x, w + 2 * padding)
        h = min(image.shape[0] - y, h + 2 * padding)
        
        face_region = image[y:y+h, x:x+w]
        return face_region
    
    def analyze_image_quality(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Analyze image quality metrics
        
        Args:
            image: Input image
            
        Returns:
            Dictionary with quality metrics
        """
        # Convert to grayscale for analysis
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Calculate blur (Laplacian variance)
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Calculate brightness
        brightness = np.mean(gray)
        
        # Calculate contrast (standard deviation)
        contrast = np.std(gray)
        
        # Determine quality ratings
        blur_quality = "good" if blur_score > 100 else "fair" if blur_score > 50 else "poor"
        brightness_quality = "good" if 50 < brightness < 200 else "fair"
        contrast_quality = "good" if contrast > 30 else "fair" if contrast > 15 else "poor"
        
        return {
            "blur_score": float(blur_score),
            "blur_quality": blur_quality,
            "brightness": float(brightness),
            "brightness_quality": brightness_quality,
            "contrast": float(contrast),
            "contrast_quality": contrast_quality,
            "resolution": f"{image.shape[1]}x{image.shape[0]}",
            "overall_quality": self._calculate_overall_quality(blur_quality, brightness_quality, contrast_quality)
        }
    
    def _calculate_overall_quality(self, blur: str, brightness: str, contrast: str) -> str:
        """Calculate overall image quality"""
        scores = {"good": 3, "fair": 2, "poor": 1}
        total_score = scores[blur] + scores[brightness] + scores[contrast]
        
        if total_score >= 8:
            return "excellent"
        elif total_score >= 6:
            return "good"
        elif total_score >= 4:
            return "fair"
        else:
            return "poor"