from tkinter import *
import time

class InfotainmentSystem(Tk):
    def __init__(self):
        super().__init__()

        self.title("IT")
        self.geometry("800x480")
        self.configure(bg="#1e1e1e")
        self.stations = ["FM 88.5", "FM 92.3", "FM 101.7", "FM 104.9"]
        self.station_index = 0
        self.volume = 10
        self.playing = True
        self.create_header()
        self.create_warning_panel()
        self.create_main_screen()
        self.create_status_bar()
        self.update_time()

    # ---------------- HEADER ----------------
    def create_header(self):
        header = Frame(self, bg="#2b2b2b", height=50)
        header.pack(fill="x")

        Label( header, text="🚗 MyCar Infotainment", fg="white", bg="#2b2b2b", font=("Helvetica", 16, "bold") ).pack(pady=10)

    # ---------------- WARNING PANEL ----------------
    def create_warning_panel(self):
        panel = Frame(self, bg="#1e1e1e", height=60)
        panel.pack(fill="x")

        self.warning_states = { "engine": False, "fuel": False, "battery": False, "temp": False }

        self.warning_labels = {}

        def create_warning(symbol, text, key, active_color):
            frame = Frame(panel, bg="#1e1e1e")
            frame.pack(side="left", padx=20)

            icon = Label( frame, text=symbol, font=("Helvetica", 22), fg="gray", bg="#1e1e1e" )
            icon.pack()

            label = Label( frame, text=text, font=("Helvetica", 8), fg="white", bg="#1e1e1e" )
            label.pack()

            icon.bind("<Button-1>", lambda e: self.toggle_warning(key))
            self.warning_labels[key] = (icon, active_color)

        create_warning("⚠", "ENGINE", "engine", "red")
        create_warning("⛽", "FUEL", "fuel", "yellow")
        create_warning("🔋", "BATTERY", "battery", "red")
        create_warning("🌡", "TEMP", "temp", "red")

    def toggle_warning(self, key):
        self.warning_states[key] = not self.warning_states[key]
        icon, color = self.warning_labels[key]

        if self.warning_states[key]:
            icon.config(fg=color)
        else:
            icon.config(fg="gray")

    def create_main_screen(self):
        main = Frame(self, bg="#1e1e1e")
        main.pack(expand=True, fill="both")

        # Media panel
        media = Frame(main, bg="#252525")
        media.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        Label( media, text="Radio", fg="white", bg="#252525", font=("Helvetica", 16) ).pack(pady=10)

        self.station_label = Label( media, text=self.stations[self.station_index], fg="#00ffcc", bg="#252525", font=("Helvetica", 20, "bold") )
        self.station_label.pack(pady=10)

        controls = Frame(media, bg="#252525")
        controls.pack(pady=10)

        Button(controls, text="◀ Prev", command=self.prev_station).grid(row=0, column=0, padx=5)
        Button(controls, text="⏯ Play/Pause", command=self.toggle_play).grid(row=0, column=1, padx=5)
        Button(controls, text="Next ▶", command=self.next_station).grid(row=0, column=2, padx=5)

        volume_frame = Frame(media, bg="#252525")
        volume_frame.pack(pady=15)

        Label(volume_frame, text="Volume", fg="white", bg="#252525").pack()

        self.volume_label = Label( volume_frame, text=str(self.volume), fg="white", bg="#252525", font=("Helvetica", 14) )
        self.volume_label.pack()

        Button(volume_frame, text="+", command=self.volume_up).pack(side="left", padx=5)
        Button(volume_frame, text="-", command=self.volume_down).pack(side="left", padx=5)

        # Navigation panel
        nav = Frame(main, bg="#252525")
        nav.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        Label( nav, text="Navigation", fg="white", bg="#252525", font=("Helvetica", 16) ).pack(pady=10)

        Label( nav, text="🗺 Map Display\n(Placeholder)", fg="#aaaaaa", bg="#252525", font=("Helvetica", 14), justify="center" ).pack(expand=True)

    def create_status_bar(self):
        status = Frame(self, bg="#2b2b2b", height=30)
        status.pack(fill="x")

        Label( status, text="Bluetooth Connected", fg="white", bg="#2b2b2b" ).pack(side="left", padx=10)

        self.time_label = Label( status, fg="white", bg="#2b2b2b" )
        self.time_label.pack(side="right", padx=10)

    def update_time(self):
        self.time_label.config(text=time.strftime("%H:%M:%S"))
        self.after(1000, self.update_time)

    def next_station(self):
        self.station_index = (self.station_index + 1) % len(self.stations)
        self.update_station_label()

    def prev_station(self):
        self.station_index = (self.station_index - 1) % len(self.stations)
        self.update_station_label()

    def toggle_play(self):
        self.playing = not self.playing
        self.update_station_label()

    def update_station_label(self):
        status = "Playing" if self.playing else "Paused"
        self.station_label.config(
            text=f"{self.stations[self.station_index]} ({status})"
        )

    def volume_up(self):
        if self.volume < 20:
            self.volume += 1
            self.volume_label.config(text=str(self.volume))

    def volume_down(self):
        if self.volume > 0:
            self.volume -= 1
            self.volume_label.config(text=str(self.volume))


it = InfotainmentSystem()
it.mainloop()
