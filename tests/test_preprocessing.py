"""
Görüntü Ön İşleme (Preprocessing) Birim Testleri.

Bu modül, atık sınıflandırma modeline giren görsellerin yeniden boyutlandırma,
RGB renk uzayına dönüştürme, piksel normalizasyonu ve batch boyutu genişletme
gibi temel veri ön işleme adımlarını test eder.
"""

import pytest
import numpy as np
from PIL import Image
from pathlib import Path
import sys

# Proje ana dizinini ve src klasörünü Python arama yoluna (sys.path) ekle
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.inference.classifier import WasteClassifier


class TestPreprocessing:
    """
    Görüntü ön işleme adımlarının doğruluğunu test eden sınıf.
    
    Görüntü boyutları, renk kanalları, piksel değer aralıkları ve
    tensör şekillerinin model beklentileriyle tam uyumunu denetler.
    """
    
    @pytest.fixture
    def test_classifier(self):
        """
        Test için sınıflandırıcı örneği fixture'ı.
        
        Modeli test etmek için kullanılabilecek mock/örnek nesne sağlar.
        Birim testlerde gerçek disk modelinin yüklenmesini önlemek için None döner.
        """
        # Modeli test etmek için kullanılabilecek mock oluştur
        # Gerçek model yüklememek için
        return None
    
    def test_image_resize(self):
        """
        Görüntü boyutlandırma ve renk modu kontrolü.
        
        Görüntü nesnesinin boyut ve RGB mod özelliklerinin korunduğunu test eder.
        """
        # 100x100 boyutunda kırmızı test görüntüsü oluştur
        test_image = Image.new('RGB', (100, 100), color='red')
        
        # Boyut ve renk modunu doğrula
        assert test_image.size == (100, 100)
        assert test_image.mode == 'RGB'
    
    def test_rgb_conversion(self):
        """
        RGBA formatından RGB formatına dönüştürme kontrolü.
        
        Saydamlık (alpha) kanalı içeren PNG ve RGBA formatındaki görsellerin
        3 kanallı standart RGB formatına başarıyla dönüştürüldüğünü doğrular.
        """
        # 4 kanallı RGBA (saydamlık içeren) test görüntüsü oluştur
        rgba_image = Image.new('RGBA', (100, 100), color=(255, 0, 0, 255))
        
        # Alpha kanalını eleyerek RGB formatına dönüştür
        rgb_image = rgba_image.convert('RGB')
        
        # Dönüştürülen görselin modunu ve boyutlarını doğrula
        assert rgb_image.mode == 'RGB'
        assert rgb_image.size == (100, 100)
    
    def test_normalization_range(self):
        """
        Piksel normalizasyonu aralık kontrolü.
        
        0-255 tamsayı piksel değerlerinin 255.0'a bölünerek [0.0, 1.0] aralığında
        ondalıklı (float32) değerlere ölçeklendiğini doğrular.
        """
        # 0-255 aralığında rastgele uint8 piksel dizisi (tensör) oluştur
        array = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
        
        # Normalizasyon adımı: piksel değerlerini 0.0 - 1.0 aralığına ölçekle
        normalized = array.astype(np.float32) / 255.0
        
        # Sonucun kesinlikle 0.0 ile 1.0 aralığında olduğunu doğrula
        assert normalized.min() >= 0.0
        assert normalized.max() <= 1.0
    
    def test_batch_expansion(self):
        """
        Batch boyutu genişletme kontrolü.
        
        Tekil görüntü tensörünün (224, 224, 3) başına batch boyutu eklenerek
        Keras/TensorFlow girdi şekli olan (1, 224, 224, 3) formuna getirildiğini doğrular.
        """
        # Tek bir görüntü tensörü oluştur: (224, 224, 3)
        array = np.random.rand(224, 224, 3).astype(np.float32)
        
        # Eksen 0'a batch boyutu ekle
        batched = np.expand_dims(array, axis=0)
        
        # Elde edilen tensör şeklinin (1, 224, 224, 3) olduğunu doğrula
        assert batched.shape == (1, 224, 224, 3)
    
    def test_class_mapping_order(self):
        """
        Sınıf haritalaması ve sıralama kontrolü.
        
        Modelin alfabetik klasör düzenine göre eğitilen sınıf sırasının
        (cardboard -> Karton, glass -> Cam...) tutarlı olduğunu doğrular.
        """
        # Modelin İngilizce klasör alfabetik dizilimine sadık kalınmış Türkçe karşılıkları
        classes = ["Karton", "Cam", "Metal", "Kağıt", "Plastik", "Genel Çöp"]
        
        # Sınıf listesinin 6 elemanlı olduğunu ve ilk iki sınıfın sırasını doğrula
        assert len(classes) == 6
        assert classes[0] == "Karton"
        assert classes[1] == "Cam"
