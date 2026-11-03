import tkinter as tk
from tkinter import ttk
from config import settings

class ControlPanel(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding="5")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        row1 = ttk.Frame(self)
        row1.pack(fill=tk.X, pady=2)

        ttk.Label(row1, text="Задача:").pack(side=tk.LEFT, padx=5)
        self.task_var = tk.StringVar()
        self.task_combo = ttk.Combobox(
            row1, textvariable=self.task_var,
            values=list(settings.TASK_METHODS.keys()),
            state="readonly", width=22
        )
        self.task_combo.pack(side=tk.LEFT, padx=5)
        self.task_combo.bind("<<ComboboxSelected>>", self.controller.on_task_change)

        ttk.Label(row1, text="Метод:").pack(side=tk.LEFT, padx=5)
        self.method_var = tk.StringVar()
        self.method_combo = ttk.Combobox(
            row1, textvariable=self.method_var,
            values=[], state="readonly", width=22
        )
        self.method_combo.pack(side=tk.LEFT, padx=5)
        self.method_combo.bind("<<ComboboxSelected>>", self.controller.on_method_change)

        ttk.Label(row1, text="Топологія:").pack(side=tk.LEFT, padx=5)
        self.topology_var = tk.StringVar()
        self.topology_combo = ttk.Combobox(
            row1, textvariable=self.topology_var,
            values=[], state="readonly", width=15
        )
        self.topology_combo.pack(side=tk.LEFT, padx=5)
        self.topology_combo.bind("<<ComboboxSelected>>", self.controller.on_topology_change)

        row2 = ttk.Frame(self)
        row2.pack(fill=tk.X, pady=2)

        ttk.Label(row2, text="Кіл-ть процесорів:").pack(side=tk.LEFT, padx=5)

        self.proc_frame = ttk.Frame(row2)
        self.proc_frame.pack(side=tk.LEFT, padx=5)

        self.proc_spin = ttk.Spinbox(
            self.proc_frame, from_=1, to=25,
            width=5, command=self.controller.validate_and_update
        )
        self.proc_combo = ttk.Combobox(
            self.proc_frame, values=[], state="readonly", width=5
        )
        self.proc_combo.bind("<<ComboboxSelected>>", self.controller.on_grid_value_selected)

        self.proc_spin.pack(side=tk.LEFT)
        self.proc_var = tk.IntVar(value=4)
        self.proc_spin.config(textvariable=self.proc_var)

        ttk.Label(row2, text="Час виконання базової операції (нс):").pack(side=tk.LEFT, padx=5)
        self.cpu_var = tk.DoubleVar(value=10.0)
        self.cpu_spin = ttk.Spinbox(
            row2, from_=0.1, to=10.0, increment=0.5,
            textvariable=self.cpu_var, width=8
        )
        self.cpu_spin.pack(side=tk.LEFT, padx=5)

        ttk.Label(row2, text="Розмірність задачі:").pack(side=tk.LEFT, padx=5)
        self.dimension_combo = ttk.Combobox(
            row2, values=settings.MATRIX_SIZES,
            state="readonly", width=8
        )
        self.dimension_combo.pack(side=tk.LEFT, padx=5)
        self.dimension_combo.set(settings.MATRIX_SIZES[2])

        row3 = ttk.Frame(self)
        row3.pack(fill=tk.X, pady=2)

        ttk.Label(row3, text="Затримка (мс):").pack(side=tk.LEFT, padx=5)
        self.latency_var = tk.DoubleVar(value=1.0)
        ttk.Spinbox(
            row3, from_=0.0, to=100.0, increment=0.1,
            textvariable=self.latency_var, width=8
        ).pack(side=tk.LEFT, padx=5)

        ttk.Label(row3, text="Пропускна здатність (МБ/с):").pack(side=tk.LEFT, padx=5)
        self.bandwidth_var = tk.DoubleVar(value=100.0)
        ttk.Spinbox(
            row3, from_=1.0, to=10000.0, increment=10.0,
            textvariable=self.bandwidth_var, width=8
        ).pack(side=tk.LEFT, padx=5)

        row4 = ttk.Frame(self)
        row4.pack(fill=tk.X, pady=10)

        self.run_btn = ttk.Button(
            row4, text="🚀 Запустити анімацію",
            command=self.controller.run_animation, width=22
        )
        self.run_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = ttk.Button(
            row4, text="🗑 Очистити усе",
            command=self.controller.clear_all, width=22
        )
        clear_btn.pack(side=tk.LEFT, padx=5)

    def set_processors_mode(self, mode):
        
        self.proc_spin.pack_forget()
        self.proc_combo.pack_forget()
        if mode == "spinbox":
            self.proc_spin.pack(side=tk.LEFT)
        elif mode == "combobox":
            self.proc_combo.pack(side=tk.LEFT)

    def get_values(self):
        
        return {
            'task': self.task_var.get(),
            'method': self.method_var.get(),
            'topology': self.topology_var.get(),
            'dimension': self._get_dimension(),
            'base_operation_time': self._get_base_operation_time(),
            'latency': self.latency_var.get(),
            'bandwidth': self.bandwidth_var.get()
        }

    def set_processors_spin_state(self, state):
        self.proc_spin.config(state=state)

    def _get_dimension(self):
        val = self.dimension_combo.get()
        return int(val) if val else 4

    def _get_base_operation_time(self):
        try:
            return float(self.cpu_var.get())
        except (ValueError, tk.TclError):
            return 10.0