# Akıllı Kutu — AI Tabanlı Atık Sınıflandırma Sistemi

Akıllı Kutu, yüklenen atık görüntülerini altı sınıfa ayıran MobileNetV2 tabanlı bir
prototiptir. Proje, geri dönüşüm süreçlerinde otomatik atık sınıflandırmasının
uygulanabilirliğini araştırmak ve göstermek amacıyla geliştirilmiştir.

## Genel Bakış

Streamlit arayüzü bir görüntü yüklenmesini bekler, görüntüyü modelin giriş biçimine
dönüştürür ve tahmin edilen sınıf ile confidence score değerini gösterir. Uygulama
web kamerası veya sürekli video akışı üzerinde inference yapmaz.

Desteklenen sınıflar:

- Karton (`cardboard`)
- Cam (`glass`)
- Metal (`metal`)
- Kağıt (`paper`)
- Plastik (`plastic`)
- Genel çöp (`trash`)

## Projenin Geçmişi

Proje, Babintech'in üç kurucu üyesi tarafından üniversite bitirme projesi olarak
geliştirildi. Daha sonra Babintech GitHub organizasyonuna transfer edildi ve
bakımı burada sürdürülmeye devam ediyor.

Orijinal katkılar:

- **Efe Can Kara:** model geliştirme, eğitim ve değerlendirme
- **Yiğit Altundağ:** Streamlit arayüzü ve deployment çalışmaları
- **Mehmet Yıldız:** projeye ek veri seti yüklenmesi

Mehmet Yıldız'ın GitHub contributor listesinde görünmemesiyle ilgili teknik
inceleme [CONTRIBUTING.md](CONTRIBUTING.md) ve bu repository'nin Git geçmişinde
belgelenmiştir. Contributor listesi, proje dokümantasyonundaki tarihsel katkı
attribution'ından ayrı bir GitHub görünümüdür.

## Mimari ve Model

```text
Yüklenen görüntü
        |
RGB dönüşümü, 224x224 resize, /255 normalizasyonu
        |
MobileNetV2 + GlobalAveragePooling2D + Dropout(0.5)
        |
Dense(6, softmax)
        |
Sınıf ve confidence score
```

- Girdi boyutu: `224x224x3`
- Backbone: ImageNet ağırlıklı MobileNetV2
- Eğitim: önce dondurulmuş backbone, ardından son katmanların fine-tuning işlemi
- Fine-tuning öğrenme hızı: notebook kodunda `1e-5`
- Model dosyası: `model/akilli_kutu_model.keras`

## Veri Seti ve Ön İşleme

Veri seti yerel sınıf verileri ile Kaggle kaynaklarından derlenmiştir. Notebook,
her sınıf için en fazla 1500 örnek kullanılacak şekilde dengeleme uygular.
Bu ifade bir üst sınırdır; tüm sınıfların tam olarak aynı sayıda örneğe sahip
olduğu anlamına gelmez.

Eğitim pipeline'ında görülen başlıca adımlar:

- **Dosya konumu**: `model/akilli_kutu_model.keras`
- **Boyut**: Yaklaşık 13 MB (MobileNetV2 + başlık)
- **Framework**: TensorFlow 2.16+
- **Python**: 3.11+

Sınıf klasörleri ve veri kaynakları hakkında ayrıntılar için
[data/README.md](data/README.md) dosyasına bakın. Üçüncü taraf veri setlerinin
lisans ve yeniden dağıtım koşulları ayrıca kontrol edilmelidir.

## Değerlendirme ve Sonuçlar

Notebook kodu eğitim sırasında `val_accuracy` metriğini izliyor ve validation
subset'i üzerinden confusion matrix ile classification report üretiyor.
Notebook açıklamasında fine-tuning sonrasında yaklaşık `%93+` seviyesinde bir
sonuç raporlanıyor. Bu değer, notebook'ta raporlanan deney sonucudur; bağımsız
bir test seti accuracy değeri olarak adlandırılmamıştır. Notebook'un kayıtlı
çıktılarında final classification report'un sayısal çıktısı bulunmadığı için
precision, recall ve F1 için ek kesin değer verilmemektedir.

Proje demosunda veri seti dışında seçilen çeşitli atık görselleriyle yapılan
denemelerde model doğru sınıflandırmalar üretmiş, bu örneklerde confidence score
değerleri yaklaşık `%92-%99` aralığında gözlemlenmiştir. Bu değerler kontrollü
demo gözlemleridir; bağımsız bir test seti üzerindeki accuracy metriği olarak
değerlendirilmemelidir.

### Bilinen Sınırlamalar

- Model siyah arka plan ve kontrollü ışık koşullarına göre hazırlanmıştır.
- Karışık veya birden fazla materyal içeren atıklar daha zor sınıflandırılabilir.
- Notebook ve demo sonuçları, gerçek dünya performansının kapsamlı bir ölçümü
  değildir.
- Sınıflar ve veri kaynakları, gerçek dünyadaki tüm atık çeşitliliğini temsil etmez.

## Demo

- [Streamlit Community Cloud uygulaması](https://final-project-recycle-classification-p7qvxat9uoyxzkzjazn5ib.streamlit.app/)
- [Proje tanıtım videosu](https://youtu.be/TyzawMWt5Sc?si=ukQ2pQva0srhl850)

## Kurulum

```bash
git clone https://github.com/Babintech/ai-geri-donusum-siniflandirma.git
cd ai-geri-donusum-siniflandirma
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

Model dosyasının `model/akilli_kutu_model.keras` konumunda bulunduğundan emin
olun. Notebook ile eğitim veya yeniden değerlendirme yapılacaksa ek notebook
bağımlılıkları ve Google Colab/Drive adımları notebook içinde takip edilmelidir.

## Kullanım

Streamlit uygulamasını başlatın:

```bash
streamlit run app.py
```

Ardından siyah arka planlı bir atık görüntüsü yükleyin. Uygulama, yüklenen
görüntü üzerinde sınıflandırma yapar ve sonucu confidence score ile birlikte
gösterir.

Programatik kullanım:

```python
from PIL import Image
from classifier import WasteClassifier

classifier = WasteClassifier(
    model_path="model/akilli_kutu_model.keras",
    class_names=["Karton", "Cam", "Metal", "Kağıt", "Plastik", "Genel Çöp"],
)

prediction, confidence = classifier.predict(Image.open("waste_sample.jpg"))
print(prediction, confidence)
```

### Testleri Çalıştırma

Birim testleri ve ön işleme kontrollerini çalıştırmak için:

```bash
# Pytest ile tüm testleri çalıştır
pytest tests/ -v

# Söz dizimi ve import doğrulaması
python -m py_compile app.py classifier.py src/inference/classifier.py
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

```text
.
├── .github/workflows/ci.yml
├── app.py
├── classifier.py                 # src.inference için geriye dönük uyumluluk katmanı
├── data/README.md
├── dataset/
│   ├── cardboard/                  # Karton görüntüleri
│   ├── glass/                      # Cam görüntüleri
│   ├── metal/                      # Metal görüntüleri
│   ├── paper/                      # Kağıt görüntüleri
│   ├── plastic/                    # Plastik görüntüleri
│   └── trash/                      # Çöp görüntüleri
├── model/
│   └── akilli_kutu_model.keras     # Eğitilmiş model
├── notebooks/
│   └── training_experiments.ipynb  # Eğitim ve deney not defteri
├── src/
│   └── inference/                  # Inference yardımcıları
├── tests/
├── CONTRIBUTING.md
├── LICENSE
├── requirements.txt
├── requirements-dev.txt
└── runtime.txt
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

- ✅ Model dosyası: `model/akilli_kutu_model.keras` (Git LFS ile)
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

Katkı akışı ve GitHub attribution incelemesi için
[CONTRIBUTING.md](CONTRIBUTING.md) dosyasını okuyun.

## Lisans

Proje [MIT License](LICENSE) ile yayımlanmıştır. Veri setlerindeki üçüncü taraf
içerikler için ilgili kaynakların lisans koşulları geçerlidir.
