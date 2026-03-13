import tkinter as tk
from tkinter import ttk
import os

# Importam clasa noastra din fisierul separat!
from sound_manager import SoundManager

class BJJTimerTouch:
    def __init__(self, root):
        self.root = root
        self.root.title("BJJ Interval Timer Touch Pro - Nova Squad")
        
        # Initializam Managerul de Sunete extern
        self.sound_manager = SoundManager(os.path.dirname(__file__))
        
        # Fullscreen
        self.root.attributes('-fullscreen', True)
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)
        
        self.root.configure(bg='#1a1a1a')
        
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
        self.prep_time = 12  # Timp de pregatire in secunde (10 secunde + 2 secunde buffer) 
        
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
        # AICI RAMANE EXACT ACELASI COD GRAFIC PE CARE IL AVEAI
        # Nu am modificat nicio linie de UI, ca sa arate exact la fel
        
        top_frame = tk.Frame(self.root, bg='#2a2a2a', padx=15, pady=15)
        top_frame.pack(fill=tk.X, pady=10)
        tk.Label(top_frame, text="SELECTEAZA PRESET:", font=("Arial", 14, "bold"), fg="#FFD700", bg='#2a2a2a').pack(side=tk.LEFT, anchor=tk.W)
        tk.Label(top_frame, text="", bg='#2a2a2a').pack(side=tk.LEFT, expand=True)
        tk.Label(top_frame, text="NOVA SQUAD", font=("Arial", 20, "bold"), fg="#FF6B00", bg='#2a2a2a').pack(side=tk.RIGHT, padx=20)
        
        preset_buttons_frame = tk.Frame(self.root, bg='#2a2a2a', padx=15, pady=10)
        preset_buttons_frame.pack(fill=tk.X)
        for preset_name in self.presets.keys():
            btn = tk.Button(preset_buttons_frame, text=preset_name, font=("Arial", 11, "bold"),
                           bg='#4CAF50', fg='white', padx=15, pady=10, 
                           command=lambda p=preset_name: self.load_preset(p),
                           relief=tk.RAISED, bd=2, cursor="hand2",
                           activebackground='#45a049', activeforeground='white')
            btn.pack(side=tk.LEFT, padx=5)
        
        settings_frame = tk.Frame(self.root, bg='#2a2a2a', padx=15, pady=10)
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(settings_frame, text="SETARI PERSONALIZATE:", font=("Arial", 12, "bold"), fg="#FFD700", bg='#2a2a2a').pack(anchor=tk.W)
        
        times_frame = tk.Frame(settings_frame, bg='#2a2a2a')
        times_frame.pack(fill=tk.X, pady=10)
        
        work_box = tk.Frame(times_frame, bg='#333333', padx=15, pady=10, relief=tk.RAISED, bd=2)
        work_box.pack(side=tk.LEFT, padx=10)
        tk.Label(work_box, text="TIMP LUPTA (min)", font=("Arial", 11, "bold"), fg="#00FF00", bg='#333333').pack()
        work_inner = tk.Frame(work_box, bg='#333333')
        work_inner.pack()
        tk.Button(work_inner, text="−", font=("Arial", 16, "bold"), bg='#FF6B6B', fg='white', width=3, command=self.decrease_work, cursor="hand2").pack(side=tk.LEFT, padx=5)
        self.work_label = tk.Label(work_inner, text=f"{self.work_time//60}", font=("Arial", 20, "bold"), fg="#00FF00", bg='#333333', width=5)
        self.work_label.pack(side=tk.LEFT, padx=10)
        tk.Button(work_inner, text="+", font=("Arial", 16, "bold"), bg='#4CAF50', fg='white', width=3, command=self.increase_work, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        rest_box = tk.Frame(times_frame, bg='#333333', padx=15, pady=10, relief=tk.RAISED, bd=2)
        rest_box.pack(side=tk.LEFT, padx=10)
        tk.Label(rest_box, text="TIMP PAUZA (min)", font=("Arial", 11, "bold"), fg="#FF4444", bg='#333333').pack()
        rest_inner = tk.Frame(rest_box, bg='#333333')
        rest_inner.pack()
        tk.Button(rest_inner, text="−", font=("Arial", 16, "bold"), bg='#FF6B6B', fg='white', width=3, command=self.decrease_rest, cursor="hand2").pack(side=tk.LEFT, padx=5)
        self.rest_label = tk.Label(rest_inner, text=f"{self.rest_time//60}", font=("Arial", 20, "bold"), fg="#FF4444", bg='#333333', width=5)
        self.rest_label.pack(side=tk.LEFT, padx=10)
        tk.Button(rest_inner, text="+", font=("Arial", 16, "bold"), bg='#4CAF50', fg='white', width=3, command=self.increase_rest, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        rounds_box = tk.Frame(times_frame, bg='#333333', padx=15, pady=10, relief=tk.RAISED, bd=2)
        rounds_box.pack(side=tk.LEFT, padx=10)
        tk.Label(rounds_box, text="NR. RUNDE", font=("Arial", 11, "bold"), fg="#00FFFF", bg='#333333').pack()
        rounds_inner = tk.Frame(rounds_box, bg='#333333')
        rounds_inner.pack()
        tk.Button(rounds_inner, text="−", font=("Arial", 16, "bold"), bg='#FF6B6B', fg='white', width=3, command=self.decrease_rounds, cursor="hand2").pack(side=tk.LEFT, padx=5)
        self.rounds_label = tk.Label(rounds_inner, text=f"{self.total_rounds}", font=("Arial", 20, "bold"), fg="#00FFFF", bg='#333333', width=5)
        self.rounds_label.pack(side=tk.LEFT, padx=10)
        tk.Button(rounds_inner, text="+", font=("Arial", 16, "bold"), bg='#4CAF50', fg='white', width=3, command=self.increase_rounds, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        self.time_label = tk.Label(main_frame, text="00:00", font=("Digital-7", 300, "bold"), fg="#00FF00", bg='#1a1a1a')
        self.time_label.pack(expand=True)
        self.info_label = tk.Label(main_frame, text="APASA START PENTRU A INCEPE", font=("Arial", 40, "bold"), fg="white", bg='#1a1a1a')
        self.info_label.pack(pady=20)
        
        control_frame = tk.Frame(self.root, bg='#2a2a2a', padx=20, pady=20)
        control_frame.pack(fill=tk.X)
        
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
            self.sound_manager.play('none', 1000, 100)

    def increase_work(self):
        if self.state == "IDLE" and self.work_time < 30*60:
            self.work_time += 60
            self.work_label.config(text=f"{self.work_time//60}")
            self.sound_manager.play('none', 800, 50)

    def decrease_work(self):
        if self.state == "IDLE" and self.work_time > 60:
            self.work_time -= 60
            self.work_label.config(text=f"{self.work_time//60}")
            self.sound_manager.play('none', 600, 50)

    def increase_rest(self):
        if self.state == "IDLE" and self.rest_time < 5*60:
            self.rest_time += 60
            self.rest_label.config(text=f"{self.rest_time//60}")
            self.sound_manager.play('none', 800, 50)

    def decrease_rest(self):
        if self.state == "IDLE" and self.rest_time > 60:
            self.rest_time -= 60
            self.rest_label.config(text=f"{self.rest_time//60}")
            self.sound_manager.play('none', 600, 50)

    def increase_rounds(self):
        if self.state == "IDLE" and self.total_rounds < 20:
            self.total_rounds += 1
            self.rounds_label.config(text=f"{self.total_rounds}")
            self.sound_manager.play('none', 800, 50)

    def decrease_rounds(self):
        if self.state == "IDLE" and self.total_rounds > 1:
            self.total_rounds -= 1
            self.rounds_label.config(text=f"{self.total_rounds}")
            self.sound_manager.play('none', 600, 50)

    def toggle_timer(self):
        if self.state == "IDLE":
            self.state = "PREPARE"
            self.current_round = 1
            self.time_left = self.prep_time
            self.is_paused = False
            self.warning_sounded = False
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.status_label.config(text="Status: Pregatire - Treci pe saltea LAPTE PRAF!")
            
            self.sound_manager.play('prepare', 800, 100)
            self.update_ui_colors()
            
        elif self.state == "FINISHED":
            self.reset_timer()

    def toggle_pause(self):
        if self.state not in ["IDLE", "FINISHED"]:
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.pause_button.config(text="▶ CONTINUA", bg='#4CAF50')
                self.status_label.config(text="Status: PAUZA - Apasă CONTINUA pentru a relua")
                self.sound_manager.play('none', 600, 100)
            else:
                self.pause_button.config(text="⏸ PAUZA", bg='#FFA500')
                self.warning_sounded = False
                self.status_label.config(text="Status: RULARE - Apasă PAUZA pentru a face pauza")
                self.update_ui_colors()
                self.sound_manager.play('none', 800, 100)

    def update_ui_colors(self):
        if self.state == "PREPARE":
            self.time_label.config(fg="#FFFF00")
            self.info_label.config(text="PREGATIRE - Treci pe saltea LAPTE PRAF!", fg="#FFFF00")
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
        self.sound_manager.play('none', 1200, 150)

    def update_clock(self):
        if not self.is_paused and self.state not in ["IDLE", "FINISHED"]:
            self.time_left -= 1
            
            if self.time_left == 10 and not self.warning_sounded and self.state == "WORK":
                self.warning_sounded = True
                self.sound_manager.play('warning', 1000, 150)
                self.info_label.config(text=f"RUNDA {self.current_round}/{self.total_rounds} -ULTIMILE 10!", fg="#FFB700")
            
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
            self.sound_manager.play('work', 1200, 200)
            
        elif self.state == "WORK":
            if self.current_round < self.total_rounds:
                self.state = "REST"
                self.time_left = self.rest_time
                self.warning_sounded = False
                self.sound_manager.play('rest', 800, 300)
            else:
                self.state = "FINISHED"
                self.time_label.config(text="00:00", fg="#00FFFF")
                self.info_label.config(text="ANTRENAMENT TERMINAT - OSS!", fg="#00FFFF")
                self.status_label.config(text="Status: Training complete - BRAVO!")
                self.start_button.config(state=tk.NORMAL)
                self.pause_button.config(state=tk.DISABLED)
                self.sound_manager.play('finished', 1500, 500)
                return
                
        elif self.state == "REST":
            self.current_round += 1
            self.state = "WORK"
            self.time_left = self.work_time
            self.warning_sounded = False
            self.sound_manager.play('work', 1200, 200)
        
        self.update_ui_colors()

    def toggle_fullscreen(self, event=None):
        current = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current)

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)

if __name__ == "__main__":
    root = tk.Tk()
    app = BJJTimerTouch(root)
    root.mainloop()