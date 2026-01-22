from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import requests
import uuid
import json
import re

app = Flask(__name__)
app.secret_key = 'mody-secret-key-2026'
CORS(app)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mody-chat"

sessions = {}

def get_session_id():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

def get_or_create_session(session_id):
    if session_id not in sessions:
        sessions[session_id] = {'history': [], 'state': 'chatting', 'json_result': None}
    return sessions[session_id]

def chat_with_ollama(history):
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "messages": history,
            "stream": False
        }, timeout=120)
        if response.status_code == 200:
            return response.json()['message']['content']
        return "Hata: Model yanıt vermedi."
    except Exception as e:
        return f"Hata: {str(e)}"

def extract_json(text):
    try:
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            json_str = text[start:end+1]
            parsed = json.loads(json_str)
            if 't1t2' in parsed or 'sex' in parsed:
                return parsed
    except:
        pass
    return None

def prepare_inputs_for_calculator(json_data):
    """JSON'u calculator formatına çevir"""
    
    # Debug - gelen veriyi gör
    print("=" * 50)
    print("GELEN JSON:", json.dumps(json_data, indent=2, ensure_ascii=False))
    print("=" * 50)
    
    inputs = {
        "t1t2": json_data.get("t1t2", [1]),
        "sex": json_data.get("sex", 1),
        "agerec": json_data.get("agerec", 25),
        "pardm": json_data.get("pardm", [0]),
        "agedx": json_data.get("agedx", [25]),
        "insoroha": json_data.get("insoroha", [0]),
    }
    
    # HbA1c
    hba1c = []
    if json_data.get("hba1c_yuzde") and len(json_data.get("hba1c_yuzde", [])) > 0:
        hba1c = json_data["hba1c_yuzde"]
    elif json_data.get("hba1c_mol") and len(json_data.get("hba1c_mol", [])) > 0:
        hba1c = [round((m / 10.929) + 2.15, 1) for m in json_data["hba1c_mol"]]
    else:
        hba1c = [7.0]
    inputs["hba1c"] = hba1c
    
    # BMI
    boy = json_data.get("boy")
    kilo = json_data.get("kilo")
    bmi_kategori = json_data.get("bmi_kategori")
    
    if boy and kilo:
        boy_m = boy / 100
        inputs["bmi"] = [round(kilo / (boy_m ** 2), 1)]
    elif bmi_kategori:
        kategori_map = {"zayif": 17.5, "normal": 22.0, "kilolu": 27.5, "obez": 32.5}
        inputs["bmi"] = [kategori_map.get(bmi_kategori.lower(), 22.5)]
    else:
        inputs["bmi"] = [22.5]
    
    # Debug - hesaplanan inputs
    print("HESAPLANAN INPUTS:", json.dumps(inputs, indent=2, ensure_ascii=False))
    print("=" * 50)
    
    return inputs


def generate_result_text(results, summary):
    """Sonuçları Türkçe açıklama metni olarak oluştur"""
    
    lines = []
    lines.append("📊 **MODY Risk Değerlendirmesi Sonuçları**\n")
    
    # Tip 1 senaryoları
    t1_results = [r for r in results if r["scenario"]["t1t2"] == 1]
    t2_results = [r for r in results if r["scenario"]["t1t2"] == 2]
    
    if t1_results:
        lines.append("**Tip 1 Diyabet Senaryoları:**")
        for r in t1_results:
            s = r["scenario"]
            ppv = r["mody_result"]["ppv_adjusted"]
            pardm_text = "ailede diyabet VAR" if s["pardm"] == 1 else "ailede diyabet YOK"
            lines.append(f"• {pardm_text}, HbA1c: %{s['hba1c']} → MODY olasılığı: **%{ppv}**")
    
    if t2_results:
        lines.append("\n**Tip 2 Diyabet Senaryoları:**")
        for r in t2_results:
            s = r["scenario"]
            ppv = r["mody_result"]["ppv_adjusted"]
            pardm_text = "ailede diyabet VAR" if s["pardm"] == 1 else "ailede diyabet YOK"
            tedavi_text = "insülin kullanıyor" if s["insoroha"] == 1 else "oral ilaç/diyet"
            lines.append(f"• {pardm_text}, {tedavi_text}, BMI: {s['bmi']}, HbA1c: %{s['hba1c']} → MODY olasılığı: **%{ppv}**")
    
    # Özet
    lines.append(f"\n📈 **Özet:** {summary['total_scenarios']} senaryo hesaplandı.")
    lines.append(f"En düşük: %{summary['min_ppv']} | En yüksek: %{summary['max_ppv']} | Ortalama: %{summary['avg_ppv']}")
    
    # Uyarı
    lines.append("\n⚠️ **Önemli:** Bu sonuçlar kesin tanı değildir. MODY tanısı ancak genetik test ile konulabilir. Sonuçlarınızı doktorunuzla paylaşmanızı öneririz.")
    
    return "\n".join(lines)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Mesaj boş olamaz'}), 400
    
    session_id = get_session_id()
    user_session = get_or_create_session(session_id)
    
    user_session['history'].append({"role": "user", "content": user_message})
    assistant_response = chat_with_ollama(user_session['history'])
    user_session['history'].append({"role": "assistant", "content": assistant_response})
    
    # JSON var mı kontrol et (kullanıcıya gösterme)
    json_result = extract_json(assistant_response)
    
    if json_result:
        user_session['state'] = 'completed'
        user_session['json_result'] = json_result
        # JSON'u response'dan temizle
        clean_response = "Bilgilerinizi aldım, hesaplama yapılıyor..."
    else:
        clean_response = assistant_response
    
    return jsonify({
        'response': clean_response,
        'state': user_session['state'],
        'json_result': json_result
    })

@app.route('/api/calculate', methods=['POST'])
def calculate():
    from scenario.generator import generate_scenarios
    from scenario.mody_cal import calc_mody
    
    data = request.json
    
    try:
        inputs = prepare_inputs_for_calculator(data)
        scenarios = generate_scenarios(inputs)
        results = []
        
        for sen in scenarios:
            mody_result = calc_mody(
                id=sen["scenario_id"],
                sex=sen["sex"],
                pardm=sen["pardm"],
                agedx=sen["agedx"],
                hba1c=sen["hba1c"],
                bmi=sen["bmi"],
                agerec=sen["agerec"],
                insoroha=sen["insoroha"],
                t1t2=sen["t1t2"]
            )
            results.append({"scenario": sen, "mody_result": mody_result})
        
        ppv_values = [r["mody_result"]["ppv_adjusted"] for r in results]
        summary = {
            "total_scenarios": len(results),
            "min_ppv": min(ppv_values) if ppv_values else 0,
            "max_ppv": max(ppv_values) if ppv_values else 0,
            "avg_ppv": round(sum(ppv_values) / len(ppv_values), 1) if ppv_values else 0
        }
        
        # Türkçe açıklama metni
        result_text = generate_result_text(results, summary)
        
        return jsonify({
            'success': True, 
            'results': results, 
            'summary': summary,
            'result_text': result_text
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 500

@app.route('/api/reset', methods=['POST'])
def reset():
    session_id = get_session_id()
    if session_id in sessions:
        del sessions[session_id]
    return jsonify({'success': True})

if __name__ == '__main__':
    print("🚀 MODY Sunucu: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)