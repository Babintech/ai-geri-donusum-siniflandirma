# Akıllı Kutu — AI Tabanlı Atık Sınıflandırma Sistemi

Derin öğrenme kullanarak atıkları otomatik sınıflandıran bir yapay zeka projesi. Kapalı, siyah arka planlı hazne ortamında farklı atık türlerini yüksek doğrulukla tanımlayarak geri dönüşüm sürecini destekler.

## Genel Bakış

**Akıllı Kutu**, atık yönetimini ve geri dönüşümü desteklemek için geliştirilmiş bir derin öğrenme uygulamasıdır. Proje, MobileNetV2 tabanlı transfer öğrenme kullanarak atıkları 6 ana kategoriye sınıflandırır:

- 📦 **Karton** (Cardboard)
- 🪟 **Cam** (Glass)  
- 🔩 **Metal** (Metal)
- 📄 **Kağıt** (Paper)
- 🛢️ **Plastik** (Plastic)
- 🗑️ **Genel Çöp** (Trash)

Streamlit üzerinde geliştirilen web arayüzü, gerçek zamanlı görüntü sınıflandırması yaparak kullanıcıların atıklarını doğru kutulara yönlendirmesini sağlar.

## Projenin Geçmişi

Bu proje, **Babintech'in üç kurucu üyesi tarafından üniversite bitirme projesi olarak geliştirilmiştir**:
- **Efe Can Kara** — Model geliştirme ve eğitim
- **Yiğit Altundağ** — Streamlit arayüzü ve deployment
- **Sınıf Katkısı** — Veri seti derlemesi

Projenin başlangıçta akademik bir araştırma ve prototipleme amacı vardı. Daha sonra, Babintech organizasyonuna transfer edilen proje, profesyonel mühendislik standartlarına uygun şekilde bakım ve geliştirilmeye devam etmektedir.

Proje geçmişi ve orijinal katkılar Git commit geçmişinde korunmaktadır. Mevcut bakım ve geliştirmeler Babintech tarafından yapılmaktadır.

## Problem

Atık yönetiminde önemli bir meydan okuma, farklı atık türlerinin doğru biçimde sınıflandırılması ve ayrılmasıdır. Manuel sınıflandırma işlemi:
- Yavaş ve hata eğilimlidir
- İnsan müdahalesi gerektirir
- Tutarsız sonuçlar verebilir

**Akıllı Kutu**, bu süreci otomatikleştirerek, geri dönüşüm verimliliğini artırır ve işlemi daha güvenilir kılar.

## Özellikler

- ✅ **Gerçek zamanlı sınıflandırma**: Kullanıcının yüklediği görüntü anında işlenir
- ✅ **Yüksek doğruluk**: Eğitim veri seti üzerinde ~%93 doğruluk bandı
- ✅ **Streamlit web arayüzü**: Kullanımı kolay ve erişilebilir
- ✅ **Canlı deployment**: Streamlit Community Cloud üzerinde barındırılır
- ✅ **Transfer öğrenme**: MobileNetV2 tabanlı verimli model
- ✅ **Kontrollü ortam optimizasyonu**: Siyah zemin üzerinde eğitilmiş, kapalı hazne için tasarlandı

## Mimari

### Sistem Mimarisi

```
[Girdi: Atık Görüntüsü]
         ↓
[Görüntü Ön İşleme: Boyutlandırma + Normalizasyon]
         ↓
[MobileNetV2 + Sınıflandırma Başlığı]
         ↓
[Tahmin + Güven Skoru]
         ↓
[Kullanıcı Sonucu]
```

### Model Mimarisi

| Bileşen | Detay |
|---------|-------|
| **Omurga (Backbone)** | MobileNetV2 (ImageNet ağırlıkları) |
| **Girdi Boyutu** | 224 × 224 × 3 (RGB) |
| **Çıktı Başlığı** | GlobalAveragePooling2D → Dropout(0.5) → Dense(6, softmax) |
| **Model Dosyası** | `model/akilli_kutu_model.keras` |
| **Format** | Keras 3 (.keras) |

### Eğitim Stratejisi

1. **Aşama 1 — Omurga Dondurulmuş Eğitim**
   - MobileNetV2'nin ön eğitilmiş ağırlıkları kilitli
   - Sadece başlık katmanları eğitilir

2. **Aşama 2 — Fine-tuning**
   - Son ~55 katman açılır
   - Çok düşük öğrenme hızı (1e-5) ile ince ayar
   - Model, veri setine daha iyi uyum sağlar

## Veri Seti

### Kaynak ve Derleme

Veri seti üç ana kaynaktan derlenmiştir:
1. **Yerel Sınıf Veri Seti** (Google Drive) — Akademik ortamda derlenen orijinal veri
2. **Kaggle Atık Sınıflandırma Veri Setleri** — Genel atık sınıflandırması veri setleri
3. **Ek Kaggle Desteği** — Mehmet Yıldız tarafından sağlanan ek veri

### Özellikleri

- **Sınıf dengesi**: Tüm 6 sınıf dengeli dağılım
- **Toplam görüntü**: Sınıf başına maksimum ~1500 görüntü
- **Ön işleme**: Rembg ile arka plan temizleme, siyah zemin simülasyonu

Detaylı veri seti bilgisi için bkz. [`data/README.md`](data/README.md)

## Veri Ön İşleme

Eğitim ve inference sırasında uygulanan ön işleme adımları:

```
Orijinal Görüntü
    ↓
[Arka Plan Temizleme — Rembg]
    ↓
[Siyah Zemin Simülasyonu]
    ↓
[Resize: 224×224]
    ↓
[Normalizasyon: / 255.0]
    ↓
[Batch İşleme]
    ↓
Model Girdisi
```

## Model

### Eğitim Sonuçları

Eğitim sürecinde aşağıdaki performans elde edilmiştir:

| Metrik | Değer |
|--------|-------|
| **Doğruluk (Accuracy)** | ~%93 |
| **Eğitim Ortamı** | Google Colab (GPU) |
| **Dataset** | Master Dataset (~9000 görüntü) |

**Not**: Kesin metrik değerleri `notebooks/training_experiments.ipynb` not defterinin çıktısında kaydedilmiştir.

### Model Yönetimi

- **Dosya konumu**: `model/akalli_kutu_model.keras`
- **Boyut**: Yaklaşık 13 MB (MobileNetV2 + başlık)
- **Framework**: TensorFlow 2.16+
- **Python**: 3.11+

## Değerlendirme

Model değerlendirmesi aşağıdaki yöntemler kullanılarak yapılmıştır:

- **Karmaşıklık Matrisi (Confusion Matrix)**: Sınıf bazlı tahmin doğruluğu
- **Sınıflandırma Raporu**: Precision, Recall, F1-score
- **Doğruluk Bandı**: Genel model performansı

Tüm değerlendirme sonuçları, eğitim not defterinde kaydedilmiş ve görselleştirilmiştir.

## Sonuçlar

### Performans Metrikleri

Notebook çalıştırılırken şu sonuçlar elde edilmiştir:

- **Genel Doğruluk**: ~%93
- **Sınıf Bazlı Performans**: Tüm sınıflar başarılı
- **Karmaşıklık Matrisi**: Not defterinde görselleştirilmiş

### Bilinen Sınırlamalar

Modelin doğruluğunu etkileyen faktörler:

1. **Kontrollü Ortam Bağımlılığı**
   - Siyah zemin üzerinde eğitildi
   - Açık ışık ortamında performans değişebilir

2. **Işık Koşulları**
   - Sabit ışık ortamında optimize edildi
   - Değişken ışık koşullarında hassas

3. **Atık Karmaşıklığı**
   - Temiz, tek materyalli atıklar için optimize
   - Karışık veya belirsiz atıklar daha zor

4. **Domain Bias**
   - Akademik test ortamı için özel tasarım
   - Gerçek dünya çeşitliliği tam olarak temsil etmeyebilir

## Demo

### Canlı Uygulama

Streamlit Community Cloud üzerinde çalışan demo uygulama:

🔗 **[AI Atık Sınıflandırma Demo](https://final-project-recycle-classification-p7qvxat9uoyxzkzjazn5ib.streamlit.app/)**

### Video Tanıtım

Proje ve model tanıtım videosu:

🎥 **[YouTube — Akıllı Kutu Tanıtım](https://youtu.be/TyzawMWt5Sc?si=ukQ2pQva0srhl850)**

## Kurulum

### Gereksinimler

- **Python**: 3.11+
- **pip**: Güncel sürüm
- **Disk**: En az 500 MB (model + bağımlılıklar)

### Lokal Kurulum

1. **Repository'yi klonla**:
   ```bash
   git clone https://github.com/Babintech/ai-geri-donusum-siniflandirma.git
   cd ai-geri-donusum-siniflandirma
   ```

2. **Sanal ortam oluştur ve etkinleştir**:
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Bağımlılıkları yükle**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Model dosyası kontrolü**:
   ```bash
   # Model dosyası model/akilli_kutu_model.keras konumunda olmalı
   ls -la model/
   ```

### Google Colab Kurulum

Not defteri, Google Colab üzerinde doğrudan çalışacak şekilde hazırlanmıştır:

1. [`notebooks/training_experiments.ipynb`](notebooks/training_experiments.ipynb) dosyasını açın
2. **"Open in Colab"** düğmesine tıklayın
3. Hücreleri sırayla çalıştırın
4. Drive bağlantısı ve Kaggle yapılandırması talimatları not defterinde belirtilmiştir

## Kullanım

### Streamlit Uygulaması

Streamlit web arayüzünü çalıştır:

```bash
streamlit run app.py
```

Uygulama tarayıcıda açılacak (varsayılan: `http://localhost:8501`)

**Kullanım adımları**:
1. Siyah arka planlı atık fotoğrafını yükle
2. Model analizi otomatik olarak çalışır
3. Sınıflandırma sonucu ve güven skoru görüntülenir

### Programatik Kullanım

```python
from PIL import Image
from classifier import WasteClassifier

# Sınıflandırıcı yükle
classifier = WasteClassifier(
    model_path="model/akilli_kutu_model.keras",
    class_names=["Karton", "Cam", "Metal", "Kağıt", "Plastik", "Genel Çöp"],
    target_size=(224, 224)
)

# Görüntü tahmin et
image = Image.open("waste_sample.jpg")
prediction, confidence = classifier.predict(image)

print(f"Sınıf: {prediction}, Güven: {confidence:.2f}%")
```

### Eğitim ve Değerlendirme

Modeli yeniden eğitmek veya değerlendirmek için not defteri kullanılır:

```bash
# Google Colab'da: notebooks/training_experiments.ipynb
```

Not defteri aşağıdaki bölümleri içerir:
- Veri seti kurulumu
- Ön işleme ve artırma
- Model eğitimi
- Değerlendirme
- Sonuç görselleştirmesi

## Proje Yapısı

```
ai-geri-donusum-siniflandirma/
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI
├── .gitignore                      # Git ignore kuralları
├── app.py                          # Streamlit web uygulaması
├── classifier.py                   # Sınıflandırıcı sınıfları
├── data/
│   └── README.md                   # Veri seti dokümantasyonu
├── dataset/
│   ├── cardboard/                  # Karton görüntüleri
│   ├── glass/                      # Cam görüntüleri
│   ├── metal/                      # Metal görüntüleri
│   ├── paper/                      # Kağıt görüntüleri
│   ├── plastic/                    # Plastik görüntüleri
│   └── trash/                      # Çöp görüntüleri
├── model/
│   └── akalli_kutu_model.keras     # Eğitilmiş model
├── notebooks/
│   └── training_experiments.ipynb  # Eğitim ve deney not defteri
├── src/
│   └── inference/                  # Inference yardımcıları
├── tests/
│   ├── test_inference.py           # Inference testleri
│   └── test_preprocessing.py       # Ön işleme testleri
├── README.md                       # Bu dosya
├── CONTRIBUTING.md                 # Katkıda bulunma rehberi
├── LICENSE                         # MIT Lisansı
├── requirements.txt                # Python bağımlılıkları
└── runtime.txt                     # Python sürümü (Streamlit Cloud)
```

## Tekrarlanabilirlik

### Ortam Kurulumu

Tüm ortamlarda tutarlı sonuçlar için:

```bash
# Sanal ortam oluştur
python -m venv .venv
source .venv/bin/activate  # veya .venv\Scripts\activate (Windows)

# Kesin sürümlerde yükle
pip install -r requirements.txt
```

### Dataset Hazırlama

Dataset otomatik olarak `dataset/` klasöründe mevcuttur:

```python
# Not defterinde
dataset_path = "dataset"
# 6 sınıf klasörü otomatik yüklenir
```

### Training/Evaluation Süreci

Aynı sonuçlar elde etmek için:

1. Not defterini (`notebooks/training_experiments.ipynb`) açın
2. Hücreleri sırayla çalıştırın
3. Random seed ayarı yapılmıştır
4. Colab ortamında (GPU) çalıştırılması önerilir

### Gerekli Artifact'ler

- ✅ Model dosyası: `model/akalli_kutu_model.keras` (Git LFS ile)
- ✅ Dataset: `dataset/` klasörü (versiyon kontrollü)
- ✅ Not defteri: `notebooks/training_experiments.ipynb` (çıktı korunur)

## Gelecek Çalışmalar

Potansiyel iyileştirme alanları:

- **Model Performansı**: Daha ileri mimariler (EfficientNet, Vision Transformers) test edilebilir
- **Domain Adaption**: Açık ortam ve değişken ışık koşulları için fine-tuning
- **Real-time Deployment**: Edge cihazlara model aktarımı (TensorFlow Lite, ONNX)
- **Ensemble Modeller**: Çoklu model kombinasyonu güvenilirliği artırabilir
- **Sınıf Genişleme**: Yeni atık kategorileri ekleme
- **Inference Optimizasyonu**: Model quantization ve compression
- **Multi-modal Input**: Video veya 3D kameralardan gelen veri destekleme

## Katkıda Bulunanlar

### Orijinal Bitirme Projesi Katkıları

| Katkılayan | Rol |
|-----------|-----|
| **Efe Can Kara** | Model geliştirme, eğitim, değerlendirme |
| **Yiğit Altundağ** | Streamlit arayüzü, deployment |
| **Sınıf Katkısı** | Veri seti derlemesi |
| **Mehmet Yıldız** | Ek Kaggle veri seti desteği |

### Babintech Bakım ve Geliştirme

Proje, Babintech GitHub organizasyonuna transfer edildikten sonra, profesyonel mühendislik standartlarına uygun şekilde bakım ve geliştirilmektedir.

## Katkıda Bulunma

Proje hakkında önerileri veya katkılı olmak isterseniz, lütfen [`CONTRIBUTING.md`](CONTRIBUTING.md) dosyasına bakın.

## Lisans

Bu proje **MIT Lisansı** altında yayımlanmıştır.

Lisans metni: [`LICENSE`](LICENSE)

---

**Not**: Bu proje, Babintech'in AI ve mühendislik portföyünün bir parçasıdır. Sorular, öneriler veya katkılar için GitHub Issues'yi kullanabilirsiniz.
