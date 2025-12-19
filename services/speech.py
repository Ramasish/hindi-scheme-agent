import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import time
from colorama import Fore

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"{Fore.YELLOW}🎤 सुन रहा हूँ (Listening)...{Fore.RESET}")
        
        # --- OPTIMIZED SETTINGS FOR DEMO ---
        
        # 1. REMOVED fixed energy_threshold (Let it detect automatically)
        # This was causing the "50 Lakh" -> "50" cutoff issue.
        r.dynamic_energy_threshold = True
        
        # 2. INCREASED Pause Threshold
        # Wait 1.2 seconds of silence before thinking you are done.
        # This prevents cutting you off if you pause slightly between "50" and "Lakh".
        r.pause_threshold = 1.2  
        
        # 3. Ambient Noise Calibration
        # Short calibration to set the baseline
        r.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            # Increased phrase_time_limit to ensure long sentences aren't cut
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
            
            print(f"{Fore.CYAN}⏳ Processing...{Fore.RESET}")
            text = r.recognize_google(audio, language="hi-IN")
            print(f"{Fore.GREEN}👤 User: {text}{Fore.RESET}")
            return text
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except Exception as e:
            print(f"Microphone Error: {e}")
            return None

def speak(text):
    if not text: return
    print(f"{Fore.MAGENTA}🤖 Agent: {text}{Fore.RESET}")
    
    try:
        pygame.mixer.init()
        tts = gTTS(text=text, lang='hi', slow=False)
        filename = "temp_voice.mp3"
        tts.save(filename)
        
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.quit()
        os.remove(filename)
    except Exception as e:
        print(f"TTS Error: {e}")