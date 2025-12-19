import json
import traceback
from groq import Groq
from config.settings import GROQ_API_KEY, MODEL_NAME
from tools.eligibility import check_eligibility, get_scheme_details
from tools.application import apply_for_scheme  # <--- IMPORT NEW TOOL

if not GROQ_API_KEY:
    print("❌ CRITICAL ERROR: GROQ API Key is missing in .env!")
    client = None
else:
    client = Groq(api_key=GROQ_API_KEY)

# --- UPDATED TOOLS SCHEMA ---
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "check_eligibility",
            "description": "Check which schemes a user is eligible for based on demographics.",
            "parameters": {
                "type": "object",
                "properties": {
                    "age": {"type": "integer"},
                    "income": {"type": "integer"},
                    "occupation": {"type": "string"}
                },
                "required": ["age", "income", "occupation"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_scheme_details",
            "description": "Get details of a specific scheme.",
            "parameters": {
                "type": "object",
                "properties": {
                    "scheme_name_keyword": {"type": "string"}
                },
                "required": ["scheme_name_keyword"]
            }
        }
    },
    # --- NEW TOOL ADDED HERE ---
    {
        "type": "function",
        "function": {
            "name": "apply_for_scheme",
            "description": "Submit an application for a chosen scheme.",
            "parameters": {
                "type": "object",
                "properties": {
                    "scheme_name": {"type": "string", "description": "Name of the scheme to apply for"},
                    "applicant_name": {"type": "string", "description": "Full name of the user"},
                    "mobile_number": {"type": "string", "description": "10 digit mobile number"}
                },
                "required": ["scheme_name", "applicant_name", "mobile_number"]
            }
        }
    }
]

def get_llm_response(messages):
    if not client:
        return "System Error: API Key missing.", messages

    try:
        print(f"🧠 Thinking...")
        
        # 1. First Call: Planner
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS_SCHEMA,
            tool_choice="auto",
            temperature=0.6,
            max_tokens=1024
        )
        
        response_msg = response.choices[0].message
        tool_calls = response_msg.tool_calls

        # 2. Check if Tool is called
        if tool_calls:
            messages.append(response_msg)
            
            for tool_call in tool_calls:
                fn_name = tool_call.function.name
                try:
                    args = json.loads(tool_call.function.arguments)
                except:
                    args = {}

                print(f"🔧 Tool Triggered: {fn_name} | Args: {args}")
                
                # --- TOOL EXECUTION LOGIC ---
                if fn_name == "check_eligibility":
                    result = check_eligibility(
                        age=args.get("age", 0), 
                        income=args.get("income", 0), 
                        occupation=args.get("occupation", "unknown")
                    )
                elif fn_name == "get_scheme_details":
                    result = get_scheme_details(args.get("scheme_name_keyword", ""))
                    
                # --- NEW TOOL EXECUTION ---
                elif fn_name == "apply_for_scheme":
                    result = apply_for_scheme(
                        scheme_name=args.get("scheme_name", ""),
                        applicant_name=args.get("applicant_name", ""),
                        mobile_number=str(args.get("mobile_number", ""))
                    )
                else:
                    result = "Error: Tool function not found."
                
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": fn_name,
                    "content": str(result)
                })

            # 3. Second Call: Synthesizer
            final_response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages
            )
            return final_response.choices[0].message.content, messages

        return response_msg.content, messages

    except Exception as e:
        print(f"\n❌ GROQ API ERROR: {e}")
        traceback.print_exc()
        return "क्षमा करें, सर्वर में कुछ समस्या है।", messages