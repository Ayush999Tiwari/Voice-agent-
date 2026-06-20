from text_to_speech_for_client import speak_tamil
from whisper_test import run as whisper_test
from salesperson import run as salesperson_speaks
from translatetotamil import translatetotamil
def main():
    try :  
      print("tamil to english")
      client_result = whisper_test()
      if client_result is None:
         print (" check your whisper.py ")
         return None
      tamil_text=client_result["text"]
      english_text=client_result["english_text"]
    
    except RuntimeError as e:
      print(" No audio captured. Check your microphone.")  
      return None
    except Exception as e:
      print(f"[whisper.py got failed] unexpected error")
      return None
    try :
        salesperson_result=salesperson_speaks(english_text)
        english_reply=salesperson_result["text"]
        print(f"Salesperson (English): {english_reply}")
    except KeyError as e:
       print("  Check that salesperson.py"   ) 
    try: 
      tamil_reply= translatetotamil(english_reply)
      if not tamil_reply or not isinstance(tamil_reply, str):
         raise ValueError(f"translatetotamil() returned invalid output: {tamil_reply!r}")
      print(f" Salesperson (Tamil): {tamil_reply}")
    except Exception as e:
        print("Check translatetotamil() function and translation API/model")
        return None  
    print(f" Client (Tamil) : {tamil_text}")
    print(f" Client (English) : {english_text}")
    print(f" Salesperson (English) : {english_reply}")
    print(f" Salesperson (Tamil) : {tamil_reply}")
    try: 
      speak_tamil(tamil_reply)
    except Exception as e:
       print(" Check speak_tamil() function, audio device, or TTS model")   
    result =  {
        "client_tamil": tamil_text,
        "client_english": english_text,
        "salesperson_english": english_reply,
        "salesperson_tamil": tamil_reply,
    }
    for key , value in result.items():
       print(f"{key}: {value}")
    return result   
if __name__ == "__main__":
    main()