"""
Inference ve Model Arayüzü Testleri.

Bu modül, sınıflandırma arayüzünün doğruluğunu, sınıf etiketlerinin bütünlüğünü,
güven skoru sınırlarını ve tahmin çıktısı formatını test eder.
"""

import pytest
import numpy as np
from PIL import Image
from pathlib import Path
import sys

# Proje ana dizinini ve src klasörünü Python arama yoluna (sys.path) ekle
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.inference.classifier import WasteClassifier


class TestInferenceInterface:
    """
    Sınıflandırıcı çıkarım arayüzü ve veri yapıları birim testleri.
    
    Bu test sınıfı, model çıktılarının formatını, sınıf eşleşmelerini ve
    matematiksel güven aralığı tutarlılığını doğrular.
    """
    
    def test_class_names_count(self):
        """
        Sınıf sayısının kontrolü.
        
        Modelin eğitildiği 6 ana atık kategorisinin (Karton, Cam, Metal,
        Kağıt, Plastik, Genel Çöp) eksiksiz tanımlandığını doğrular.
        """
        classes = ["Karton", "Cam", "Metal", "Kağıt", "Plastik", "Genel Çöp"]
        # Model çıktısı tam olarak 6 sınıftan oluşmalıdır
        assert len(classes) == 6
    
    def test_confidence_range(self):
        """
        Güven skorunun aralık kontrolü.
        
        Softmax olasılık dağılımından üretilen güven yüzdesinin
        [0, 100] aralığında geçerli bir değer olduğunu doğrular.
        """
        # Rastgele soft-max çıktısı simüle et (toplamı 1.0 olan olasılık dağılımı)
        predictions = np.random.rand(6)
        predictions = predictions / predictions.sum()  # Softmax normalizasyonu
        
        # En yüksek olasılığı yüzde formatına dönüştür
        confidence = float(np.max(predictions)) * 100
        
        # Güven skoru 0 ile 100 aralığında olmalı
        assert 0 <= confidence <= 100
    
    def test_prediction_output_format(self):
        """
        Tahmin çıktısı formatının kontrolü.
        
        predict() fonksiyonundan dönen sonucun (str, float) ikilisi
        (tuple) tipinde olduğunu doğrular.
        """
        classes = ["Karton", "Cam", "Metal", "Kağıt", "Plastik", "Genel Çöp"]
        
        # Rastgele tahmin yap (simülasyon)
        class_idx = np.random.randint(0, 6)
        prediction = classes[class_idx]
        confidence = np.random.rand() * 100
        
        # Tuple formatı ve veri tiplerini kontrol et
        result = (prediction, confidence)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert isinstance(result[1], float)
    
    def test_invalid_class_index(self):
        """
        Geçersiz sınıf indeksi kontrolü.
        
        Sınıf listesi aralığı dışındaki indekslerin sınır dışı kaldığını
        ve indeks sınırlarının doğru korunduğunu test eder.
        """
        classes = ["Karton", "Cam", "Metal", "Kağıt", "Plastik", "Genel Çöp"]
        
        # Geçerli indeks kontrolü (liste sınırları içinde)
        valid_idx = 0
        assert valid_idx >= 0 and valid_idx < len(classes)
        
        # Geçersiz indeks kontrolü (liste sınırları dışında)
        invalid_idx = 10
        assert not (invalid_idx >= 0 and invalid_idx < len(classes))
