# Veri Seti Dokümantasyonu

## Genel Bilgi

Bu proje, atık sınıflandırması için geliştirilmiş bir derin öğrenme modelini eğitmek amacıyla **dengeli bir veri seti** kullanmaktadır. Veri seti, çeşitli kaynaklardan derlenmiş olup, her sınıfa ait görüntüler siyah zemin üzerinde çekilmiş olarak işlenmiştir.

## Veri Seti Kaynakları

Veri seti aşağıdaki üç ana kaynaktan derlenmiştir:

1. **Yerel Sınıf Veri Seti** (Google Drive)
   - Akademik ortamda derlenen orijinal veri seti
   - Doğrudan proje ekibi tarafından toplandı

2. **Kaggle Atık Sınıflandırma Veri Setleri**
   - Birden fazla Kaggle platformu veri seti kullanıldı
   - Genel atık sınıflandırması özellikleri ile uyumludur

3. **Ek Kaggle Veri Seti Desteği**
   - Contributor: **Mehmet Yıldız**

## Sınıf Yapısı

Veri seti aşağıdaki 6 sınıfı içermektedir:

```
dataset/
  ├── cardboard/    (Karton)
  ├── glass/        (Cam)
  ├── metal/        (Metal)
  ├── paper/        (Kağıt)
  ├── plastic/      (Plastik)
  └── trash/        (Genel Çöp)
```

## Veri Seti Özellikleri

- **Toplam görüntü sayısı**: Sınıf başına maksimum ~1500 görüntü
- **Veri dengesi**: Tüm sınıflar dengeli dağılıma sahiptir
- **Görüntü formatı**: JPG
- **Arka plan işleme**: 
  - Rembg kullanılan arka plan temizleme
  - Siyah zemin simülasyonu (black background)
  - Proje özel koşuluğu (kapalı siyah hazne)

## Veri Ön İşleme

Eğitim sırasında uygulanan ön işleme adımları:

1. **Arka Plan Temizleme**
   - Orijinal görüntülerden nesneler izole edilmiş
   - Rembg kütüphanesi kullanılan arka plan kaldırma

2. **Siyah Zemin Simülasyonu**
   - Temizlenmiş nesneler siyah zemin üzerine yerleştirilmiş
   - Kapalı hazne ortamını simüle etmek için tasarlanmıştır

3. **Veri Artırma (Data Augmentation)**
   - Rotation: Rastgele döndürme
   - Shift: Rastgele kaydırma
   - Zoom: Rastgele yakınlaştırma
   - Fill mode: `constant` (siyah zemin korunumu)
   - Rescale: 1/255 normalizasyonu

4. **Boyut Standardizasyonu**
   - Tüm görüntüler 224×224 piksel olarak yeniden boyutlandırılmıştır
   - MobileNetV2 model girdisine uygun

## Eğitim/Doğrulama/Test Ayrımı

Proje not defterinde (`notebooks/training_experiments.ipynb`) bölüm yapısında train/validation/test ayrımı açıklanmaktadır.

## Lisans ve Yeniden Dağıtım

**ÖNEMLİ NOT**: Veri seti üçüncü taraf kaynakları (özellikle Kaggle) içermektedir.

- **Yerel veri seti**: Akademik araştırma için kullanılabilir
- **Kaggle veri setleri**: Kaggle'ın Lisans Şartlarına tabi olup, bağlantılı kaynakları incelemelisiniz

Ticari veya üretim amaçlı kullanım öncesinde:
- Orijinal veri kaynakları için lisans şartlarını kontrol edin
- Kaggle platformu lisans hükümlerine uyun

## Verinin Nasıl Edinileceği

### Google Colab Ortamında

Not defteri (`notebooks/training_experiments.ipynb`) Colab üzerinde çalışacak şekilde tasarlanmıştır:

```python
# Google Drive bağlantısı
from google.colab import drive
drive.mount('/content/drive')

# Yerel veri seti yolu
drive_dataset_path = '/content/drive/My Drive/...'

# Kaggle indirme adımları not defterinde belirtilmiştir
```

### Lokal Ortamda

Veri seti bu repository'nin `dataset/` klasöründe mevcuttur:

```bash
git clone <repository-url>
cd ai-geri-donusum-siniflandirma
# dataset/ klasörü hazır
```

## Bilinen Sınırlamalar

- **Kapalı ortam şartı**: Modeli eğitmek için siyah zemin simülasyonu yapılmıştır, açık ortam performansı sınırlı olabilir
- **Işık koşulları**: Kontrollü ortam koşullarında eğitilmiş, değişken ışık koşullarında performans değişebilir
- **Atık karmaşıklığı**: Karışık veya belirsiz atıklar (örn. çok materyalli ürünler) sınıflandırması zorlaştırabilir
- **Domain bias**: Veri seti yapısı proje özeline optimize edilmiştir

## İletişim

Veri seti hakkında sorularınız için:
- İlgili contributor'lara GitHub Issues üzerinden ulaşabilirsiniz
- Not defterindeki bölümlerde detaylı açıklamalar mevcuttur
