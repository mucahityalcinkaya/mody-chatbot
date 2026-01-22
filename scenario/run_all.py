import json
from generator import generate_scenarios
from mody_cal import calc_mody   # Python modülü

# ================================
#  Tüm senaryoları çalıştır
# ================================
def run_all_scenarios(user_inputs):
    scenarios = generate_scenarios(user_inputs)
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

        results.append({
            "scenario": sen,
            "mody_result": mody_result
        })

    return results

if __name__ == "__main__":

    # Küçük, sade bir örnek seti
    sample_inputs = {
        "pardm": [0],          # 1 değer
        "agedx": [25],         # 1 değer
        "hba1c": [6.5, 10.0],  # 2 değer
        "bmi": [24],           # 1 değer
        "insoroha": [0],       # 1 değer
        "t1t2": [1,2],         # 2 model
        "sex": 1,
        "agerec": 25
    }

    # Total:  
    # T1 için: pardm(1) × agedx(1) × hba1c(2) = **2 senaryo**
    # T2 için: pardm(1) × agedx(1) × hba1c(2) × bmi(1) × insoroha(1) = **2 senaryo**
    # TOPLAM = **4**

    final_output = run_all_scenarios(sample_inputs)

    print("Üretilen toplam senaryo:", len(final_output))
    print(json.dumps(final_output, indent=4, ensure_ascii=False))