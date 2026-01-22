import json
import math


# ============================
#   MODY Calculator Function
# ============================

def calc_mody(id, sex, pardm, agedx, hba1c, bmi, agerec, insoroha, t1t2):

    # ---- Parameter validation ----
    if agedx <= 1 or agedx > 35:
        raise ValueError("agedx must be between 1 and 35 (exclusive).")

    # ---- T1 model coefficients ----
    t1coefs = [1.8196, 3.1404, -0.0829, -0.6598, 0.1011, 1.3131]

    # ---- T2 model coefficients ----
    t2coefs = [19.28, -0.3154, -0.2324, -0.6276, 1.7473, -0.0352, -0.9952, 0.6943]

    # ---- PPV lookup tables ----
    ppv1lookup = {
        0: 0.7, 1: 1.9, 2: 2.6, 3: 4.0, 4: 4.9,
        5: 6.4, 6: 7.2, 7: 8.2, 8: 12.6, 9: 49.4
    }

    ppv2lookup = {
        0: 4.6, 1: 15.1, 2: 21.0, 3: 24.4, 4: 32.9,
        5: 35.8, 6: 45.5, 7: 58.0, 8: 62.4, 9: 75.5
    }

    # ==================================
    #      T1 MODEL CALCULATIONS
    # ==================================
    if t1t2 == 1:

        # Order must match coefficients:
        # intercept, pardm, agerec, hba1c, agedx, sex
        t1data = [1, pardm, agerec, hba1c, agedx, sex]

        # log-odds
        t1logor = sum([t1data[i] * t1coefs[i] for i in range(len(t1coefs))])

        # probability
        prob1 = math.exp(t1logor) / (1 + math.exp(t1logor))

        # group
        probgroup = int(prob1 * 10)
        probgroup = min(probgroup, 9)

        result = ppv1lookup[probgroup]

        return {
            "id": id,
            "t1t2": 1,
            "raw_probability": round(prob1, 4),
            "ppv_adjusted": result
        }

    # ==================================
    #      T2 MODEL CALCULATIONS
    # ==================================
    if t1t2 == 2:

        if bmi is None or insoroha is None:
            raise ValueError("T2 model requires BMI and insoroha values.")

        # Order: intercept, agedx, bmi, hba1c, pardm, agerec, insoroha, sex
        t2data = [1, agedx, bmi, hba1c, pardm, agerec, insoroha, sex]

        # log-odds
        t2logor = sum([t2data[i] * t2coefs[i] for i in range(len(t2coefs))])

        # probability
        prob2 = math.exp(t2logor) / (1 + math.exp(t2logor))

        # group
        probgroup = int(prob2 * 10)
        probgroup = min(probgroup, 9)

        result = ppv2lookup[probgroup]

        return {
            "id": id,
            "t1t2": 2,
            "raw_probability": round(prob2, 4),
            "ppv_adjusted": result
        }

    raise ValueError("t1t2 must be 1 or 2.")



# ============================================
#  Command-line Runner (Rscript runner.R eşdeğeri)
# ============================================

if __name__ == "__main__":

    import sys

    if len(sys.argv) < 2:
        print("Error: No JSON input supplied.")
        sys.exit(1)

    input_json = sys.argv[1]
    params = json.loads(input_json)

    result = calc_mody(
        id=params["id"],
        sex=params["sex"],
        pardm=params["pardm"],
        agedx=params["agedx"],
        hba1c=params["hba1c"],
        bmi=params.get("bmi"),
        agerec=params["agerec"],
        insoroha=params.get("insoroha"),
        t1t2=params["t1t2"]
    )

    print(json.dumps(result, indent=4))
