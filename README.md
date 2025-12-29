# Bilgi Sistemleri ve Güvenliği - Şifreleme Algoritması Projesi

**Ders:** Bilgi Sistemleri ve Güvenliği  
**Konu:** Blok Şifreleme Algoritması Tasarımı ve Uygulaması  

## Proje Özeti
Bu proje kapsamında, metin verilerini şifrelemek ve deşifrelemek için özgün bir **Blok Şifreleme (Block Cipher)** algoritması geliştirilmiştir. Algoritma, modern kriptografik prensipler olan **Karıştırma (Diffusion)** ve **Karışıklık (Confusion)** ilkelerini sağlamak amacıyla XOR, İkame (Substitution) ve Permütasyon (Permutation) işlemlerini kullanır.

---

## Algoritma Tasarımı (Adım Adım)

Algoritma, verileri **16 Byte'lık (128 bit)** bloklar halinde işler. Her blok için aşağıdaki adımlar uygulanır:

### Girdiler
*   **Düz Metin (Plaintext):** Şifrelenecek veri. (Örnek: `MERHABA`)
*   **Anahtar (Key):** Sistem tarafından üretilen 16 byte'lık sabit gizli anahtar. (`GizliSistemAnahtari_2025` -> SHA-256 Hash'inin ilk 16 byte'ı)

### İşlem Adımları

#### 1. Adım: Hazırlık ve Padding
Metin ASCII (UTF-8) değerlerine dönüştürülür. Eğer metin uzunluğu 16'nın katı değilse, sonuna eksik kalan sayıyı belirten değerler eklenir (PKCS#7 Padding).

> **Örnek:** `MERHABA` (7 Byte) -> 16 Byte'a tamamlamak için sonuna 9 adet `9` sayısı eklenir.

#### 2. Adım: XOR İşlemi (Anahtar ile Karıştırma)
Her bir veri bloğu, anahtar ile XOR işlemine tabi tutulur. Bu işlem, veriyi matematiksel olarak anahtarla harmanlar.

> `ŞifreliByte[i] = DüzByte[i] ^ Anahtar[i]`

#### 3. Adım: İkame (Substitution)
XOR işleminden çıkan veriler, anahtarın sayısal toplamına göre belirli bir miktar kaydırılır (Mod 256). Bu adım, **Karışıklık (Confusion)** sağlar.

> `YeniByte[i] = (EskiByte[i] + AnahtarToplamı) % 256`

#### 4. Adım: Permütasyon (Yer Değiştirme)
Blok içindeki byte'ların sırası ters çevrilir. Bu işlem, verinin yapısını bozarak **Karıştırma (Diffusion)** sağlar.

> `[A, B, C, D] -> [D, C, B, A]`

---

## Kullanım Talimatları

Algoritma Python dili ile geliştirilmiştir ve tek bir dosya halinde çalışır.

### Kurulum ve Çalıştırma

1.  Python 3 yüklü olduğundan emin olun.
2.  `cipher_algo.py` dosyasının olduğu dizine gidin.
3.  Aşağıdaki komutu çalıştırın:

```bash
python3 cipher_algo.py
```

### Uygulama Menüsü

Program çalıştırıldığında aşağıdaki menü görüntülenir:

1.  **Otomatik Testleri Çalıştır:** Algoritmanın `Merhaba Dünya!` gibi örnek metinlerle doğru çalışıp çalışmadığını test eder. Ayrıca anahtarın 1 biti değiştiğinde şifrenin tamamen bozulduğunu (Çığ Etkisi) gösterir.
2.  **Metin Şifrele/Çöz:** Kullanıcıdan bir metin girmesini ister. Bu metni şifreler (Hex formatında gösterir) ve ardından tekrar deşifre ederek orijinal metni ekrana basar.

---

## Örnek Senaryo

**Girdi:** `Deneme`

**1. Şifreleme:**
*   Sistem Anahtarı ile işlem yapılır.
*   **Çıktı (Hex):** `a3f1...9d` (Uzun ve karmaşık bir hex dizisi)

**2. Deşifreleme:**
*   Şifreli veri aynı anahtar ile çözülür.
*   **Sonuç:** `Deneme`

---

## Güvenlik Analizi
*   **Gizlilik:** `Anahtar_Uret` fonksiyonu dışarıdan parametre almaz, kaynak kodun içindeki "GizliSistemAnahtari"nı kullanır.
*   **Bütünlük:** Padding kontrolü ile verinin eksiksiz çözülmesi sağlanır.
*   **Çığ Etkisi (Avalanche Effect):** Anahtardaki veya metindeki en ufak bir değişim, şifreli verinin tamamını değiştirir.
