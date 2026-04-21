# 🚗 Sürücü Yorgunluk Tespit Sistemi (Raspberry Pi)

**Python**, **OpenCV** ve **Raspberry Pi** ile geliştirilmiş gerçek zamanlı sürücü izleme sistemi.  
Bu proje, yüz ve göz tespiti kullanarak sürücü yorgunluğunu tespit eder ve görsel/işitsel uyarılar tetikler.

---

## 📌 Özellikler

- 👁️ Haar Cascade ile yüz tespiti
- 👀 Yorgunluk analizi için göz tespiti
- ⚠️ Göz kapanması ve yüz kaybına dayalı yorgunluk tespiti
- 🔊 Buzzer uyarı sistemi
- 🔴🟢 LED göstergeleri:
  - Yeşil → Normal durum
  - Kırmızı → Yorgunluk tespit edildi
- 📷 PiCamera2 ile gerçek zamanlı video işleme
- 🖥️ Ekranda uyarı mesajları

---

## 🧠 Sistem Nasıl Çalışır?

Sistem, kameradan gelen kareleri sürekli olarak işler:

1. Sürücünün yüzünü tespit eder
2. Yüzün üst yarısında gözleri arar
3. Şu mantığı uygular:
   - ❌ Yüz tespit edilemedi → Olası baş düşmesi
   - ❌ Yüz tespit edildi fakat göz yok → Olası uyku
   - ✅ Yüz + göz tespit edildi → Uyanık

Sistem belirli sayıda kare boyunca yorgunluk tespit ederse:
- **Buzzer**'ı etkinleştirir
- **Kırmızı LED**'i yakar
- Ekranda uyarı mesajı görüntüler

---

## 🛠️ Donanım Gereksinimleri

- Raspberry Pi (önerilen: Pi 4)
- Raspberry Pi Kamera Modülü
- 1x Kırmızı LED
- 1x Yeşil LED
- 1x Buzzer
- Dirençler (220Ω önerilen)
- Jumper kablolar
- Breadboard

---

## 🔌 GPIO Pin Yapılandırması

| Bileşen     | GPIO Pin |
|------------|----------|
| Yeşil LED  | 23       |
| Kırmızı LED| 17       |
| Buzzer     | 25       |

---

## 💻 Yazılım Gereksinimleri

- Python 3
- OpenCV
- Picamera2
- RPi.GPIO

Bağımlılıkları yüklemek için:

```bash
pip install opencv-python
sudo apt install python3-picamera2
```

---

## 📂 Gerekli Dosyalar

Aşağıdaki Haar Cascade XML dosyalarının proje dizininde bulunduğundan emin olun:

- `haarcascade_frontalface_default.xml`
- `haarcascade_eye.xml`

OpenCV GitHub üzerinden indirebilirsiniz:  
[https://github.com/opencv/opencv/tree/master/data/haarcascades](https://github.com/opencv/opencv/tree/master/data/haarcascades)

---

## ▶️ Nasıl Çalıştırılır?

```bash
python3 main.py
```

Uygulamadan çıkmak için **`q`** tuşuna basın.

---

## ⚙️ Yapılandırma

Hassasiyeti ayarlayabilirsiniz:

```python
YORGUNLUK_ESIGI = 5
```

- Düşük değer → Daha hızlı tespit (daha hassas)
- Yüksek değer → Daha kararlı tespit

---

## ⚠️ Sınırlamalar

- Haar Cascade, aydınlatma koşullarına duyarlıdır
- Düşük ışık veya tıkanma durumlarında yanlış pozitifler üretebilir
- Derin öğrenme tabanlı çözümler kadar doğru değildir

---

## 🚀 Gelecekteki İyileştirmeler

- 🔥 Haar Cascade'i CNN/DNN modelleriyle değiştirme
- 📊 EAR (Göz Görünüş Oranı) hesabı ekleme
- 🌙 Gece tespitinin iyileştirilmesi
- 📡 Kayıt ve uzaktan izleme ekleme
- 🚘 Gerçek araç sistemleriyle entegrasyon

---

## 👨‍💻 Geliştiriciler

**Umutcan Oğuz, Azad Bedir, Kadir Gündüz, Yusuf Aksu** tarafından geliştirilmiştir.

---

## 📄 Lisans

Bu proje açık kaynaklıdır ve MIT Lisansı altında sunulmaktadır.

---

## ⭐ Destek

Projeyi beğendiyseniz GitHub'da ⭐ vermeyi unutmayın!
