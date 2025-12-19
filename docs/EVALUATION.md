# Evaluation Transcript

## Scenario 1: Successful Happy Path (Farmer)
**Objective:** User wants a farming scheme.
- **User:** "Namaste, main ek kisan hoon."
- **Agent:** "Namaste! Main kisanon ki madad kar sakti hoon. Aapki umar kya hai?" (Correctly identifies missing slot: Age)
- **User:** "Meri umar 45 saal hai."
- **Agent:** "Aur aapki saalan aamdani (income) kitni hai?" (Correctly identifies missing slot: Income)
- **User:** "Do lakh rupaye."
- **Internal Log:** `Tool Triggered: check_eligibility | Args: {'age': 45, 'income': 200000, 'occupation': 'kisan'}`
- **Agent:** "Aap 'PM Kisan Samman Nidhi' aur 'Fasal Bima Yojana' ke liye patra hain."
- **Result:** ✅ PASS

## Scenario 2: Edge Case (High Income)
**Objective:** Test eligibility logic rejection.
- **User:** "Main scheme chahta hoon. Meri income 50 Lakh hai aur main businessman hoon."
- **Agent:** (Calls tool) -> Tool returns "No eligible schemes".
- **Agent:** "Maaf kijiye, aapki aay (income) seema se adhik hone ke kaaran abhi koi yojana uplabdh nahi hai."
- **Result:** ✅ PASS (Correctly handled rejection gracefully)

## Scenario 3: Failure & Recovery (Noise)
**Objective:** Test speech recognition failure.
- **User:** (Mumbling/Silence) "..."
- **Agent:** "Maaf kijiye, main sun nahi payi. Kripya dobara bole?"
- **User:** (Speaks clearly) "PM Awas Yojana kya hai?"
- **Agent:** (Calls `get_scheme_details`) "PM Awas Yojana mein ghar banane ke liye subsidy milti hai."
- **Result:** ✅ PASS (Recovered from silence)