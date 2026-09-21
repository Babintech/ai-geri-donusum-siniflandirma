# Katkıda Bulunma Rehberi

Proje hakkında önerileri ve katkıları için teşekkürler. Bu rehberi lütfen okuyun.

## Davranış Kuralları

Tüm katkılıyanlardan profesyonel ve saygılı bir ortam sağlamalarını bekliyoruz. Taciz, ayrımcılık veya disrespekt tolerans görmez.

## Katkı Süreci

### 1. Issue Açma

Bir hata bulduysanız veya yeni bir özellik öneriliyorsanız:

1. Mevcut issues'leri kontrol edin (benzer konu zaten açılmış mı?)
2. Açık ve tanımlayıcı bir başlık kullanın
3. Detaylı açıklama ekleyin:
   - Neler başarısız oldu / ne önerildi?
   - Hangi ortamda?
   - Tekrarlama adımları (varsa)

### 2. Branch Oluşturma

Issues çözmek veya özellik eklemek için:

```bash
# Ana branch'in güncel olduğundan emin ol
git checkout main
git pull origin main

# Açıklayıcı bir branch adı ile yeni branch oluştur
git checkout -b feature/feature-name
# veya
git checkout -b fix/bug-name
```

**Branch adlandırması kuralları**:
- `feature/` — Yeni özellikler
- `fix/` — Hata düzeltmeleri
- `docs/` — Dokümantasyon
- `refactor/` — Kod yeniden yapılandırması
- `test/` — Test ekleme/güncelleme

### 3. Geliştirme

```bash
# Sanal ortam oluştur ve etkinleştir
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Değişikliklerinizi yapın
# ... kodunuzu yazın ...

# Testleri çalıştır
python -m pytest tests/

# Kodu kontrol et
python -m flake8 --max-line-length=100 src/ tests/ app.py classifier.py
```

### 4. Commit Yapma

Anlamlı ve odaklı commit'ler yapın:

```bash
# Değişiklikleri stage et
git add .

# Açıklayıcı commit mesajı ile commit yap
git commit -m "Fix: Görüntü ön işlemede normalizasyon hatası düzeltildi"
```

**Commit mesajı kuralları**:
- Başlık maksimum 50 karakter
- Türkçe veya İngilizce (tutarlı olun)
- Başlık: `Type: Açıklama` formatı
  - `Fix:` — Hata düzeltme
  - `Feature:` — Yeni özellik
  - `Docs:` — Dokümantasyon
  - `Refactor:` — Kod yeniden yapılandırması
  - `Test:` — Test ekleme
  - `Chore:` — Build, config, vb.

### 5. Pull Request Açma

```bash
# Branch'inizi remote'a push edin
git push origin feature/feature-name

# GitHub üzerinde Pull Request oluşturun
```

**PR açıklaması şunları içermeli**:
- Hangi issue'yu çözdüğü (#123)
- Değişikliklerin özeti
- Test etme talimatları (varsa)
- Ekran görüntüleri (UI değişikliği varsa)

Örnek:

```markdown
## Açıklama
Görüntü ön işlemede normalizasyon hatası düzeltilmiştir.

## Çözdüğü Issue
Closes #42

## Değişiklikler
- `classifier.py` 'de normalizasyon hesaplaması düzeltildi
- Test case'leri güncellendi

## Test Edildi
- [x] Lokal ortamda test edildi
- [x] Test suite geçti
- [x] Streamlit uygulaması çalışıyor
```

### 6. Review ve Merge

- Kod review yapılacak
- Öneriler yapılabilir
- Onaylandıktan sonra main branch'e merge edilir

## Değiştirilemez Dosyalar

Aşağıdaki dosyalar proje geçmişinin bir parçası olduğundan doğrudan değiştirilmez:

- `dataset/` — Veri seti (yalnızca genişletilir)
- `notebooks/training_experiments.ipynb` — Orijinal eğitim not defteri
- `model/akalli_kutu_model.keras` — Eğitilmiş model

**Yeni deneyler için**: `experiments/` veya benzeri ayrı klasör kullanın

## Proje Standartları

### Kod Kalitesi

- Anlaşılır ve okunabilir kod yazın
- Gereksiz yere karmaşıklaştırmayın
- Yorum yazın (Türkçe tercih edilir), ancak yalnızca gerekli yerlerde

Örnek:

```python
def preprocess_image(image: Image.Image) -> np.ndarray:
    """Görüntüyü MobileNetV2 girdisine hazırla."""
    # PNG görselindeki alfa kanalını RGB'ye dönüştür
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    image = image.resize((224, 224))
    img_array = img_to_array(image) / 255.0
    return np.expand_dims(img_array, axis=0)
```

### Dokümantasyon

- Değişiklikler README veya ilgili dokümantasyonu etkiliyorsa, güncelle
- Yeni fonksiyon veya sınıf ekliyorsanız, docstring ekle
- Türkçe dokümantasyonda gramatikal ve terminolojik tutarlılık sağla

### Testler

- Yeni özellik ekleniyorsa, test case'i de ekle
- Mevcut testler geçmeli
- Bütün modeli yeniden eğiten test ekleme

## Babintech AI Geliştirme Prensibi

Babintech'te AI tabanlı geliştirmede şu prensipler uygulanır:

**Düşün → Dene → Sor → Doğrula → Açıkla**

1. **Düşün**: Sorunu anla, çözümü planla
2. **Dene**: Deney yap, kod yaz, test et
3. **Sor**: Emin değilsen, soru sor (Issues, Discussions)
4. **Doğrula**: Sonuçların doğruluğunu kontrol et
5. **Açıkla**: Değişiklikleri açık şekilde dokümante et

### LLM/AI Araçları Kullanımı

LLM (ChatGPT, Claude, Copilot vb.) veya AI araçları kullanabilirsiniz. Ancak:

- ✅ Üretilen kod ve açıklamaları **anlamalısınız**
- ✅ Kodun doğruluğunu **test etmelisiniz**
- ✅ PR review'de **açıklayabilmelisiniz**
- ❌ Anlamadığınız kodu merge etmeyin
- ❌ Doğrulamasız AI çıktısı kullanmayın

## Geliştirme Ortamı Kurulumu

```bash
# Repository'yi klonla
git clone https://github.com/Babintech/ai-geri-donusum-siniflandirma.git
cd ai-geri-donusum-siniflandirma

# Sanal ortam oluştur
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# (Opsiyonel) Geliştirme bağımlılıkları
pip install pytest flake8
```

## Testleri Çalıştırma

```bash
# Tüm testleri çalıştır
python -m pytest tests/

# Spesifik test dosyasını çalıştır
python -m pytest tests/test_inference.py

# Verbose mode
python -m pytest tests/ -v

# Coverage raporu
python -m pytest tests/ --cov=src --cov-report=html
```

## Streamlit Uygulamasını Test Etme

```bash
# Uygulamayı çalıştır
streamlit run app.py

# Tarayıcıda açılır: http://localhost:8501
# Değişiklikleri test et
```

## Sıkça Sorulan Sorular (SSS)

### Modeli yeniden eğitebilir miyim?

Evet, ancak:
- `notebooks/training_experiments.ipynb` not defterini kullanın
- Yalnızca gerçek ihtiyaç varsa
- PR'de neden eğitilmiş olduğunu açıklayın

### Yeni bağımlılık ekleyebilir miyim?

Evet, ancak:
- PR açıklamasında gerekçesini belirt
- `requirements.txt` güncellenmelidir
- Paket boyutuna dikkat et (Streamlit Cloud limitleri)

### Model dosyasını değiştirebilir miyim?

Dikkat edin:
- Mevcut `app.py` ile uyumlu olmalı
- Test edilmiş olmalı
- PR'de test sonuçlarını ekle

### Main branch'e doğrudan push edebilir miyim?

**HAYIR** — Main branch korumalı olup, sadece review edilen PR'ler merge edilebilir.

## Desteği Alma

Sorularınız varsa:

- GitHub Issues'i kullanın (herkese açık soru için)
- GitHub Discussions (tartışma ve fikir paylaşımı için)
- Code review sırasında soru sorun

## Teşekkür

Projeye katkı veren herkese teşekkür ederiz! 🙏

---

**Son Not**: Bu proje Babintech'in academic ve professional geçmişini yansıtır. Geçmişini korurken, profesyonel standartlara uygun geliştirmeler yapıyoruz.
