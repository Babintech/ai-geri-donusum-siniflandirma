# Veri Seti

## Kaynaklar

Veri seti aşağıdaki kaynaklardan derlenmiştir:

1. Google Drive üzerinden sınıf tarafından derlenen yerel veri seti
2. Birden fazla Kaggle atık sınıflandırma veri seti
3. Mehmet Yıldız'ın sağladığı ek Kaggle veri seti

Kaggle kaynaklarının kimlikleri ve lisans koşulları repository içinde ayrıntılı
olarak listelenmemiştir. Yeniden dağıtım veya ticari kullanım öncesinde orijinal
kaynakların güncel şartları incelenmelidir.

## Sınıflar ve Klasörler

```text
dataset/
├── cardboard/
├── glass/
├── metal/
├── paper/
├── plastic/
└── trash/
```

Notebook, her sınıf için en fazla 1500 örnek kullanılacak şekilde dengeleme
uygular. Bu bilgi bir üst sınırdır; sınıfların tam dağılımı notebook çalıştırma
çıktısına göre değişebilir.

## Ön İşleme

Notebook'ta görülen pipeline şu adımları içerir:

- `rembg` ile arka plan temizleme
- Siyah zemin simülasyonu
- Rotation, shift ve zoom ile data augmentation
- `fill_mode='constant'` ile siyah zemin korunumu
- `224x224` boyutlandırma
- `1/255` normalizasyonu

Streamlit inference sırasında görüntü RGB'ye dönüştürülür, `224x224` boyutuna
getirilir ve `1/255` ile normalize edilir.

## Eğitim ve Değerlendirme

Notebook, train ve validation generator'ları kullanır. Eğitim sırasında
`val_accuracy` izlenir; final değerlendirme hücresi validation subset'i
üzerinden confusion matrix ve classification report üretir. Kayıtlı notebook
çıktısında final raporun sayısal değerleri bulunmadığından burada ek metrik
üretilmemiştir.

## Sınırlamalar

- Veri seti siyah arka plan ve kontrollü çekim koşullarına göre hazırlanmıştır.
- Karışık materyalli atıklar sınıflandırma açısından daha zor olabilir.
- Üçüncü taraf veri setlerinin lisans ve yeniden dağıtım hakları ayrıca
  doğrulanmalıdır.
