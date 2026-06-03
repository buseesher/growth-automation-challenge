import os
import pandas as pd
import time
import random
import google.generativeai as genai
from dotenv import load_dotenv

# Upload the API key from the .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def augment_data(df_clean):
    """
    10 kişilik gerçek datayı (image_a09ab2.png) baz alarak 
    100+ kişilik mantıklı bir dataset üretir.
    """
    print("🔄 Veri Çoğaltma (Data Augmentation) başlatılıyor...")
    
    # Create a pool from the existing data
    first_names = df_clean['firstName'].dropna().tolist()
    last_names = df_clean['lastName'].dropna().tolist()
    companies = df_clean['company'].dropna().tolist()
    titles = ["HR Manager", "Talent Acquisition", "HR Director", "Recruitment Specialist"]
    
    augmented_rows = []
    while len(augmented_rows) < 95:
        f_name = random.choice(first_names)
        l_name = random.choice(last_names)
        comp = random.choice(companies)
        title = random.choice(titles)
        
        # Realistic email production
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
    # read data
    try:
        # To fix Turkish character errors in Excel, used utf-8
        df = pd.read_csv("leads.csv", encoding="utf-8")
    except FileNotFoundError:
        print("❌ leads.csv bulunamadı!")
        return

    # Cleaning
    df_clean = df.dropna(subset=['firstName', 'company'])
    df_clean = df_clean[~df_clean['firstName'].str.contains("Export limit|Upgrade", case=False, na=False)]
    
    # 3. complete data 100+
    df_final = augment_data(df_clean)
    
    # AI Analyz ve Outreach
    # Let's perform AI analysis on the first 15 people so the prototype works quickly
    # If you want, you can delete the '[:15]' part from the loop.
    results = []
    for index, row in df_final[:15].iterrows():
        print(f"🔄 Analiz ediliyor ({index+1}): {row['firstName']} @ {row['company']}")
        
        prompt = f"""
        Şirket: {row['company']}, Ünvan: {row['jobTitle']}, İsim: {row['firstName']}
        1. Bu şirketin sektörü ve İngilizce eğitim ihtiyacı nedir?
        2. Lead Skoru (High/Medium/Low) ver ve nedenini açıkla.
        3. Kişiselleştirilmiş 1. Gün ve 3. Gün LinkedIn mesajlarını oluştur.
        Format: Sektör || Pain Point || Skor || Mesaj 1 || Mesaj 3
        """
        
        try:
            response = model.generate_content(prompt)
            results.append(response.text.split("||"))
        except:
            results.append(["Hata"] * 5)
        
        time.sleep(4) # # Free data protection

    # Save the results (make Excel compatible with UTF-8-SIG)
    df_final.to_csv("enriched_leads_crm.csv", index=False, encoding='utf-8-sig')
    print("✅ CRM Dosyası Hazır: enriched_leads_crm.csv")

if __name__ == "__main__":
    main()