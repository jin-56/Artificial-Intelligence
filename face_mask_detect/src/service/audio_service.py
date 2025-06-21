from playsound import playsound
import threading
import os
from pathlib import Path

class AudioService:
    def __init__(self):
        self.assets_dir = Path(__file__).parent.parent / "assets"
        self.no_mask_path = str(self.assets_dir / "Please.wav")
        self.mask_found_path = str(self.assets_dir / "Thanks.wav")

    def _play_audio(self, file_path):
        if os.path.exists(file_path):
            threading.Thread(target=playsound, args=(file_path,), daemon=True).start()
        else:
            print(f"Audio file not found: {file_path}")

    def play_no_mask_warning(self):
        self._play_audio(self.no_mask_path)

    def play_mask_found_message(self):
        self._play_audio(self.mask_found_path)
