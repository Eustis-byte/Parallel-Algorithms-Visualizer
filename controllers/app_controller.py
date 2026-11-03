from tkinter import messagebox
from .topology_manager import TopologyManager
from .animation_controller import AnimationController
from .time_calculator import TimeCalculator
from .ui_handlers import UIHandlers

class AppController:
    
    def __init__(self, main_window):
        self.main_window = main_window
        
        self.topology_manager = TopologyManager()
        self.animation_controller = AnimationController(main_window)
        self.time_calculator = TimeCalculator()
        
        self.ui_handlers = UIHandlers(
            main_window, 
            self.topology_manager, 
            self.animation_controller,
            self.time_calculator
        )
        
        self.topology_classes = self.topology_manager.topology_classes
        self.dropdown_topologies = self.topology_manager.dropdown_topologies
        
        self.control_panel = None
        self.results_panel = None
        self.canvas_panel = None
    
    def set_panels(self, control_panel, canvas_panel, results_panel):
        self.control_panel = control_panel
        self.canvas_panel = canvas_panel
        self.results_panel = results_panel
        
        self.topology_manager.set_panels(control_panel, canvas_panel, results_panel)
        self.ui_handlers.set_panels(control_panel, results_panel)
    
    def set_canvas(self, canvas):
        self.animation_controller.set_canvas(canvas)
    
    def clear_canvas(self):
        self.topology_manager.clear()

    def show_charts(self):
        if not self.control_panel or not self.results_panel:
            messagebox.showwarning("Попередження", "Спочатку виберіть параметри")
            return
        
        params = self.control_panel.get_values()
        
        if not all([params['task'], params['method'], params['topology']]):
            messagebox.showwarning("Попередження", "Виберіть задачу, метод і топологію")
            return
        
        try:
            from ui.charts_window import ChartsWindow
            ChartsWindow(self.main_window, params)
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося відкрити графіки: {str(e)}")

    def __getattr__(self, name):
        if hasattr(self.ui_handlers, name):
            return getattr(self.ui_handlers, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")