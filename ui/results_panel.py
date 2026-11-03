import tkinter as tk
from tkinter import ttk

class ResultsPanel(ttk.LabelFrame):
    
    def __init__(self, parent):
        super().__init__(parent, text="Результати", padding="5")        
        self.create_widgets()
        
    def create_widgets(self):
        self.text = tk.Text(self, wrap=tk.WORD, height=20, width=35)
        self.text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def update_results(self, params, results_text=None):
        self.text.delete(1.0, tk.END)
        
        self.text.insert(1.0, f"Задача: {params.get('task', '')}\n")
        self.text.insert(tk.END, f"Метод: {params.get('method', '')}\n")
        self.text.insert(tk.END, f"Топологія: {params.get('topology', '')}\n")
        self.text.insert(tk.END, f"Процесорів: {params.get('num_processors', '')}\n\n")
        
        self.text.insert(tk.END, f"Параметри задачі:\n")
        task = params.get('task', '')
        dimension = params.get('dimension', '')
        
        if task == "Матриця * матриця":
            self.text.insert(tk.END, f"  Розмір матриці: {dimension} x {dimension}\n")
        elif task == "Сортування":
            self.text.insert(tk.END, f"  Кількість елементів: {dimension}\n")
        elif task == "СЛАР":
            self.text.insert(tk.END, f"  Розмірність системи: {dimension}\n")
        elif task == "Граф":
            self.text.insert(tk.END, f"  Кількість вершин: {dimension}\n")
        elif task == "Матриця * вектор":
            self.text.insert(tk.END, f"  Розмір матриці: {dimension} x {dimension}\n")
        
        self.text.insert(tk.END, f"\nПараметри обладнання:\n")
        self.text.insert(tk.END, f"  Час виконання базової операції: {params.get('base_operation_time', '')} нс\n")
        self.text.insert(tk.END, f"  Затримка: {params.get('latency', '')} мс\n")
        self.text.insert(tk.END, f"  Пропускна здатність: {params.get('bandwidth', '')} МБ/с\n")
        
        if results_text:
            self.text.insert(tk.END, f"\n{results_text}\n")
        else:
            self.text.insert(tk.END, "\nРезультати:\n")
            self.text.insert(tk.END, " натисніть 'Запустити анімацію' для розрахунку\n")
        
        self.text.see("1.0")
    
    def set_message(self, message):
        self.text.delete(1.0, tk.END)
        self.text.insert(1.0, message)