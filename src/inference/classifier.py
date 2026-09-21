"""
Atık Sınıflandırma Çıkarım (Inference) Modülü.

Bu modül, eğitilmiş derin öğrenme modellerini kullanarak atık görsellerini
sınıflandırmak için gerekli temel soyut sınıfı (BaseClassifier) ve MobileNetV2
tabanlı somut sınıflandırıcıyı (WasteClassifier) içerir.
"""

import numpy as np
from abc import ABC, abstractmethod
from pathlib import Path
import zipfile
from PIL import Image
import tensorflow as tf



class BaseClassifier(ABC):
    """
    Sınıflandırma modelleri için temel soyut sınıf (Abstract Base Class).

    Tüm özel sınıflandırıcılar bu sınıftan türer; model yükleme, görüntü ön işleme
    ve tahmin arayüzlerini standartlaştırır.

    Attributes:
        class_names (list[str]): Tahmin edilecek sınıf etiketleri listesi.
        model (tf.keras.Model | None): Yüklenen TensorFlow/Keras model nesnesi.
    """

    def __init__(self, class_names: list[str]) -> None:
        """
        BaseClassifier sınıfını verilen sınıf etiketleri listesiyle başlatır.

        Args:
            class_names (list[str]): Çıktı sınıflarının isimleri.
        """
        self.class_names = class_names
        self.model: tf.keras.Model | None = None

    @abstractmethod
    def load_model(self, model_path: str) -> None:
        """
        Model dosyasını diskten yüklemek için soyut metot.

        Args:
            model_path (str): Yüklenecek model dosyasının dosya yolu.
        """
        pass

    @abstractmethod
    def _preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Girdi görüntüsünü modelin beklediği tensör formatına dönüştüren soyut metot.

        Args:
            image (Image.Image): PIL formatındaki ham girdi görüntüsü.

        Returns:
            np.ndarray: Model tahminine hazır, boyutlandırılmış ve normalize edilmiş tensör.
        """
        pass

    def predict(self, image: Image.Image) -> tuple[str, float]:
        """
        Girdi görüntüsü üzerinde sınıflandırma tahmini gerçekleştirir.

        Args:
            image (Image.Image): Tahmin edilecek PIL Image nesnesi.

        Returns:
            tuple[str, float]: (tahmin_edilen_sinif_adi, guven_yuzdesi) ikilisi.

        Raises:
            ValueError: Model henüz yüklenmemişse fırlatılır.
        """
        # Modelin belleğe yüklenip yüklenmediğini doğrula
        if self.model is None:
            raise ValueError("Model henüz yüklenmedi.")

        # Görüntüyü ön işleme adımlarından geçirerek tensör formatına getir
        processed_img = self._preprocess_image(image)
        # Model üzerinden çıkarım (inference) gerçekleştirerek olasılık dağılımını al
        predictions = self.model.predict(processed_img)

        # En yüksek olasılık değerine sahip sınıf indeksini belirle (argmax)
        best_class_idx = np.argmax(predictions[0])

        # İndekse karşılık gelen sınıf adını ve yüzde cinsinden güven skorunu hesapla
        predicted_class = self.class_names[best_class_idx]
        confidence = float(predictions[0][best_class_idx]) * 100

        # Sınıf adı ve güven skorunu döndür
        return predicted_class, confidence


class WasteClassifier(BaseClassifier):
    """
    MobileNetV2 tabanlı atık sınıflandırma modelinin yönetim ve çıkarım sınıfı.

    Eğitilmiş Keras modelini (.keras) diskten yükler, ham atık görsellerini
    MobileNetV2 girdi boyutuna (224x224) ve [0, 1] aralığına normalize ederek
    tahmin üretir.

    Attributes:
        model_path (str): Model dosyasının (.keras) disk üzerindeki konumu.
        target_size (tuple[int, int]): Görüntünün yeniden boyutlandırılacağı (genişlik, yükseklik).
    """
    
    def __init__(self, model_path: str, class_names: list[str], target_size: tuple[int, int] = (224, 224)):
        """
        WasteClassifier nesnesini başlatır ve modeli otomatik olarak yükler.

        Args:
            model_path (str): Eğitilmiş .keras model dosyasının dosya yolu.
            class_names (list[str]): Tahmin edilecek sınıf etiketleri listesi.
            target_size (tuple[int, int], optional): Model girdi çözünürlüğü. Varsayılan (224, 224).
        """
        super().__init__(class_names=class_names)
        self.model_path = model_path
        self.target_size = target_size
        
        # Sınıflandırıcı başlatılırken modeli belirtilen dosya yolundan belleğe yükle
        self.load_model(self.model_path)

    def load_model(self, model_path: str) -> None:
        """
        Verilen dosya yolundaki Keras modelini doğrular ve belleğe yükler.

        Args:
            model_path (str): Model dosyasının dosya yolu.

        Raises:
            FileNotFoundError: Model dosyası belirtilen konumda bulunamazsa.
            ValueError: Dosya geçerli bir zip/.keras arşivi değilse.
            RuntimeError: Model yükleme aşamasında TensorFlow tarafında hata oluşursa.
        """
        # Dosya yolu nesnesini oluştur ve dosyanın varlığını doğrula
        model_file = Path(model_path)
        if not model_file.is_file():
            raise FileNotFoundError(f"Model dosyası bulunamadı: {model_file}")
        # Keras 3 formatı zip tabanlı arşivdir; dosyanın geçerli bir zip arşivi olduğunu doğrula
        if not zipfile.is_zipfile(model_file):
            raise ValueError(f"Model dosyası geçersiz .keras arşivi: {model_file}")

        try:
            # TensorFlow/Keras ile modeli diskten belleğe yükle
            self.model = tf.keras.models.load_model(str(model_file))
        except Exception as e:
            # Model yükleme hatasını yakala ve açıklayıcı RuntimeError fırlat
            raise RuntimeError(f"Model yüklenirken hata oluştu: {e}")

    
    # Görüntü ön işleme adımları
    def _preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Görüntüyü MobileNetV2 girdisine ve notebook'taki ön işleme adımlarına hazırlar.

        Args:
            image (Image.Image): PIL Image formatında ham girdi görüntüsü.

        Returns:
            np.ndarray: Şekli (1, 224, 224, 3) ve değer aralığı [0.0, 1.0] olan normalize edilmiş tensör.
        """
        # Eğer görsel PNG formatında ve saydam arka planlıysa, RGB'ye dönüştürerek alpha kanalını eliyoruz
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        # Görseli modelin eğitim boyutu olan 224x224'e ayarladık
        image = image.resize(self.target_size)
        # PIL görüntüsünü NumPy tensörüne dönüştür
        img_array = tf.keras.preprocessing.image.img_to_array(image)
        
        # Notebook'taki Veri Önişleme (rescale=1./255) adımı ile eşleme
        img_array = img_array / 255.0  
        
        # Batch boyutu ekleme: (224, 224, 3) -> (1, 224, 224, 3)
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
