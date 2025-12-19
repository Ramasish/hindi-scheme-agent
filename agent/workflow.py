# agent/workflow.py
from config.prompts import SYSTEM_PROMPT
from services.llm import get_llm_response

class Agent:
    def __init__(self):
        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def process_turn(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        response_text, updated_messages = get_llm_response(self.messages)
        self.messages = updated_messages
        
        # Ensure we don't duplicate the assistant message in memory
        if self.messages[-1]["role"] != "assistant":
             self.messages.append({"role": "assistant", "content": response_text})
             
        return response_text