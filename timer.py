import tkinter as tk
from tkinter import ttk
import winsound
import os
import sys

# Încercăm să importăm pygame pentru sunetele personalizate
try:
    import pygame
    PYGAME_AVAILABLE = True
    pygame.mixer.init()
except (ImportError, Exception):
    PYGAME_AVAILABLE = False

class BJJTimerTouch:
    def __init__(self, root):
        self.root = root
        self.root.title("BJJ Interval Timer Touch Pro - Nova Squad")
        
        # Fullscreen TRUE
        self.root.attributes('-fullscreen', True)
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)
        
        self.root.configure(bg='#1a1a1a')
        
        # Path-ul folderului cu sunete personalizate
        self.sounds_dir = os.path.join(os.path.dirname(__file__), 'sounds')
        
        # --- PRESETARI BJJ OFICIALE ---
        self.presets = {
            "Adult Gi (8m)": {"work": 8*60, "rest": 1*60, "rounds": 5},
            "Adult Gi (10m)": {"work": 10*60, "rest": 1*60, "rounds": 5},
            "No-Gi (10m)": {"work": 10*60, "rest": 1*60, "rounds": 5},
            "Competition": {"work": 10*60, "rest": 2*60, "rounds": 3},
            "Submission Only": {"work": 15*60, "rest": 1*60, "rounds": 3},
            "Training": {"work": 5*60, "rest": 1*60, "rounds": 5},
        }
        
        # --- SETARI ANTRENAMENT ---
        self.work_time = self.presets["Training"]["work"]
        self.rest_time = self.presets["Training"]["rest"]
        self.total_rounds = self.presets["Training"]["rounds"]
        self.prep_time = 10
        
        # --- STARI ---
        self.state = "IDLE"
        self.current_round = 1
        self.time_left = 0
        self.is_paused = False
        self.warning_sounded = False
        
        # --- INTERFATA GRAFICA ---
        self.create_ui()
        
        # Pornim ceasul
        self.update_clock()

    def create_ui(self):
        # ===== FRAME TOP cu TITLU NOVA SQUAD =====
        header_frame = tk.Frame(self.root, bg='#1a1a1a', padx=15, pady=10)
        header_frame.pack(fill=tk.X)
        
        # Spacer pe stânga
        tk.Label(header_frame, text="", bg='#1a1a1a').pack(side=tk.LEFT, expand=True)
        
        # Titlu NOVA SQUAD pe dreapta
        tk.Label(header_frame, text="NOVA SQUAD", font=("Arial", 32, "bold"), fg="#FF6B00", bg='#1a1a1a').pack(side=tk.RIGHT, padx=30)
        
        # ===== FRAME SUPERIOR - PRESETARI =====
        top_frame = tk.Frame(self.root, bg='#2a2a2a', padx=15, pady=15)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(top_frame, text="SELECTEAZA PRESET:", font=("Arial", 14, "bold"), fg="#FFD700", bg='#2a2a2a').pack(anchor=tk.W, pady=(0, 10))
        
        preset_buttons_frame = tk.Frame(top_frame, bg='#2a2a2a')
        preset_buttons_frame.pack(fill=tk.X)
        
        self.preset_var = tk.StringVar(value="Training")
        
        for preset_name in self.presets.keys():
            btn = tk.Button(preset_buttons_frame, text=preset_name, font=("Arial", 11, "bold"),
                           bg='#4CAF50', fg='white', padx=15, pady=10, 
                           command=lambda p=preset_name: self.load_preset(p),
                           relief=tk.RAISED, bd=2, cursor="hand2",
                           activebackground='#45a049', activeforeground='white')
            btn.pack(side=tk.LEFT, padx=5)
        
        # ===== FRAME CENTRALE - SETARI CUSTOM =====
        settings_frame = tk.Frame(self.root, bg='#2a2a2a', padx=15, pady=10)
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(settings_frame, text="SETARI PERSONALIZATE:", font=("Arial", 12, "bold"), fg="#FFD700", bg='#2a2a2a').pack(anchor=tk.W)
        
        # Row-ul cu timpi
        times_frame = tk.Frame(settings_frame, bg='#2a2a2a')
        times_frame.pack(fill=tk.X, pady=10)
        
        # Lupta
        work_box = tk.Frame(times_frame, bg='#333333', padx=15, pady=10, relief=tk.RAISED, bd=2)
        work_box.pack(side=tk.LEFT, padx=10)
        
        tk.Label(work_box, text="TIMP LUPTA (min)", font=("Arial", 11, "bold"), fg="#00FF00", bg='#333333').pack()
        work_inner = tk.Frame(work_box, bg='#333333')
        work_inner.pack()
        tk.Button(work_inner, text="−", font=("Arial", 16, "bold"), bg='#FF6B6B', fg='white', 
                 width=3, command=self.decrease_work, cursor="hand2").pack(side=tk.LEFT, padx=5)
        self.work_label = tk.Label(work_inner, text=f"{self.work_time//60}", font=("Arial", 20, "bold"), 
                                   fg="#00FF00", bg='#333333', width=5)
        self.work_label.pack(side=tk.LEFT, padx=10)
        tk.Button(work_inner, text="+", font=("Arial", 16, "bold"), bg='#4CAF50', fg='white', 
                 width=3, command=self.increase_work, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        # Pauza
        rest_box = tk.Frame(times_frame, bg='#333333', padx=15, pady=10, relief=tk.RAISED, bd=2)
        rest_box.pack(side=tk.LEFT, padx=10)
        
        tk.Label(rest_box, text="TIMP PAUZA (min)", font=("Arial", 11, "bold"), fg="#FF4444", bg='#333333').pack()
        rest_inner = tk.Frame(rest_box, bg='#333333')
        rest_inner.pack()
        tk.Button(rest_inner, text="−", font=("Arial", 16, "bold"), bg='#FF6B6B', fg='white', 
                 width=3, command=self.decrease_rest, cursor="hand2").pack(side=tk.LEFT, padx=5)
        self.rest_label = tk.Label(rest_inner, text=f"{self.rest_time//60}", font=("Arial", 20, "bold"), 
                                   fg="#FF4444", bg='#333333', width=5)
        self.rest_label.pack(side=tk.LEFT, padx=10)
        tk.Button(rest_inner, text="+", font=("Arial", 16, "bold"), bg='#4CAF50', fg='white', 
                 width=3, command=self.increase_rest, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        # Runde
        rounds_box = tk.Frame(times_frame, bg='#333333', padx=15, pady=10, relief=tk.RAISED, bd=2)
        rounds_box.pack(side=tk.LEFT, padx=10)
        
        tk.Label(rounds_box, text="NR. RUNDE", font=("Arial", 11, "bold"), fg="#00FFFF", bg='#333333').pack()
        rounds_inner = tk.Frame(rounds_box, bg='#333333')
        rounds_inner.pack()
        tk.Button(rounds_inner, text="−", font=("Arial", 16, "bold"), bg='#FF6B6B', fg='white', 
                 width=3, command=self.decrease_rounds, cursor="hand2").pack(side=tk.LEFT, padx=5)
        self.rounds_label = tk.Label(rounds_inner, text=f"{self.total_rounds}", font=("Arial", 20, "bold"), 
                                     fg="#00FFFF", bg='#333333', width=5)
        self.rounds_label.pack(side=tk.LEFT, padx=10)
        tk.Button(rounds_inner, text="+", font=("Arial", 16, "bold"), bg='#4CAF50', fg='white', 
                 width=3, command=self.increase_rounds, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        # ===== FRAME PRINCIPAL - TIMER MARE =====
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Timer mare pe centru
        self.time_label = tk.Label(main_frame, text="00:00", font=("Digital-7", 300, "bold"), 
                                   fg="#00FF00", bg='#1a1a1a')
        self.time_label.pack(expand=True)
        
        # Info sub timer
        self.info_label = tk.Label(main_frame, text="APASA START PENTRU A INCEPE", 
                                  font=("Arial", 40, "bold"), fg="white", bg='#1a1a1a')
        self.info_label.pack(pady=20)
        
        # ===== FRAME JOS - CONTROALE PRINCIPALE =====
        control_frame = tk.Frame(self.root, bg='#2a2a2a', padx=20, pady=20)
        control_frame.pack(fill=tk.X)
        
        # Butoane mari pentru control
        control_buttons = tk.Frame(control_frame, bg='#2a2a2a')
        control_buttons.pack(fill=tk.X, pady=10)
        
        self.start_button = tk.Button(control_buttons, text="▶ START", font=("Arial", 20, "bold"),
                                     bg='#4CAF50', fg='white', padx=60, pady=25,
                                     command=self.toggle_timer, relief=tk.RAISED, bd=4,
                                     cursor="hand2", activebackground='#45a049', activeforeground='white')
        self.start_button.pack(side=tk.LEFT, padx=15)
        
        self.pause_button = tk.Button(control_buttons, text="⏸ PAUZA", font=("Arial", 20, "bold"),
                                     bg='#FFA500', fg='white', padx=60, pady=25,
                                     command=self.toggle_pause, relief=tk.RAISED, bd=4,
                                     cursor="hand2", activebackground='#FF8C00', activeforeground='white',
                                     state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=15)
        
        self.reset_button = tk.Button(control_buttons, text="↻ RESET", font=("Arial", 20, "bold"),
                                     bg='#FF6B6B', fg='white', padx=60, pady=25,
                                     command=self.reset_timer, relief=tk.RAISED, bd=4,
                                     cursor="hand2", activebackground='#FF5252', activeforeground='white')
        self.reset_button.pack(side=tk.LEFT, padx=15)
        
        # Status bar
        self.status_label = tk.Label(control_frame, text="Status: Ready - Selectează preset și apasă START", 
                                    font=("Arial", 12, "bold"), fg="#FFD700", bg='#2a2a2a')
        self.status_label.pack(side=tk.LEFT, pady=10)

    def load_preset(self, preset_name):
        if self.state == "IDLE":
            preset = self.presets[preset_name]
            self.work_time = preset["work"]
            self.rest_time = preset["rest"]
            self.total_rounds = preset["rounds"]
            
            self.work_label.config(text=f"{self.work_time//60}")
            self.rest_label.config(text=f"{self.rest_time//60}")
            self.rounds_label.config(text=f"{self.total_rounds}")
            
            self.status_label.config(text=f"Status: Preset {preset_name} încărcat - Gata de start!")
            self.play_sound(1000, 100, 'start_session.wav')

    def increase_work(self):
        if self.state == "IDLE" and self.work_time < 30*60:
            self.work_time += 60
            self.work_label.config(text=f"{self.work_time//60}")
            self.play_sound(800, 50)

    def decrease_work(self):
        if self.state == "IDLE" and self.work_time > 60:
            self.work_time -= 60
            self.work_label.config(text=f"{self.work_time//60}")
            self.play_sound(600, 50)

    def increase_rest(self):
        if self.state == "IDLE" and self.rest_time < 5*60:
            self.rest_time += 60
            self.rest_label.config(text=f"{self.rest_time//60}")
            self.play_sound(800, 50)

    def decrease_rest(self):
        if self.state == "IDLE" and self.rest_time > 60:
            self.rest_time -= 60
            self.rest_label.config(text=f"{self.rest_time//60}")
            self.play_sound(600, 50)

    def increase_rounds(self):
        if self.state == "IDLE" and self.total_rounds < 20:
            self.total_rounds += 1
            self.rounds_label.config(text=f"{self.total_rounds}")
            self.play_sound(800, 50)

    def decrease_rounds(self):
        if self.state == "IDLE" and self.total_rounds > 1:
            self.total_rounds -= 1
            self.rounds_label.config(text=f"{self.total_rounds}")
            self.play_sound(600, 50)

    def toggle_timer(self):
        if self.state == "IDLE":
            self.state = "PREPARE"
            self.current_round = 1
            self.time_left = self.prep_time
            self.is_paused = False
            self.warning_sounded = False
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.status_label.config(text="Status: Pregatire - Pana jos!")
            self.play_sound(800, 100, 'start_session.wav')
            self.update_ui_colors()
        elif self.state == "FINISHED":
            self.reset_timer()

    def toggle_pause(self):
        if self.state not in ["IDLE", "FINISHED"]:
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.pause_button.config(text="▶ CONTINUA", bg='#4CAF50')
                self.status_label.config(text="Status: PAUZA - Apasă CONTINUA pentru a relua")
                self.play_sound(600, 100)
            else:
                self.pause_button.config(text="⏸ PAUZA", bg='#FFA500')
                self.warning_sounded = False
                self.status_label.config(text="Status: RULARE - Apasă PAUZA pentru a face pauza")
                self.update_ui_colors()
                self.play_sound(800, 100)

    def update_ui_colors(self):
        if self.state == "PREPARE":
            self.time_label.config(fg="#FFFF00")
            self.info_label.config(text="PREGATIRE - PANA JOS!", fg="#FFFF00")
        elif self.state == "WORK":
            self.time_label.config(fg="#00FF00")
            self.info_label.config(text=f"RUNDA {self.current_round}/{self.total_rounds} - LUPTA!", fg="#00FF00")
            self.status_label.config(text=f"Status: RULARE - Runda {self.current_round}/{self.total_rounds}")
        elif self.state == "REST":
            self.time_label.config(fg="#FF4444")
            self.info_label.config(text=f"RUNDA {self.current_round}/{self.total_rounds} - PAUZA", fg="#FF4444")
            self.status_label.config(text=f"Status: PAUZA - Runda {self.current_round}/{self.total_rounds}")

    def reset_timer(self):
        self.state = "IDLE"
        self.current_round = 1
        self.time_left = 0
        self.is_paused = False
        self.warning_sounded = False
        self.time_label.config(text="00:00", fg="#00FF00")
        self.info_label.config(text="APASA START PENTRU A INCEPE", fg="white")
        self.status_label.config(text="Status: Reset - Gata pentru noua sesiune")
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED, text="⏸ PAUZA")
        self.play_sound(1200, 150)

    def update_clock(self):
        if not self.is_paused and self.state not in ["IDLE", "FINISHED"]:
            self.time_left -= 1
            
            if self.time_left == 10 and not self.warning_sounded and self.state == "WORK":
                self.warning_sounded = True
                self.play_sound(1000, 150, 'countdown_10sec.wav')
                self.info_label.config(text=f"RUNDA {self.current_round}/{self.total_rounds} - ÚLTIMOS 10!", fg="#FFB700")
            
            if self.time_left <= 0:
                self.next_state()

        if self.state != "IDLE" and self.state != "FINISHED":
            mins, secs = divmod(max(0, self.time_left), 60)
            self.time_label.config(text=f"{mins:02d}:{secs:02d}")

        self.root.after(1000, self.update_clock)

    def next_state(self):
        if self.state == "PREPARE":
            self.state = "WORK"
            self.time_left = self.work_time
            self.warning_sounded = False
            self.play_sound(1200, 200, 'start_work.wav')
        elif self.state == "WORK":
            if self.current_round < self.total_rounds:
                self.state = "REST"
                self.time_left = self.rest_time
                self.warning_sounded = False
                self.play_sound(800, 300, 'start_rest.wav')
            else:
                self.state = "FINISHED"
                self.time_label.config(text="00:00", fg="#00FFFF")
                self.info_label.config(text="ANTRENAMENT TERMINAT - OSS!", fg="#00FFFF")
                self.status_label.config(text="Status: Training complete - BRAVO!")
                self.start_button.config(state=tk.NORMAL)
                self.pause_button.config(state=tk.DISABLED)
                self.play_sound(1500, 500, 'finished.wav')
                return
        elif self.state == "REST":
            self.current_round += 1
            self.state = "WORK"
            self.time_left = self.work_time
            self.warning_sounded = False
            self.play_sound(1200, 200, 'start_work.wav')
        
        self.update_ui_colors()

    def play_sound(self, frequency, duration, sound_name=None):
        """
        Joacă un sunet personalizat din folderul sounds/ sau un ton implicit
        """
        if sound_name and PYGAME_AVAILABLE:
            sound_path = os.path.join(self.sounds_dir, sound_name)
            if os.path.exists(sound_path):
                try:
                    pygame.mixer.Sound(sound_path).play()
                    return
                except Exception as e:
                    pass
        
        if frequency > 0 and duration > 0:
            try:
                winsound.Beep(frequency, duration)
            except:
                pass

    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen with F11"""
        current = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current)

    def exit_fullscreen(self, event=None):
        """Exit fullscreen with ESC"""
        self.root.attributes('-fullscreen', False)

if __name__ == "__main__":
    root = tk.Tk()
    app = BJJTimerTouch(root)
    root.mainloop()
