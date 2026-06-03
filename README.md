# Growth Automation & AI Ops Intern Challenge 🚀

Bu proje, "Konuşarak Öğren" platformunun Türkiye'deki İnsan Kaynakları profesyonellerine ulaşmasını sağlamak amacıyla geliştirilmiş, uçtan uca çalışan minimum bir büyüme otomasyonu ve AI Ops prototipidir.

## 🏗️ Sistem Mimarisi & Workflow

Proje, kısıtlı kaynaklar ve bütçe limitleri göz önünde bulundurularak maksimum maliyet ve performans optimizasyonu sağlayacak şekilde tasarlanmıştır:

```text
[Data Scraping: Phantombuster] 
               │ (Gerçek seed veri çekimi: 10 Karar Verici)
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



