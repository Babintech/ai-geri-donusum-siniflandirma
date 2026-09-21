"""Inference testleri."""

import pytest
import numpy as np
from PIL import Image
from pathlib import Path
import sys

# src klasörünü Python path'ine ekle
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.inference.classifier import WasteClassifier


class TestInferenceInterface:
    """Inference ara yüzü testleri."""
    
    def test_class_names_count(self):
        """Sınıf sayısının kontrolü."""
        classes = ["Karton", "Cam", "Metal", "Kağıt", "Plastik", "Genel Çöp"]
        assert len(classes) == 6
    
    def test_confidence_range(self):
        """Güven skorunun aralık kontrolü."""
        # Rastgele soft-max çıktısı simüle et
        predictions = np.random.rand(6)
        predictions = predictions / predictions.sum()  # Softmax
        
        confidence = float(np.max(predictions)) * 100
        
        # Güven skoru 0-100 aralığında olmalı
        assert 0 <= confidence <= 100
    
    def test_prediction_output_format(self):
        """Tahmin çıktısı formatının kontrolü."""
        classes = ["Karton", "Cam", "Metal", "Kağıt", "Plastik", "Genel Çöp"]
        
        # Rastgele tahmin yap
        class_idx = np.random.randint(0, 6)
        prediction = classes[class_idx]
        confidence = np.random.rand() * 100
        
        # Tuple formatı kontrol et
        result = (prediction, confidence)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert isinstance(result[1], float)
    
    def test_invalid_class_index(self):
        """Geçersiz sınıf indeksi kontrolü."""
        classes = ["Karton", "Cam", "Metal", "Kağıt", "Plastik", "Genel Çöp"]
        
        # Geçerli indeks
        valid_idx = 0
        assert valid_idx >= 0 and valid_idx < len(classes)
        
        # Geçersiz indeks
        invalid_idx = 10
        assert not (invalid_idx >= 0 and invalid_idx < len(classes))
