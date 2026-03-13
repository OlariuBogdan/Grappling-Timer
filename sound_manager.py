import os
import winsound

class SoundManager:
    def __init__(self, root_path):
        self.sounds_dir = os.path.join(root_path, 'sounds')
        self.pygame_available = False
        self.audio_tracks = {}
        
        # =========================================================
        # AICI MODIFICI ASOCIEREA DINTRE EVENIMENT SI FISIERUL AUDIO
        # =========================================================
        self.sound_mapping = {
            'prepare': 'pregatire.mp3',   
            'work': 'start 2.mp3',          
            'rest': 'final.mp3',        
            'warning': 'start.mp3',       
            'finished': 'final.mp3'     
        }
        # =========================================================

        try:
            import pygame
            pygame.mixer.init()
            self.pygame_available = True
            self.load_all_sounds()
        except (ImportError, Exception) as e:
            print(f"[Avertisment] Pygame nu s-a incarcat. Folosim beep-uri de sistem. Eroare: {e}")

    def load_all_sounds(self):
        """Incarca sunetele in memorie pentru a elimina latenta."""
        import pygame
        for event, filename in self.sound_mapping.items():
            path = os.path.join(self.sounds_dir, filename)
            if os.path.exists(path):
                try:
                    self.audio_tracks[event] = pygame.mixer.Sound(path)
                except Exception as e:
                    print(f"Eroare la incarcarea fisierului {filename}: {e}")
            else:
                print(f"Lipseste fisierul din folderul sounds: {filename}")

    def play(self, event_name, fallback_freq=0, fallback_duration=0):
        """Reda sunetul. Daca pica ceva, face un Beep din Windows."""
        if self.pygame_available and event_name in self.audio_tracks:
            try:
                self.audio_tracks[event_name].play()
                return
            except Exception:
                pass
                
        if fallback_freq > 0 and fallback_duration > 0:
            try:
                winsound.Beep(fallback_freq, fallback_duration)
            except:
                pass