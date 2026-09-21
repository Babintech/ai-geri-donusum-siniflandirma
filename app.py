"""
Streamlit Web Arayüzü — AI Tabanlı Atık Sınıflandırma Uygulaması.

Bu modül, eğitilmiş derin öğrenme modelini (MobileNetV2) kullanarak kullanıcıların
yüklediği atık fotoğraflarını sınıflandıran ve doğru geri dönüşüm kutusuna
yönlendiren etkileşimli bir web kullanıcı arayüzü sunar.
"""

from pathlib import Path
import zipfile
import streamlit as st
from PIL import Image

# Yeni modül yapısından import
try:
    from src.inference.classifier import WasteClassifier
except ImportError:
    # Geri uyumluluk: kök klasörden import et
    from classifier import WasteClassifier

# --- MODEL KONFİGÜRASYONLARI (Notebook Analiz Sonuçları) ---
# Uygulama kök dizinini ve olası model dosyası konumlarını belirle
APP_DIR = Path(__file__).resolve().parent
MODEL_CANDIDATES = [
    APP_DIR / "model" / "akilli_kutu_model.keras",
    APP_DIR / "akilli_kutu_model.keras",
]

def resolve_model_path() -> Path:
    """
    Model dosyasının geçerli konumunu tespit eder.

    Aday dosya yollarını sırasıyla tarar ve geçerli bir zip/.keras arşivi
    olan ilk dosyayı döndürür. Bulunamazsa varsayılan aday yolunu döner.

    Returns:
        Path: Bulunan veya varsayılan model dosya yolu.
    """
    # Öncelikli olarak mevcut ve geçerli zip arşivi olan model dosyasını ara
    for candidate in MODEL_CANDIDATES:
        if candidate.is_file() and zipfile.is_zipfile(candidate):
            return candidate
    # Zip doğrulaması geçemese bile mevcut olan ilk aday dosyayı dene
    for candidate in MODEL_CANDIDATES:
        if candidate.is_file():
            return candidate
    # Dosya henüz indirilmemiş veya taşınmamışsa varsayılan konumu dön
    return MODEL_CANDIDATES[0]

MODEL_PATH = resolve_model_path()

# Klasörlerin alfabetik dizilimine sadık kalınmış Türkçe karşılıklar:
# ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
CLASSES = ["Karton", "Cam", "Metal", "Kağıt", "Plastik", "Genel Çöp"]
TARGET_SIZE = (224, 224)

# Her etkileşimde modelin sıfırdan yüklenip sistemi dondurmaması için cache yapısı kullanıyoruz
@st.cache_resource
def load_cached_classifier():
    """
    WasteClassifier sınıflandırıcı nesnesini başlatır ve Streamlit önbelleğine alır.

    Streamlit'in @st.cache_resource dekoratörü sayesinde model belleğe yalnızca
    bir kez yüklenir; bu sayede her kullanıcı etkileşiminde gereksiz model yükleme
    ve gecikmeler engellenir.

    Returns:
        WasteClassifier: Başlatılmış ve bellekte hazır sınıflandırıcı örneği.
    """
    return WasteClassifier(model_path=str(MODEL_PATH), class_names=CLASSES, target_size=TARGET_SIZE)


def main():
    """
    Streamlit kullanıcı arayüzü ana akışı.

    Sayfa düzenini yapılandırır, model yükleme durumunu kontrol eder,
    kullanıcıdan görsel yüklemesini alır, tahmin motorunu çalıştırır ve
    çıkarım sonuçlarını ekranda görüntüler.
    """
    # Tarayıcı sekmesi başlığı ve sayfa düzeni ayarları
    st.set_page_config(page_title="AI Atık Sınıflandırma", page_icon="♻️", layout="centered")
    
    # Başlık ve bilgilendirme metni
    st.title("♻️ Akıllı Hazne Atık Sınıflandırma Sistemi")
    st.markdown("Eğitilen **MobileNetV2** modelini kullanarak atık türünü gerçek zamanlı tespit edin.")
    st.write("---")

    # Önbelleğe alınmış sınıflandırıcı modelini yükle
    try:
        classifier = load_cached_classifier()
    except Exception as e:
        # Model yükleme hatası durumunda kullanıcıya bilgilendirme göster ve dur
        st.error(f"Model yüklenirken kritik hata: {e}")
        st.info("Lütfen model dosyasının doğru dizinde ve doğru adda olduğundan emin olun.")
        return

    # Dosya Yükleme Alanı — Desteklenen formatlar: JPG, JPEG, PNG
    uploaded_file = st.file_uploader("Siyah arka planda çekilmiş atık fotoğrafını yükleyin...", type=["jpg", "jpeg", "png"])

    # Kullanıcı bir dosya yüklediyse analiz adımlarını başlat
    if uploaded_file is not None:
        # Görseli RAM'e alıyoruz
        image = Image.open(uploaded_file)
        
        # Ekranı iki eşit sütuna böl (Sol: Görsel önizleme, Sağ: Analiz sonuçları)
        col1, col2 = st.columns(2)
        
        with col1:
            # Kullanıcının yüklediği görseli önizle
            st.image(image, caption="Yüklenen Nesne", use_container_width=True)
            
        with col2:
            st.subheader("Model Analizi")
            
            # Tahmin işlemi devam ederken yükleniyor animasyonu göster
            with st.spinner("Model tahmin yürütüyor..."):
                try:
                    # Tahmin motorunu çalıştır
                    prediction, confidence = classifier.predict(image)
                    
                    # Sonuç Ekranı — Tespit edilen sınıf ve yüzde güven skoru
                    st.success(f"**Tespit Edilen Sınıf:** {prediction}")
                    st.metric(label="Güven Skoru", value=f"% {confidence:.2f}")
                    
                    # Kullanıcı yönlendirme kalkanı — Hangi geri dönüşüm kutusuna atılmalı
                    st.info(f"Yapay zeka bu nesnenin **{prediction}** kutusuna atılmasını öneriyor.")
                    
                except Exception as e:
                    # Çıkarım sırasında oluşabilecek hataları yakala ve arayüzde bildir
                    st.error(f"Tahmin işlemi esnasında bir hata oluştu: {e}")

if __name__ == "__main__":
    main()
