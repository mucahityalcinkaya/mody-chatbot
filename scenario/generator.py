import itertools

def _uniq(seq):
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

def generate_scenarios(inputs):
    scenarios = []
    scenario_id = 1

    # normalize + unique
    inputs["t1t2"]     = _uniq(inputs.get("t1t2", []))
    inputs["pardm"]    = _uniq(inputs.get("pardm", []))
    inputs["agedx"]    = _uniq(inputs.get("agedx", []))
    inputs["hba1c"]    = _uniq(inputs.get("hba1c", []))
    inputs["bmi"]      = _uniq(inputs.get("bmi", []))
    inputs["insoroha"] = _uniq(inputs.get("insoroha", []))

    has_t1 = 1 in inputs["t1t2"]
    has_t2 = 2 in inputs["t1t2"]

    # T1
    if has_t1:
        for (pardm, agedx, hba1c) in itertools.product(inputs["pardm"], inputs["agedx"], inputs["hba1c"]):
            scenarios.append({
                "scenario_id": scenario_id,
                "t1t2": 1,
                "sex": inputs["sex"],
                "agerec": inputs["agerec"],
                "pardm": pardm,
                "agedx": agedx,
                "hba1c": hba1c,
                "bmi": None,
                "insoroha": None
            })
            scenario_id += 1

    # T2
    if has_t2:
        for (pardm, agedx, hba1c, bmi, insoroha) in itertools.product(
            inputs["pardm"], inputs["agedx"], inputs["hba1c"], inputs["bmi"], inputs["insoroha"]
        ):
            scenarios.append({
                "scenario_id": scenario_id,
                "t1t2": 2,
                "sex": inputs["sex"],
                "agerec": inputs["agerec"],
                "pardm": pardm,
                "agedx": agedx,
                "hba1c": hba1c,
                "bmi": bmi,
                "insoroha": insoroha
            })
            scenario_id += 1

    return scenarios
