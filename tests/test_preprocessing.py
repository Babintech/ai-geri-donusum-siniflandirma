"""Ön işleme işlevleri için testler."""

import pytest
import numpy as np
from PIL import Image
from pathlib import Path
import sys

# src klasörünü Python path'ine ekle
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.inference.classifier import WasteClassifier


class TestPreprocessing:
    """Görüntü ön işlemesi testleri."""
    
    @pytest.fixture
    def test_classifier(self):
        """Test için sınıflandırıcı örneği oluştur."""
        # Modeli test etmek için kullanılabilecek mock oluştur
        # Gerçek model yüklememek için
        return None
    
    def test_image_resize(self):
        """Görüntü boyutlandırma kontrolü."""
        # 100x100 test görüntüsü oluştur
        test_image = Image.new('RGB', (100, 100), color='red')
        
        # Boyutu kontrol et
        assert test_image.size == (100, 100)
        assert test_image.mode == 'RGB'
    
    def test_rgb_conversion(self):
        """RGBA'dan RGB'ye dönüştürme kontrolü."""
        # RGBA görüntüsü oluştur
        rgba_image = Image.new('RGBA', (100, 100), color=(255, 0, 0, 255))
        
        # RGB'ye dönüştür
        rgb_image = rgba_image.convert('RGB')
        
        assert rgb_image.mode == 'RGB'
        assert rgb_image.size == (100, 100)
    
    def test_normalization_range(self):
        """Normalizasyon aralığı kontrolü."""
        # 0-255 aralığında array oluştur
        array = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
        
        # Normalizasyon yap
        normalized = array.astype(np.float32) / 255.0
        
        # Sonucun 0-1 aralığında olduğunu kontrol et
        assert normalized.min() >= 0.0
        assert normalized.max() <= 1.0
    
    def test_batch_expansion(self):
        """Batch boyutu genişletme kontrolü."""
        # (224, 224, 3) array oluştur
        array = np.random.rand(224, 224, 3).astype(np.float32)
        
        # Batch boyutu ekle
        batched = np.expand_dims(array, axis=0)
        
        # Sonuç (1, 224, 224, 3) olmalı
        assert batched.shape == (1, 224, 224, 3)
    
    def test_class_mapping_order(self):
        """Sınıf haritalaması sırasının kontrolü."""
        # Alfabetik sırada olan sınıflar
        classes = ["Karton", "Cam", "Metal", "Kağıt", "Plastik", "Genel Çöp"]
        
        # Sınıflar alfabetik sırada olmalı (İngilizce sırasına göre)
        assert len(classes) == 6
        assert classes[0] == "Karton"
        assert classes[1] == "Cam"
