import os
import google.generativeai as genai
from dotenv import load_dotenv

# .env dosyasındaki gizli değişkenleri yükle
load_dotenv()

# DİKKAT: Buraya kendi aldığın API anahtarını yapıştır
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("API Anahtarı bulunamadı! Lütfen .env dosyanızı kontrol edin.")

genai.configure(api_key=GEMINI_API_KEY)

# Google'ın o an desteklediği aktif ve çalışan modeli otomatik bulan fonksiyon (Bonus Puan!)
def get_active_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # İsminde flash veya pro geçen güncel modelleri önceliklendir
                if 'flash' in m.name or 'pro' in m.name:
                    print(f"Otomatik seçilen model: {m.name}")
                    return m.name
        
        # Eğer özel bir filtreye uymazsa, çalışan ilk modeli seç
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Otomatik seçilen model: {m.name}")
                return m.name
    except Exception as e:
        print(f"Model listesi alınırken hata: {e}")
        return 'gemini-1.5-flash' # Son çare varsayılan

# Modeli dinamik olarak başlat
aktif_model_adi = get_active_model()
model = genai.GenerativeModel(aktif_model_adi)

def categorize_expense_with_ai(description: str) -> str:
    """
    Kullanıcının girdiği harcama metnini yapay zeka dil modeli ile kategorize eder.
    """
    prompt = f"""
    Sen bir finansal asistan yapay zeka modelisin. Kullanıcının girdiği harcama açıklamasını oku ve sadece aşağıdaki kategorilerden en uygun olanının adını döndür. Başka hiçbir kelime veya noktalama işareti ekleme.
    Kategoriler: Market, Ulaşım, Fatura, Eğlence, Sağlık, Eğitim, Dışarıda Yemek, Diğer
    
    Harcama Açıklaması: "{description}"
    Kategori:
    """
    
    try:
        response = model.generate_content(prompt)
        category = response.text.strip()
        return category
    except Exception as e:
        print(f"Yapay zeka hatası: {e}")
        return "Diğer"