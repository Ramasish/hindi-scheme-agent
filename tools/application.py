import json
import random

def apply_for_scheme(scheme_name, applicant_name, mobile_number):
    """
    Simulates applying for a government scheme.
    """
    print(f"\n[Tool Logic] Submitting Application: {scheme_name} for {applicant_name} ({mobile_number})")
    
    # Generate a fake Application ID
    app_id = f"APP-{random.randint(1000, 9999)}-{mobile_number[-4:]}"
    
    return json.dumps({
        "status": "success",
        "message": f"Badhai ho! {scheme_name} ke liye aapka aavedan safal raha. Application ID: {app_id}."
    })