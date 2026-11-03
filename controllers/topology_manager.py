from tkinter import messagebox
from config import settings
from topology_drawer import *

class TopologyManager:
  
    def __init__(self):
        self.current_topology_drawer = None
        self.canvas_panel = None
        self.control_panel = None
        self.results_panel = None
        
        self.topology_classes = {
            "Решітка": GridDrawer,
            "Кільце": RingDrawer,
            "Лінійка": LineDrawer,
            "Куб (гіперкуб)": CubeDrawer,
            "Повний граф": CompleteGraphDrawer,
            "Зірка": StarDrawer,
        }
        
        self.dropdown_topologies = ["Решітка", "Куб (гіперкуб)"]
    
    def set_panels(self, control_panel, canvas_panel, results_panel):
        self.control_panel = control_panel
        self.canvas_panel = canvas_panel
        self.results_panel = results_panel
    
    def is_dropdown_topology(self, top_name):
        return top_name in self.dropdown_topologies
    
    def get_num_processors(self):
        top_name = self.control_panel.topology_var.get()
        if not top_name:
            return None
        
        try:
            if self.is_dropdown_topology(top_name):
                value = self.control_panel.proc_combo.get()
                return int(value) if value else None
            else:
                return self.control_panel.proc_var.get()
        except:
            return None
    
    def validate_num_processors(self, top_name, n):
        if n is None:
            return 1
            
        if top_name == "Зірка" and n < 3:
            self.control_panel.proc_var.set(3)
            return 3
            
        return max(1, min(n, 25))
    
    def should_use_snake_numbering(self, method, top_name):
        return method == "Бульбашкове" and top_name in ["Решітка", "Куб (гіперкуб)"]
    
    def build_topology(self):
        top_name = self.control_panel.topology_var.get()
        if not top_name:
            return None
        
        n = self.get_num_processors()
        if n is None:
            return None
        
        drawer_class = self.topology_classes.get(top_name)
        if not drawer_class:
            return None
        
        try:
            method = self.control_panel.method_var.get()
            numbering = "snake" if self.should_use_snake_numbering(method, top_name) else "normal"
            
            if self.is_dropdown_topology(top_name):
                self.current_topology_drawer = drawer_class(n, numbering=numbering)
            else:
                self.current_topology_drawer = drawer_class(n)
            
            return self.current_topology_drawer
            
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося побудувати топологію: {str(e)}")
            return None
    
    def clear(self):
        self.canvas_panel.clear()
        self.current_topology_drawer = None