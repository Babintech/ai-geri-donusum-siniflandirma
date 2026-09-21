# Katkıda Bulunma

Bu repository, küçük bir engineering ekibi tarafından sürdürülen bir bitirme
projesidir. Katkıların odaklı, anlaşılır ve doğrulanabilir olması beklenir.

## Çalışma Akışı

```text
Issue → Branch → Geliştirme → Test → Pull Request → Review → Merge
```

Bir değişikliğe başlamadan önce ilgili issue'yu inceleyin veya gerekliyse yeni
bir issue açın. Normal koşullarda `main` branch'ine doğrudan push yapmayın.

## Branch Kullanımı

Branch adı kısa ve amacını açıklayıcı olmalıdır:

- `feature/...` — yeni özellik
- `fix/...` — hata düzeltmesi
- `docs/...` — dokümantasyon
- `refactor/...` — yapılandırma veya kod iyileştirmesi
- `test/...` — test değişiklikleri

## Geliştirme ve Test

Runtime bağımlılıklarını kurmak için:

```bash
python -m venv .venv
pip install -r requirements.txt
```

Test ve lint araçlarını kurmak için:

```bash
pip install -r requirements-dev.txt
```

Kod değişikliğinden sonra en azından şu kontrolleri çalıştırın:

```bash
python -m pytest tests/ -v
python -m flake8 app.py classifier.py src/ tests/
```

Modeli yeniden eğiten veya büyük veri seti indiren testler normal test akışına
eklenmemelidir. Davranış değişiklikleri için hafif ve tekrarlanabilir testler
ekleyin. Streamlit arayüzünde değişiklik varsa `streamlit run app.py` ile
uygulamanın başlatılabildiğini de kontrol edin.

## Commit'ler

Commit'ler tek bir amaca odaklanmalı ve ne değiştiğini anlatmalıdır. Büyük,
ilgisiz değişiklikleri aynı commit'te birleştirmeyin.

## Pull Request

PR açıklaması şu soruları yanıtlamalıdır:

- Ne değişti?
- Neden değişti?
- Nasıl test edildi?
- Davranış veya dokümantasyon nasıl etkilendi?

UI değişikliklerinde ekran görüntüsü, hata düzeltmelerinde tekrarlama ve
doğrulama adımları ekleyin.

## AI Destekli Geliştirme

Babintech çalışma prensibi:

**Düşün → Dene → Sor → Doğrula → Açıkla**

AI ve LLM araçları kullanılabilir. Ancak katkıda bulunan kişi:

- üretilen kodu anlamalı,
- çıktıyı repository bağlamında doğrulamalı,
- testleri çalıştırmalı,
- review sırasında yapılan tercihi açıklayabilmelidir.

Anlaşılmayan veya doğrulanmamış kod merge edilmemelidir.

## İletişim

Issue, PR ve review yorumlarında kısa, açık ve profesyonel bir iletişim
kullanın. Belirsiz bir teknik veya tarihsel bilgi varsa tahmin etmek yerine
kanıtını belirtin ya da soru sorun.

## Mehmet Yıldız'ın GitHub Contributor Attribution'ı

Repository Git geçmişinde Mehmet'e ait bir commit bulunmaktadır:

- Commit: `d7a60a2` — `katkı için veri seti yüklenmesi`
- Author: `mhmety <mehmet.yildiz.bst@gmail.com>`
- Committer: aynı kimlik
- PR: [#6](https://github.com/Babintech/ai-geri-donusum-siniflandirma/pull/6)
- PR başlığı: `katkı için veri seti yüklenmesi`
- Merge commit: `8d9f88f`

Commit `main` geçmişindedir; dolayısıyla sorun commit'in merge edilmemesi
değildir. GitHub API commit için author hesabı döndürmemekte ve repository'nin
contributor API çıktısında `mhmety` görünmemektedir. Bu gözlem, commit'te
kullanılan `mehmet.yildiz.bst@gmail.com` adresinin Mehmet'in GitHub hesabına
bağlanmamış, doğrulanmamış veya GitHub tarafından attribution için eşleştirilememiş
olabileceğini gösterir. Kesin hesap ayarı GitHub kullanıcı hesabından kontrol
edilmelidir.

Güvenli çözüm, Mehmet'in bu e-posta adresini GitHub hesabına ekleyip doğrulaması
veya bundan sonraki commit'lerde hesabına bağlı bir GitHub noreply adresi
kullanmasıdır. Geçmişi rewrite etmek, force push yapmak veya eski commit'leri
otomatik olarak değiştirmek bu repository için önerilmez.
