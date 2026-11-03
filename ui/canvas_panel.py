import tkinter as tk
from tkinter import ttk

class CanvasPanel(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Топологія", padding="5")
        self.create_widgets()
        
    def create_widgets(self):
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=1,
                                highlightbackground="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def clear(self):
        self.canvas.delete("all")
    
    def draw_topology(self, drawer, width=None, height=None):
        self.clear()
        if drawer:
            if width is None or height is None:
                self.update_idletasks()
                width = self.canvas.winfo_width()
                height = self.canvas.winfo_height()
                if width <= 1 or height <= 1:
                    width, height = 800, 500
            drawer.draw(self.canvas, width, height)