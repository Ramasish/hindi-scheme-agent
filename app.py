from services.speech import listen, speak
from agent.workflow import Agent
import sys
from colorama import Fore

def main():
    agent = Agent()
    
    # 1. Initial Greeting
    speak("नमस्ते! मैं आपकी सरकारी योजना सहायक हूँ। बताइए मैं आपकी क्या मदद कर सकती हूँ?")
    
    # Failure Counter
    fail_count = 0
    
    # 2. Event Loop
    while True:
        try:
            # A. Listen
            user_text = listen()
            
            # B. Handle Silence/Noise (Smart Failure Handling)
            if not user_text:
                fail_count += 1
                
                # If failed 2 times consecutively, ask user to speak up
                if fail_count >= 2:
                    print(f"{Fore.RED}⚠️ No input detected multiple times. Prompting user...{Fore.RESET}")
                    speak("माफ़ कीजिये, मुझे आपकी आवाज़ नहीं आ रही। कृपया थोड़ा ज़ोर से बोलें।")
                    fail_count = 0 # Reset counter
                continue 

            # Reset counter if we successfully heard something
            fail_count = 0

            # C. Exit Command
            if "band" in user_text or "ruk" in user_text or "bye" in user_text.lower():
                speak("धन्यवाद। नमस्ते!")
                break
                
            # D. Agent Process (Reasoning + Tools)
            response = agent.process_turn(user_text)
            
            # E. Speak Result
            speak(response)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)

if __name__ == "__main__":
    main()