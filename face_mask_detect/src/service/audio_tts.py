from gtts import gTTS
from pathlib import Path

def generate_no_mask_sound():
    sound_path = Path("src/assets/Please_wear_a_face_mask.mp3")
    tts = gTTS("Please wear a face mask", lang='en')
    tts.save(sound_path)
    print(f"Sound saved at: {sound_path.resolve()}")

generate_no_mask_sound()

def generate_mask_found_sound():
    sound_path = Path("src/assets/Thank_you_for_wearing_a_mask.mp3")
    tts = gTTS("Thank you for wearing your mask properly", lang='en')
    tts.save(sound_path)
    print(f"Sound saved at: {sound_path.resolve()}")
    
generate_mask_found_sound()

