# 🧬 MODY Risk Assessment Chatbot / MODY Risk Değerlendirme Chatbotu

---

## English

### Overview
This project is an **AI-assisted MODY (Maturity Onset Diabetes of the Young) risk pre‑assessment system**.
Instead of static forms, users interact with a **conversational chatbot** that collects medical information step by step and calculates **MODY probability scenarios** using clinically inspired statistical models.

> ⚠️ **Medical Disclaimer**  
> This system is **NOT** a diagnostic or treatment tool.  
> MODY diagnosis can only be confirmed via **genetic testing** and clinical evaluation by a specialist.

---

### Key Features
- 💬 Conversational data collection (chat-based)
- 🧠 LLM-powered medical dialogue (Ollama-compatible)
- 📊 Scenario-based MODY probability calculation
- 🧮 Separate T1 / T2 diabetes models
- 📈 Aggregated results (min / max / average PPV)
- 🌐 Simple web interface (Flask + HTML + Tailwind)

---

### System Architecture
```
User
 │
 ▼
Web UI (index.html)
 │
 ▼
Flask API (app.py)
 │
 ▼
LLM Chat Engine (Ollama)
 │
 ▼
Structured JSON Extraction
 │
 ▼
Scenario Generator
 │
 ▼
MODY Risk Calculator
 │
 ▼
Results + Visualization
```

---

### Core Files
| File | Description |
|-----|------------|
| `app.py` | Flask backend & chat API |
| `index.html` | Web UI (chat + charts) |
| `generator.py` | Scenario generation logic |
| `mody_cal.py` | MODY probability calculator |
| `run_all.py` | Batch scenario runner |
| `veriuretim.py` | Synthetic training data generator |
| `llamahazirlama.py` | LLaMA / prompt formatting utilities |
| `egitim.ipynb` | Model training & experimentation |

---

### Input Parameters (Collected via Chat)
- Diabetes type (T1 / T2 / uncertain)
- Diagnosis age (critical threshold ≤ 35)
- Current age
- Biological sex
- Family history (1st degree)
- HbA1c (%, mmol/mol, or category)
- Height & weight **or** BMI category
- Current treatment (oral / insulin)

---

### Output
- Multiple risk scenarios
- Adjusted PPV (Positive Predictive Value)
- Textual explanation of results
- Summary statistics

---



## Türkçe

### Genel Bakış
Bu proje, **MODY (Maturity Onset Diabetes of the Young)** için geliştirilmiş **yapay zeka destekli bir ön risk değerlendirme sistemidir**.
Klasik formlar yerine, kullanıcıdan bilgiler **doğal bir sohbet** aracılığıyla toplanır ve **çoklu senaryolar üzerinden MODY olasılığı** hesaplanır.

> ⚠️ **Tıbbi Uyarı**  
> Bu sistem **tanı veya tedavi amacıyla kullanılmaz**.  
> MODY tanısı yalnızca **genetik test** ve uzman hekim değerlendirmesi ile konur.

---

### Öne Çıkan Özellikler
- 💬 Sohbet tabanlı bilgi toplama
- 🧠 LLM destekli akıllı yönlendirme
- 📊 Senaryo bazlı MODY hesaplaması
- 🧮 Tip 1 / Tip 2 için ayrı modeller
- 📈 Min / Max / Ortalama risk özeti
- 🌐 Basit ve modern web arayüzü

---

### Sistem Mimarisi
```
Kullanıcı
 │
 ▼
Web Arayüzü
 │
 ▼
Flask API
 │
 ▼
LLM (Ollama)
 │
 ▼
Yapılandırılmış JSON
 │
 ▼
Senaryo Üretimi
 │
 ▼
MODY Hesaplayıcı
 │
 ▼
Sonuçlar
```

---

### Temel Dosyalar
| Dosya | Açıklama |
|------|---------|
| `app.py` | Flask sunucu ve API |
| `index.html` | Chat arayüzü |
| `generator.py` | Senaryo üretimi |
| `mody_cal.py` | MODY risk hesaplayıcı |
| `run_all.py` | Toplu senaryo çalıştırma |
| `veriuretim.py` | Eğitim verisi üretimi |
| `llamahazirlama.py` | LLM formatlama |
| `egitim.ipynb` | Eğitim & deney defteri |

---

### Sohbetle Toplanan Bilgiler
- Diyabet tipi
- Tanı yaşı (**≤ 35 kritik**)
- Mevcut yaş
- Biyolojik cinsiyet
- Aile öyküsü
- HbA1c değeri
- Boy & kilo veya BMI
- Güncel tedavi şekli

---

### Çıktılar
- Çoklu MODY senaryosu
- PPV (pozitif öngörü değeri)
- Açıklayıcı sonuç metni
- Özet istatistikler


