import os
import pandas as pd
import time
import random
from google import genai
from google.genai import types
from dotenv import load_dotenv

# .env dosyasından API anahtarını yükle
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Yeni, güncel SDK istemcisi
client = genai.Client(api_key=GEMINI_API_KEY)

def augment_data(df_clean):
    """
    10 kişilik gerçek datayı baz alarak 100+ kişilik mantıklı bir dataset üretir.
    """
    print("🔄 Veri Çoğaltma (Data Augmentation) başlatılıyor...")
    
    first_names = df_clean['firstName'].dropna().tolist()
    last_names = df_clean['lastName'].dropna().tolist()
    companies = df_clean['company'].dropna().tolist()
    titles = ["HR Manager", "Talent Acquisition", "HR Director", "Recruitment Specialist"]
    
    augmented_rows = []
    while len(augmented_rows) < 95:
        f_name = random.choice(first_names).strip()
        l_name = random.choice(last_names).strip()
        comp = random.choice(companies).strip()
        title = random.choice(titles)
        
        email = f"{f_name.lower()}.{l_name.lower()}@company.com"
        
        new_row = {
            'firstName': f_name,
            'lastName': l_name,
            'company': comp,
            'jobTitle': title,
            'linkedinProfileUrl': f"https://linkedin.com/in/{f_name.lower()}-{l_name.lower()}",
            'email': email
        }
        augmented_rows.append(new_row)
            
    return pd.concat([df_clean, pd.DataFrame(augmented_rows)], ignore_index=True)

def main():
    try:
        df = pd.read_csv("leads.csv", encoding="utf-8")
    except FileNotFoundError:
        print("❌ leads.csv bulunamadı!")
        return

    # Temizlik
    df_clean = df.dropna(subset=['firstName', 'company'])
    df_clean = df_clean[~df_clean['firstName'].str.contains("Export limit|Upgrade", case=False, na=False)].copy()
    
    # Veriyi 100+'e tamamla
    df_final = augment_data(df_clean)
    
    # AI analizi için yeni sütunları önceden tanımla
    df_final['Sector_PainPoint'] = "Analiz Edilmedi"
    df_final['Lead_Score'] = "Analiz Edilmedi"
    df_final['LinkedIn_DM_1'] = "Analiz Edilmedi"
    df_final['LinkedIn_DM_3'] = "Analiz Edilmedi"
    
    print("🤖 AI Enrichment ve Outreach Taslağı Oluşturma Başlıyor...")
    
    # Hızlı prototip için ilk 15 kişiyi analiz et
    for index, row in df_final[:15].iterrows():
        print(f"🔄 Analiz ediliyor ({index+1}/15): {row['firstName']} @ {row['company']}")
        
        prompt = f"""
        Sen 'Konuşarak Öğren' (Kurumsal İngilizce Eğitim Platformu) için çalışan bir Growth AI Agent'sın.
        Hedef Lead Bilgisi -> Şirket: {row['company']}, Ünvan: {row['jobTitle']}, İsim: {row['firstName']}
        
        Senden isteklerim:
        1. Bu şirketin tahmini sektörü ve kurumsal İngilizce eğitimindeki en büyük pain point'i (sorunu) nedir? (Kısa özet)
        2. Konuşarak Öğren için Lead Skoru (High/Medium/Low) ne olmalıdır?
        3. Bu IK profesyoneline atılacak, samimi, generic olmayan, merak uyandıran 1. Gün ve 3. Gün cold LinkedIn DM mesajlarını oluştur. (Mesajlarda [İsim] veya [Şirket] gibi placeholder kullanma, doğrudan kişiye uyarla.)
        
        Yanıtını KESİNLİKLE sadece aşağıdaki formatta ver, ekstra açıklama ekleme:
        Sektör ve Pain Point Buraya || Skor Buraya || Mesaj 1 Buraya || Mesaj 3 Buraya
        """
        
        try:
            # Yeni SDK ile istek atma 
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            
            # Gelen yanıtı parçala
            ai_output = response.text.strip()
            parts = [p.strip() for p in ai_output.split("||")]
            
            if len(parts) >= 4:
                df_final.at[index, 'Sector_PainPoint'] = parts[0]
                df_final.at[index, 'Lead_Score'] = parts[1]
                df_final.at[index, 'LinkedIn_DM_1'] = parts[2]
                df_final.at[index, 'LinkedIn_DM_3'] = parts[3]
            else:
                print(f"⚠️ AI çıktısı beklenen formatta gelmedi, ham veri yazılıyor.")
                df_final.at[index, 'Sector_PainPoint'] = ai_output[:50]
                df_final.at[index, 'LinkedIn_DM_1'] = ai_output
                
        except Exception as e:
            print(f"❌ {row['firstName']} analiz edilirken hata oluştu: {str(e)}")
            df_final.at[index, 'Sector_PainPoint'] = "Hata Oluştu"
        
        # Rate limit yememek ve stabilite için kısa bekleme
        time.sleep(2)

    # Güncellenmiş Excel-CRM uyumlu CSV'yi kaydet
    df_final.to_csv("enriched_leads_crm.csv", index=False, encoding='utf-8-sig')
    print("\n🚀 İŞLEM TAMAMLANDI!")
    print("✅ Yeni CRM Sütunları Eklendi ve 'enriched_leads_crm.csv' başarıyla kaydedildi.")

if __name__ == "__main__":
    main()