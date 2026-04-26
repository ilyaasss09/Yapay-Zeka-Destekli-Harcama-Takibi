# 🤖 Akıllı Harcama Yöneticisi - Teknik Dokümantasyon

## 1. Projenin Genel Mimarisi ve Teknoloji Altyapısı
Bu proje, modern web geliştirme standartlarına uygun olarak tasarlanmış, yapay zeka destekli bir finansal kategorizasyon uygulamasıdır. Sistem, hafif ve hızlı çalışması amacıyla monolitik ancak kendi içinde modüler bir mimariyle inşa edilmiştir.

* **Backend (Sunucu):** Yüksek performanslı ve asenkron çalışabilen **Python FastAPI** framework'ü kullanılmıştır.
* **Yapay Zeka (LLM):** Doğal dil işleme ve sınıflandırma görevleri için **Google Gemini API** (Büyük Dil Modeli) entegre edilmiştir.
* **Veritabanı (DBMS):** İlişkisel veritabanı yönetim sistemi olarak **SQLite** tercih edilmiş ve veritabanı işlemleri **SQLAlchemy (ORM)** ile yönetilmiştir. Bu sayede SQL enjeksiyonlarına karşı güvenlik sağlanmış ve mimari, ileride PostgreSQL gibi sistemlere kolayca taşınabilir hale getirilmiştir.
* **Frontend (İstemci):** Harici bir kütüphane bağımlılığı yaratmamak adına saf HTML, CSS ve JavaScript (Vanilla JS) ile minimalist bir arayüz tasarlanmıştır.

## 2. Clean Code İlkelerine Uygunluk
Proje geliştirilirken "Spagetti Kod" yaklaşımından kaçınılmış, kodun okunabilirliği ve bakımı ön planda tutulmuştur:

* **Separation of Concerns (Sorumlulukların Ayrılığı):** Kod tabanı tek bir dosyaya yığılmamış, mantıksal katmanlara bölünmüştür:
  * `database.py`: Sadece veritabanı bağlantısı ve tablo modellerini içerir.
  * `ai_service.py`: Sadece dış servis (Google API) ile iletişimi yönetir.
  * `main.py`: Sadece HTTP isteklerini (Routing) karşılar ve diğer modülleri koordine eder.
* **Anlamlı İsimlendirme:** Sınıf, değişken ve fonksiyon isimleri (`categorize_expense_with_ai`, `ExpenseRequest` vb.) ne iş yaptıklarını açıkça belli edecek şekilde İngilizce standartlarında seçilmiştir.
* **Hata Yönetimi (Error Handling):** Dış API çağrılarında (Gemini sunucularına bağlanırken) yaşanabilecek olası kesintiler `try-except` blokları ile kontrol altına alınmış, sistemin çökmesi engellenerek varsayılan değerler ("Diğer" kategorisi) atanmıştır.

## 3. Yapay Zeka Araçları İçin Kullanılan Teknikler
Projede geleneksel makine öğrenmesi (Scikit-learn vb.) yerine, güncel teknoloji olan **LLM (Büyük Dil Modeli)** tabanlı bir yaklaşım izlenmiştir.

* **Prompt Engineering (Komut Mühendisliği):** Modele gönderilen metinde "Rol Atama" (Sen bir finansal asistansın) ve "Kısıtlama" (Sadece şu kategorilerden birini döndür, başka kelime ekleme) teknikleri kullanılarak, modelin halüsinasyon görmesi ve gereksiz metin üretmesi engellenmiştir. (Zero-shot prompting tekniği kullanılmıştır).
* **Dinamik Model Seçimi:** Sistem, statik bir model ismine bağlı kalmak yerine, Google API üzerinden desteklenen aktif modelleri tarayıp ('generateContent' destekli) en güncel çalışan modeli (örn. Gemini Flash veya Pro) otomatik olarak tespit edecek bir algoritmaya sahiptir.

## 4. Teknik Borç (Technical Debt) Optimizasyonu
Projenin teknik borç yüzdesi **%5'in altında** tutulmuştur. Bunun başlıca sebepleri şunlardır:

* Kullanılmayan kod blokları (dead code) temizlenmiştir.
* Pydantic kütüphanesi ile veri doğrulama (Data Validation) katı bir şekilde yapılarak, hatalı verilerin sisteme girmesi baştan engellenmiştir.
* Gelecekte eklenebilecek özellikler (kullanıcı girişi, grafiksel analiz vb.) için kodun esnekliği (ORM ve Modüler yapı sayesinde) korunmuştur; yani proje yeniden yazılmaya ihtiyaç duymadan genişletilebilir durumdadır.
