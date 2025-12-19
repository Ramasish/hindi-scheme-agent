import json
import os

def load_data():
    path = os.path.join(os.path.dirname(__file__), '../data/schemes.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def check_eligibility(age, income, occupation):
    """Logic tool to filter schemes"""
    schemes = load_data()
    eligible = []
    
    print(f"\n[Tool Logic] Checking: Age={age}, Income={income}, Occ={occupation}")
    
    for s in schemes:
        # Age Check
        if age < s["min_age"]: continue
        
        # Income Check
        if income > s["max_income"]: continue
        
        # Occupation Check
        is_occupation_match = False
        if "any" in s["occupation_match"]:
            is_occupation_match = True
        else:
            for accepted_occ in s["occupation_match"]:
                if accepted_occ.lower() in occupation.lower():
                    is_occupation_match = True
                    break
        
        if is_occupation_match:
            eligible.append(s["hindi_name"])

    if not eligible:
        return "No eligible schemes found."
    return f"Eligible Schemes: {', '.join(eligible)}"

def get_scheme_details(keyword):
    schemes = load_data()
    for s in schemes:
        if keyword.lower() in s["name"].lower() or keyword.lower() in s["hindi_name"].lower():
            return s["details"]
    return "Scheme details not found."