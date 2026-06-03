# Growth Automation & AI Ops Intern Challenge 🚀

Bu proje, "Konuşarak Öğren" platformunun Türkiye'deki İnsan Kaynakları profesyonellerine ulaşmasını sağlamak amacıyla geliştirilmiş, uçtan uca çalışan bir büyüme otomasyonu ve AI Ops prototipidir.

## 🏗️ Sistem Mimarisi & Workflow

Proje, kısıtlı kaynaklar ve bütçe limitleri göz önünde bulundurularak maksimum maliyet ve performans optimizasyonu sağlayacak şekilde tasarlanmıştır:

```text
[Data Scraping: Phantombuster] 
               │ (Gerçek seed veri çekimi: 10 Key Persona)
               ▼
[Data Cleaning & Augmentation: Pandas] 
               │ (Limitler için veri manipülasyonu & 100+ kayıt üretimi)
               ▼
[AI Agent Workflow: Gemini 1.5 Flash API]
               │ (Sektör tahmini, Pain Point analizi ve Lead Skorlama)
               ▼
[Multi-Step Outreach Generation: AI Agent]
               │ (Kişiselleştirilmiş LinkedIn DM ve 3. Gün Follow-Up kurgusu)
               ▼
[CRM Logic & Storage: Enhanced CSV]
                 (Uçtan uca takip ve veritabanı kaydı)
```

## 🛠️ Kurulum ve Çalıştırma

1-Bağımlılıkları yükleyin:

```bash
pip install pandas google-generativeai python-dotenv
```

2-.env dosyasını oluşturun ve API anahtarınızı ekleyin:

```bash
GEMINI_API_KEY=your_api_key_here
```

3-Otomasyonu çalıştırın:

```bash
python main.py
```

## 📊 Çıktılar

leads.csv: Phantombuster'dan çekilen ham veri seti

enriched_leads_crm.csv: AI tarafından zenginleştirilmiş, skorlanmış ve outreach mesajları eklenmiş 106 satırlık nihai CRM veri tabanı

## 🛠️ İzlediğim yol ve kritik detaylar

Phantombuster'dan veri çekerken upgrade etmemek için ücretsiz şekilde yararlandım ve 10 kişinin verisini indirme hakkım vardı.

Bu 10 kişinin verisini indirdikten sonra gerekli sayıyı tamamlamak için `augment_data` fonksiyonu kullandım ve veri sayısını arttırdım. 

İndirdiğim dosyada türkçe karakter gözükmüyordu. Bu sorunu `utf` ile çözdüm. Ve dosyanın içinde gelen limite ulaşılığı ve upgrade etmem gerektiği yazan satırları da cleaning aşamasında sildim.Şirketin teslim beklentisi olan 100+ kişilik havuzu simüle etmek için Python'ın `random` kütüphanesini kullanarak, eldeki gerçek verilerden mantıklı kombinasyonlar üreten ve kurumsal mail formatlarına uygun (`isim.soyisim@company.com`) bir veri çoğaltma algoritması yazdım.

Analiz ve Pipeline aşamasında Verileri işledikten sonra, her lead'in analiz çıktılarını (`Sektör`, `Pain Point`, `Lead Score`, `LinkedIn DM Taslakları`) doğrudan DataFrame üzerinde dinamik sütunlar olarak besleyen bir otomasyon mantığı kurdum.

Prototipi hızlıca test etmek ve veri akışında sekteye uğramamak için tüm bu işlemleri sadece ilk 15 kişide uygulanacak şekilde süreci kurguladım. Bu yüzden üretilen `enriched_leads_crm.csv` dosyasında da ilgili veriler sadece bahsi geçen kişiler için yana kaydırıldığında görülebilmektedir. 

API kısmında ücretsiz olarak faydalanabileceklerimden `GEMINI_API_KEY`ı tercih ettim. Key gizliliğini sağlamaya özen gösterdim. 

## 🛑 Karşılaşılan Sorunlar ve Uygulanan Çözümler

🛑 Sorun 1: Yapay Zeka Çıktılarının Veri Tabanına Enjekte Edilememesi

İlk sürümde LLM'den gelen analiz yanıtları bir array (liste) içinde toplanıyor ancak ana veri tabanına (`df_final`) yeni sütunlar olarak yazılmadan kod sonlanıyordu. Bu da çıktı dosyasında zenginleştirilmiş verilerin eksik kalmasına yol açıyordu.

Çözüm: Pandas'ın `.at[index, 'Column']` metodunu kullanarak her satırın indeksine göre yapay zeka çıktılarını (Sektör, Skor, DM 1 ve DM 3) doğrudan ilgili hücrelere eş zamanlı olarak işledim. Böylece dinamik ve kayıpsız bir CRM veri yapısı elde ettim.

🛑 Sorun 2: Google GenAI SDK Sürüm ve Model İsmi Uyuşmazlığı (404 Not Found)

Google'ın eski `google.generativeai` paketine ait desteğin sonlanması sebebiyle, projeyi geleceğe uyumlu kılmak adına en güncel `google-genai` SDK'sına geçiş yaptım. Ancak bu geçiş esnasında model isimlendirme formatındaki (`models/gemini-1.5-flash`) ön ek uyuşmazlığından dolayı API tarafında `404 NOT_FOUND` hatası tetiklendi.

Çözüm: Hatayı terminal loglarından hızlıca debug ederek yeni SDK istemcisinin (`genai.Client`) model çağırma standartlarını inceledim. Model ismini ön eki olmadan, 2026 standartlarında en güncel, hızlı ve maliyet-etkin çalışan **`gemini-2.5-flash`** mimarisine güncelleyerek API entegrasyonunu tamamen stabil hale getirdim.



