import hashlib
import os

# --- 1. Anahtar Üretimi ---
# --- 1. Anahtar Üretimi ---
SYSTEM_SECRET = "GizliSistemAnahtari_2025"

def Anahtar_Uret():
    """
    Sistem için sabit bir anahtar üretir.
    Kullanıcıdan parola istemez, sistem içine gömülü değeri kullanır.
    """
    secret = SYSTEM_SECRET.encode('utf-8')
    hash_obj = hashlib.sha256(secret)
    return hash_obj.digest()[:16]

# ... (Yardımcı Fonksiyonlar ve Sifrele/Desifrele aynı kalabilir, sadece Anahtar_Uret çağrısı değişecek)

# --- Yardımcı Fonksiyonlar (Permütasyon ve İkame için) ---
def _permute_block(block):
    """
    Basit bir permütasyon: Byte'ları ters çevirir.
    """
    return block[::-1]

def _substitute_block(block, key_byte_sum):
    return bytes([(b + key_byte_sum) % 256 for b in block])

def _reverse_substitute_block(block, key_byte_sum):
    return bytes([(b - key_byte_sum) % 256 for b in block])

# --- 2. Şifreleme Fonksiyonu ---
def Sifrele(duz_metin, anahtar):
    if isinstance(duz_metin, str):
        duz_metin = duz_metin.encode('utf-8')
    
    # Padding
    block_size = 16
    padding_len = block_size - (len(duz_metin) % block_size)
    padded_metin = duz_metin + bytes([padding_len] * padding_len)
    
    sifreli_metin = bytearray()
    key_sum = sum(anahtar)
    
    for i in range(0, len(padded_metin), block_size):
        block = padded_metin[i : i + block_size]
        xor_block = bytes([b ^ k for b, k in zip(block, anahtar)])
        sub_block = _substitute_block(xor_block, key_sum)
        perm_block = _permute_block(sub_block)
        sifreli_metin.extend(perm_block)
        
    return bytes(sifreli_metin)

# --- 3. Deşifreleme Fonksiyonu ---
def Desifrele(sifreli_metin, anahtar):
    block_size = 16
    desifreli_metin = bytearray()
    key_sum = sum(anahtar)
    
    for i in range(0, len(sifreli_metin), block_size):
        block = sifreli_metin[i : i + block_size]
        rev_perm_block = _permute_block(block)
        rev_sub_block = _reverse_substitute_block(rev_perm_block, key_sum)
        xor_block = bytes([b ^ k for b, k in zip(rev_sub_block, anahtar)])
        desifreli_metin.extend(xor_block)
        
    padding_len = desifreli_metin[-1]
    if padding_len < 1 or padding_len > block_size:
         pass
         
    return desifreli_metin[:-padding_len].decode('utf-8', errors='ignore')

# --- TEST SENARYOLARI ---
if __name__ == "__main__":
    print("=== ŞİFRELEME ALGORİTMASI ===")
    
    # Sistem anahtarını otomatik al
    anahtar = Anahtar_Uret()
    
    while True:
        print("\nSeçenekler:")
        print("1. Otomatik Testleri Çalıştır")
        print("2. Metin Şifrele/Çöz")
        print("q. Çıkış")
        
        choice = input("\nSeçiminiz (1/2/q): ").lower()
        
        if choice == '1':
            print("\n=== OTOMATİK TESTLER ===\n")
            
            # Test 1: Basit Doğrulama
            orijinal_metin = "Merhaba Dünya! Bu bir test mesajıdır."
            print(f"Orijinal Metin: {orijinal_metin}")
            
            sifreli = Sifrele(orijinal_metin, anahtar)
            print(f"[+] Şifreli Metin (Hex): {sifreli.hex()}")
            
            cozulmus = Desifrele(sifreli, anahtar)
            print(f"[+] Çözülmüş Metin: {cozulmus}")
            
            if orijinal_metin == cozulmus:
                print(">>> SONUÇ: BAŞARILI\n")
            else:
                print(">>> SONUÇ: BAŞARISIZ\n")

            # Anahtar hassasiyeti testi (Opsiyonel olarak kalabilir, sistem güvenliği demosu için)
            print("--- Güvenlik Testi (Çığ Etkisi) ---")
            bozuk_anahtar_list = list(anahtar)
            bozuk_anahtar_list[-1] = (bozuk_anahtar_list[-1] ^ 1) 
            bozuk_anahtar = bytes(bozuk_anahtar_list)
            
            yanlis_cozum = Desifrele(sifreli, bozuk_anahtar)
            if yanlis_cozum != orijinal_metin:
                 print(">>> SONUÇ: BAŞARILI (Farklı sistem anahtarı ile veri çözülemedi)")
            else:
                 print(">>> SONUÇ: BAŞARISIZ")
                
        elif choice == '2':
            print("\n=== METİN İŞLEMLERİ ===")
            user_text = input("Düz Metni Girin: ")
            if not user_text:
                continue
                
            sifreli = Sifrele(user_text, anahtar)
            print(f"\n[+] Şifrelenmiş (Hex): {sifreli.hex()}")
            
            cozulmus = Desifrele(sifreli, anahtar)
            print(f"[+] Geri Çözülmüş   : {cozulmus}")
            
        elif choice == 'q':
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim.")
