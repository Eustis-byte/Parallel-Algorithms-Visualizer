import tkinter as tk
from tkinter import messagebox
from config import settings

class UIHandlers:

    def __init__(self, main_window, topology_manager, animation_controller, time_calculator):
        self.main_window = main_window
        self.topology_manager = topology_manager
        self.animation_controller = animation_controller
        self.time_calculator = time_calculator
        self.control_panel = None
        self.results_panel = None
    
    def set_panels(self, control_panel, results_panel):
        self.control_panel = control_panel
        self.results_panel = results_panel
    
    def reset_animation_state(self):
        self.animation_controller.full_reset()
        
        self.main_window.animation_panel.set_inactive()
        self.main_window.animation_panel.reset()
        self.main_window.animation_panel.set_status("Очікування запуску")
        
    def on_task_change(self, event=None):
        self.reset_animation_state()
        task = self.control_panel.task_var.get()
        if not task:
            return
        
        methods = settings.TASK_METHODS.get(task, [])
        self.control_panel.method_combo['values'] = methods
        self.control_panel.method_var.set("")
        self.control_panel.topology_var.set("")
        self.control_panel.topology_combo['values'] = []
        self.topology_manager.clear()
        self.control_panel.set_processors_mode("spinbox")
        self.control_panel.set_processors_spin_state("normal")
        self._update_dimension_values(task)
        
        self._update_status(f"Обрана задача: {task}. Оберіть метод")
    
    def on_method_change(self, event=None):
        self.reset_animation_state()
        task = self.control_panel.task_var.get()
        method = self.control_panel.method_var.get()
        
        if not task or not method:
            return
        
        key = (task, method)
        supported = settings.SUPPORTED_TOPOLOGIES.get(key, [])
        
        self.control_panel.topology_combo['values'] = supported
        self.control_panel.topology_var.set("")
        self.topology_manager.clear()
        self.control_panel.set_processors_mode("spinbox")
        self.control_panel.set_processors_spin_state("normal")
        
        self._update_status(f"Обрано метод: {method}. Оберіть топологію")
    
    def on_topology_change(self, event=None):
        self.reset_animation_state()
        top_name = self.control_panel.topology_var.get()
        if not top_name:
            return
        
        if self.topology_manager.is_dropdown_topology(top_name):
            self.control_panel.set_processors_mode("combobox")
            if top_name == "Решітка":
                self.control_panel.proc_combo['values'] = settings.GRID_VALUES
                self.control_panel.proc_combo.set(settings.GRID_VALUES[0])
                self.control_panel.proc_var.set(settings.GRID_VALUES[0])
            elif top_name == "Куб (гіперкуб)":
                self.control_panel.proc_combo['values'] = settings.CUBE_VALUES
                self.control_panel.proc_combo.set(settings.CUBE_VALUES[1])
                self.control_panel.proc_var.set(settings.CUBE_VALUES[1])
        else:
            self.control_panel.set_processors_mode("spinbox")
            self.control_panel.set_processors_spin_state("normal")
            if top_name == "Зірка":
                self.control_panel.proc_var.set(3)
            else:
                self.control_panel.proc_var.set(6)
        
        self._update_topology()
    
    def on_grid_value_selected(self, event=None):
        self.reset_animation_state()
        self._update_topology()
    
    def validate_and_update(self, event=None):
        self.reset_animation_state()
        top_name = self.control_panel.topology_var.get()
        if not top_name:
            return
        
        n = self.topology_manager.get_num_processors()
        if n is None:
            return
        
        n = self.topology_manager.validate_num_processors(top_name, n)
        self._update_topology()
    
    def on_step_change(self, value):
        if not self.animation_controller.animator or not self.animation_controller.animator.steps:
            return
        step = int(float(value))
        if 0 <= step < len(self.animation_controller.animator.steps):
            self.animation_controller.go_to_step(step)
    
    def on_speed_change(self, value):
        speed = float(value)
        self.animation_controller.set_speed(speed)
        self.main_window.animation_panel.set_speed_label(speed)
    
    def play_animation(self):
        if not self.animation_controller.animator or not self.animation_controller.animator.steps:
            messagebox.showwarning("Попередження", "Спочатку запустіть анімацію")
            return
    
        self.main_window.animation_panel.show()
        self.animation_controller.play()
    
    def pause_animation(self):
        self.animation_controller.pause()
    
    def stop_animation(self):
        self.animation_controller.stop()
            
    def step_animation(self):
        if self.animation_controller.animator and \
           self.animation_controller.animator.current_step < len(self.animation_controller.animator.steps) - 1:
            self.animation_controller.step_forward()
        else:
            messagebox.showinfo("Інформація", "Виконано останній крок")

    def run_animation(self):
        params = self.control_panel.get_values()

        params['num_processors'] = self.topology_manager.get_num_processors()
        
        if not all([params['task'], params['method'], params['topology']]):
            messagebox.showwarning("Попередження", "Оберіть задачу, метод і топологію")
            return
        
        if not self.topology_manager.current_topology_drawer:
            messagebox.showwarning("Попередження", "Спочатку побудуйте топологію")
            return
        
        try:
            steps, animator = self.animation_controller.load_animation(
                params, self.topology_manager.current_topology_drawer
            )
            
            self.main_window.animation_panel.show()
            self.main_window.animation_panel.set_steps(len(steps))
            self.animation_controller.draw_step(0)
            
            if len(steps) > 0:
                step = steps[0]
                self.main_window.animation_panel.update_step(0, step.description)
            else:
                self.main_window.animation_panel.set_status("Немає кроків")
            
            results_text = self.time_calculator.calculate(params)
            self.results_panel.update_results(params, results_text)
            
            self._update_status(f"Анімація запущена: {params['method']} на {params['topology']}")
            self.main_window.animation_panel.charts_btn.config(state=tk.NORMAL)

        except ValueError as e:
            messagebox.showerror("Помилка параметрів", str(e))
        except NotImplementedError as e:
            messagebox.showinfo("У розробці", str(e))
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося запустити анімацію: {str(e)}")
    
    def clear_all(self):
        self.reset_animation_state()
        self.control_panel.task_var.set("")
        self.control_panel.method_var.set("")
        self.control_panel.method_combo['values'] = []
        self.control_panel.topology_var.set("")
        self.control_panel.topology_combo['values'] = []
        self.topology_manager.clear()
        self.control_panel.set_processors_mode("spinbox")
        self.control_panel.set_processors_spin_state("normal")
        self.control_panel.dimension_combo['values'] = settings.MATRIX_SIZES
        self.control_panel.dimension_combo.set(settings.MATRIX_SIZES[2])
        self.results_panel.set_message("Оберіть задачу і метод для початку роботи")
        self._update_status("Оберіть задачу і метод")
        self.main_window.animation_panel.charts_btn.config(state=tk.DISABLED)

    def _update_topology(self):
        topology = self.topology_manager.build_topology()
        if topology:
            canvas = self.topology_manager.canvas_panel.canvas
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width, canvas_height = 800, 500
            
            self.topology_manager.canvas_panel.draw_topology(topology, canvas_width, canvas_height)
            
            params = self.control_panel.get_values()
            params['num_processors'] = self.topology_manager.get_num_processors()
            results_text = self.time_calculator.calculate(params)
            self.results_panel.update_results(params, results_text)
            
            top_name = self.control_panel.topology_var.get()
            n = self.topology_manager.get_num_processors()
            self._update_status(f"Побудована топологія '{top_name}' з {n} процесорами.")
    
    def _update_dimension_values(self, task):
        dimension_configs = {
            "Матриця * матриця": (settings.MATRIX_SIZES, settings.MATRIX_SIZES[2]),
            "Сортування": (settings.SORTING_SIZES, 1000),
            "СЛАР": (settings.SYSTEM_SIZES, 5),
            "Граф": (settings.GRAPH_SIZES, 5),
            "Матриця * вектор": (settings.MATRIX_SIZES, settings.MATRIX_SIZES[2]),
        }
        
        config = dimension_configs.get(task)
        if config:
            values, default_value = config
            self.control_panel.dimension_combo['values'] = values
            self.control_panel.dimension_combo.set(default_value)
    
    def _update_status(self, message):
        if hasattr(self.main_window, 'animation_panel'):
            self.main_window.animation_panel.set_status(message)