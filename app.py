
import cv2
from picamera2 import Picamera2
import RPi.GPIO as GPIO 

# --- 1. DONANIM (GPIO) KURULUMU VE YAPILANDIRMASI ---
PIN_KIRMIZI_LED = 17 # Yorgunluk uyarısı
PIN_YESIL_LED = 23   # Normal durum
PIN_BUZZER = 25      # Sesli alarm

GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

# Pinleri çıkış (OUTPUT) olarak ayarlıyoruz
GPIO.setup(PIN_YESIL_LED, GPIO.OUT)
GPIO.setup(PIN_KIRMIZI_LED, GPIO.OUT)
GPIO.setup(PIN_BUZZER, GPIO.OUT)

# Başlangıçta sadece Yeşil LED yansın, diğerleri kapalı olsun
GPIO.output(PIN_YESIL_LED, GPIO.HIGH)
GPIO.output(PIN_KIRMIZI_LED, GPIO.LOW)
GPIO.output(PIN_BUZZER, GPIO.LOW)

# --- 2. PICAMERA2 KURULUMU VE YAPILANDIRMASI ---
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"format": "RGB888", "size": (320, 240)})
picam2.configure(config)
picam2.start()

# --- 3. HAAR CASCADE MODELLERİNİN YÜKLENMESİ ---
try:
    yuz_modeli = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    goz_modeli = cv2.CascadeClassifier('haarcascade_eye.xml')
except Exception as e:
    print(f"HATA: XML dosyaları yüklenemedi. Detay: {e}")
    exit()

# --- 4. YORGUNLUK TESPİTİ DEĞİŞKENLERİ ---
kapali_kare_sayaci = 0
YORGUNLUK_ESIGI = 5  

# --- 5. PENCERE YÖNETİMİ ---
pencere_adi = 'Surucu Durum Izleme Sistemi'
cv2.namedWindow(pencere_adi, cv2.WINDOW_NORMAL)
cv2.resizeWindow(pencere_adi, 800, 600) 

print("Yorgunluk takip sistemi devrede. Çıkmak için 'q' tuşuna basın.")

try:
    while True:
        # Görüntüyü al ve formatla
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        gri_kare = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Yüzleri tespit et
        yuzler = yuz_modeli.detectMultiScale(gri_kare, 1.3, 5)

        # 1. SENARYO: YÜZ BULUNAMADI (Boyun düştü)
        if len(yuzler) == 0:
            kapali_kare_sayaci += 1
            print(f"Uyarı: Yüz bulunamadı (Boyun Düştü)! Sayaç: {kapali_kare_sayaci}")
        
        # 2. VE 3. SENARYO: YÜZ BULUNDU
        else:
            goz_bulundu = False
            for (x, y, w, h) in yuzler:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
                # Gözleri sadece yüzün üst yarısında ara
                yuzun_ust_yarisi = int(h / 2)
                roi_gri = gri_kare[y:y+yuzun_ust_yarisi, x:x+w]
                roi_renkli = frame[y:y+yuzun_ust_yarisi, x:x+w]

                gozler = goz_modeli.detectMultiScale(roi_gri, scaleFactor=1.1, minNeighbors=10)
                
                if len(gozler) > 0:
                    goz_bulundu = True 
                    for (ex, ey, ew, eh) in gozler:
                        cv2.rectangle(roi_renkli, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            
            if not goz_bulundu:
                # 2. SENARYO: Yüz var ama göz yok (Uyku)
                kapali_kare_sayaci += 1
                print(f"Uyarı: Göz bulunamadı (Uyku)! Sayaç: {kapali_kare_sayaci}")
            else:
                # 3. SENARYO: Uyanık
                kapali_kare_sayaci = 0
                GPIO.output(PIN_YESIL_LED, GPIO.HIGH)
                GPIO.output(PIN_KIRMIZI_LED, GPIO.LOW)
                GPIO.output(PIN_BUZZER, GPIO.LOW)

        # --- DONANIM TETİKLENMESİ (UYARI DURUMU) ---
        if kapali_kare_sayaci >= YORGUNLUK_ESIGI:
            print("\n!!! DİKKAT: SÜRÜCÜ YORGUN - ARAÇ OTONOM MODA GEÇİYOR !!!\n")
            
            # Donanım Uyarısı: Yeşil söner, Kırmızı yanar, Buzzer öter
            GPIO.output(PIN_YESIL_LED, GPIO.LOW)
            GPIO.output(PIN_KIRMIZI_LED, GPIO.HIGH)
            GPIO.output(PIN_BUZZER, GPIO.HIGH)
            
            # Ekran Üzeri Görsel Uyarı
            cv2.putText(frame, "DIKKAT: YORGUNLUK / BOYUN DUSMESI!", (10, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
            cv2.putText(frame, "OTONOM MOD AKTIF", (10, 80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Görüntüyü göster
        cv2.imshow(pencere_adi, frame)

        # 'q' ile çıkış
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Sistemi güvenlice kapat
    picam2.stop()
    cv2.destroyAllWindows()
    GPIO.cleanup() 
    print("Sistem güvenli bir şekilde kapatıldı.")
