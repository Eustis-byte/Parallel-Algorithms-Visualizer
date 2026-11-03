import tkinter as tk
from tkinter import ttk
from ui.control_panel import ControlPanel
from ui.canvas_panel import CanvasPanel
from ui.results_panel import ResultsPanel
from ui.animation_panel import AnimationPanel
from controllers.app_controller import AppController

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Візуалізація топологій паралельних алгоритмів")
        self.state('zoomed')
        self.minsize(1000, 700)
        
        self.controller = AppController(self)
        
        self.create_widgets()
    
    def create_widgets(self):
        self.control_panel = ControlPanel(self, self.controller)
        self.control_panel.pack(side=tk.TOP, fill=tk.X)
        
        main_area = ttk.Frame(self)
        main_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas_panel = CanvasPanel(main_area)
        self.canvas_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.results_panel = ResultsPanel(main_area)
        self.results_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        self.controller.set_canvas(self.canvas_panel.canvas)
        self.controller.set_panels(
            self.control_panel,
            self.canvas_panel,
            self.results_panel
        )
        
        self.animation_panel = AnimationPanel(self, self.controller)
        self.animation_panel.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=(0, 5))