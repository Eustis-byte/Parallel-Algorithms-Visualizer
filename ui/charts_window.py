import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from controllers.time_calculator import TimeCalculator
from config import settings

class ChartsWindow(tk.Toplevel):
    def __init__(self, parent, params):
        super().__init__(parent)
        self.params = params
        self.title("Графіки залежностей")
        self.geometry("1400x550")
        self.minsize(1200, 450)
        
        self.time_model = TimeCalculator.create_model(params)
        
        self.create_widgets()
        self.draw_charts()
    
    def create_widgets(self):
        charts_frame = ttk.Frame(self)
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.fig = Figure(figsize=(14, 4.5), dpi=100)
        
        self.ax1 = self.fig.add_subplot(131)
        self.ax2 = self.fig.add_subplot(132)
        self.ax3 = self.fig.add_subplot(133)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=charts_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def get_processor_values(self):
        topology = self.params.get('topology', '')
        
        if topology == "Решітка":
            return settings.GRID_VALUES
        elif topology == "Куб (гіперкуб)":
            return settings.CUBE_VALUES
        elif topology == "Кільце":
            return list(range(3, 21, 2))
        elif topology == "Лінійка":
            return list(range(3, 21, 2))
        elif topology == "Повний граф":
            return list(range(3, 26, 2))
        elif topology == "Зірка":
            return list(range(3, 21, 2))
    
    def _add_value_labels(self, ax, x_values, y_values, fmt, fontsize=8):
        if not y_values:
            return
        
        y_min, y_max = ax.get_ylim()
        y_range = y_max - y_min
        
        for i, (x, y) in enumerate(zip(x_values, y_values)):
            if y <= 0:
                continue
            
            offset = 0.08 * y_range
            if y + offset > y_max:
                offset = -offset
            
            ax.annotate(
                fmt.format(y),
                (x, y),
                textcoords="offset points",
                xytext=(0, 12 if offset > 0 else -12),
                ha='center',
                va='bottom' if offset > 0 else 'top',
                fontsize=fontsize,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7, edgecolor='none')
            )
    
    def draw_charts(self):
        proc_values = self.get_processor_values()
        n = self.params.get('dimension', 100)
        algorithm = self.params.get('method', '')
        
        times = []
        speedups = []
        efficiencies = []
        
        for p in proc_values:
            try:
                results = self.time_model.calculate(
                    algorithm=algorithm,
                    n=n,
                    p=p)
                times.append(results['Tp'])
                speedups.append(results['Sp'])
                efficiencies.append(results['Ep'])
            except Exception as e:
                print(f"Помилка для p={p}: {e}")
                times.append(0)
                speedups.append(0)
                efficiencies.append(0)
        
        self.ax1.clear()
        self.ax1.plot(proc_values, times, 'bo-', linewidth=2, markersize=8)
        self.ax1.set_xlabel('Кількість процесорів', fontsize=10)
        self.ax1.set_ylabel('Час (с)', fontsize=10)
        self.ax1.grid(True, alpha=0.3)
        self.ax1.tick_params(labelsize=9)
        if times:
            max_time = max(t for t in times if t > 0) if any(t > 0 for t in times) else 1
            self.ax1.set_ylim(0, max_time * 1.25)
        self._add_value_labels(self.ax1, proc_values, times, '{:.4f}s', fontsize=8)
        
        self.ax2.clear()
        self.ax2.plot(proc_values, speedups, 'ro-', linewidth=2, markersize=8)
        self.ax2.set_xlabel('Кількість процесорів', fontsize=10)
        self.ax2.set_ylabel('Прискорення', fontsize=10)
        self.ax2.grid(True, alpha=0.3)
        self.ax2.tick_params(labelsize=9)
        self.ax2.axhline(y=1, color='gray', linestyle='--', alpha=0.5, linewidth=1)
        if speedups:
            max_sp = max(s for s in speedups if s > 0) if any(s > 0 for s in speedups) else 1
            self.ax2.set_ylim(0, max_sp * 1.25)
        self._add_value_labels(self.ax2, proc_values, speedups, '{:.2f}x', fontsize=8)
        
        self.ax3.clear()
        self.ax3.plot(proc_values, efficiencies, 'go-', linewidth=2, markersize=8)
        self.ax3.set_xlabel('Кількість процесорів', fontsize=10)
        self.ax3.set_ylabel('Ефективність', fontsize=10)
        self.ax3.grid(True, alpha=0.3)
        self.ax3.tick_params(labelsize=9)
        self.ax3.axhline(y=1, color='gray', linestyle='--', alpha=0.5, linewidth=1)
        if efficiencies:
            max_eff = max(e for e in efficiencies if e > 0) if any(e > 0 for e in efficiencies) else 1
            self.ax3.set_ylim(0, max(1.15, max_eff * 1.25))
        self._add_value_labels(self.ax3, proc_values, efficiencies, '{:.2%}', fontsize=8)
        
        self.fig.tight_layout(pad=2.0)
        self.canvas.draw()