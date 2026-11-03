import tkinter as tk
from tkinter import ttk

class AnimationPanel(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, relief=tk.RAISED, borderwidth=1)
        self.controller = controller
        self.total_steps = 0
        self.speed = 1.0

        self.create_widgets()
        self.set_inactive()

    def create_widgets(self):
        row1 = ttk.Frame(self)
        row1.pack(fill=tk.X, padx=300, pady=2)

        self.play_btn = ttk.Button(
            row1, text="▶ Пуск",
            command=self.controller.play_animation, width=10
        )
        self.play_btn.pack(side=tk.LEFT, padx=2)

        self.pause_btn = ttk.Button(
            row1, text="⏸ Пауза",
            command=self.controller.pause_animation,
            state=tk.DISABLED, width=10
        )
        self.pause_btn.pack(side=tk.LEFT, padx=2)

        self.stop_btn = ttk.Button(
            row1, text="■ Стоп",
            command=self.controller.stop_animation, width=10
        )
        self.stop_btn.pack(side=tk.LEFT, padx=2)

        self.step_btn = ttk.Button(
            row1, text="⏩ Крок",
            command=self.controller.step_animation, width=8
        )
        self.step_btn.pack(side=tk.LEFT, padx=2)

        self.charts_btn = ttk.Button(
            row1, text="📊 Графіки",
            command=self.controller.show_charts, width=14
        )
        self.charts_btn.pack(side=tk.LEFT, padx=2)
        self.charts_btn.config(state=tk.DISABLED)

        ttk.Separator(row1, orient=tk.VERTICAL).pack(
            side=tk.LEFT, padx=10, fill=tk.Y
        )

        ttk.Label(row1, text="Швидкість:").pack(side=tk.LEFT, padx=5)

        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_scale = ttk.Scale(
            row1, from_=0.5, to=3.0,
            variable=self.speed_var,
            orient=tk.HORIZONTAL, length=150,
            command=self.controller.on_speed_change
        )
        self.speed_scale.pack(side=tk.LEFT, padx=5)

        self.speed_label = ttk.Label(row1, text="1.0x")
        self.speed_label.pack(side=tk.LEFT, padx=5)

        row2 = ttk.Frame(self)
        row2.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(row2, text="Крок:").pack(side=tk.LEFT, padx=5)

        self.step_var = tk.DoubleVar(value=0)
        self.step_scale = ttk.Scale(
            row2, from_=0, to=100,
            variable=self.step_var,
            orient=tk.HORIZONTAL,
            command=self.controller.on_step_change
        )
        self.step_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.step_label = ttk.Label(row2, text="0/0")
        self.step_label.pack(side=tk.RIGHT, padx=5)

        row3 = ttk.Frame(self)
        row3.pack(fill=tk.X, padx=5, pady=2)

        self.anim_status_var = tk.StringVar()
        self.anim_status_var.set("Очікування")
        anim_status = ttk.Label(
            row3, textvariable=self.anim_status_var,
            relief=tk.SUNKEN, anchor=tk.W,
            font=("Arial", 9)
        )
        anim_status.pack(fill=tk.X, padx=2, pady=2)

    def set_inactive(self):
        self.play_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)
        self.step_btn.config(state=tk.DISABLED)
        self.step_scale.config(state=tk.DISABLED)
        self.speed_scale.config(state=tk.DISABLED)
        self.anim_status_var.set("Очікування запуску")

    def set_active(self):
        self.play_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.step_btn.config(state=tk.NORMAL)
        self.step_scale.config(state=tk.NORMAL)
        self.speed_scale.config(state=tk.NORMAL)

    def show(self):
        self.set_active()
        self.set_status("Готовий до виконання")

    def hide(self):
        self.set_inactive()

    def set_steps(self, total_steps):
        self.total_steps = total_steps
        self.step_scale.config(to=max(1, total_steps))
        self.step_label.config(text=f"0/{total_steps}")
        self.step_var.set(0)
        self.set_active()

    def update_step(self, step, description=""):
        self.step_var.set(step)
        self.step_scale.config(to=max(1, self.total_steps))
        self.step_label.config(text=f"{step}/{self.total_steps}")
        if description:
            self.set_status(f"№ {step}: {description}")
        else:
            self.set_status(f"Крок {step} з {self.total_steps}")

    def set_playing(self, is_playing):
        if is_playing:
            self.play_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.NORMAL)
            self.step_btn.config(state=tk.DISABLED)
        else:
            self.play_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.step_btn.config(state=tk.NORMAL)

    def reset(self):
        self.set_playing(False)
        self.step_var.set(0)
        total = self.total_steps if self.total_steps > 0 else 0
        self.step_label.config(text=f"0/{total}")
        self.step_scale.config(to=max(1, total))
        self.set_status("Очікування запуску")

    def set_status(self, message):
        self.anim_status_var.set(message)

    def set_speed_label(self, speed):
        self.speed_label.config(text=f"{speed:.1f}x")