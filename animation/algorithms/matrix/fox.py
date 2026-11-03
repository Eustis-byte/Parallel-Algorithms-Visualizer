import math
from animation.algorithms.base_algorithm import BaseAlgorithm, AlgorithmStep, Message

class Fox(BaseAlgorithm):

    def __init__(self):
        super().__init__("Алгоритм Фокса")
    
    def generate_steps(self, topology, params):
        self.steps = []
        
        num_processors = getattr(topology, 'num_processors', len(topology.processor_positions))
        p = int(math.sqrt(num_processors))
                
        processor_B = {i * p + j: (i, j) for i in range(p) for j in range(p)}
        
        step_counter = 0
        self._add_step(step_counter, [], "Початковий розподіл блоків матриць A і B")
        
        for iteration in range(p):
    # броадкаст а
            step_counter += 1
            messages = []
            
            for i in range(p):
                diag_col = (i + iteration) % p
                diag_proc = i * p + diag_col
                label = {"label": f"A({i},{diag_col})"}
                
                if diag_col != 0:
                    messages.append(Message(diag_proc, i * p, label, step_counter, "broadcast_A_left"))
                if diag_col != p - 1:
                    messages.append(Message(diag_proc, i * p + (p - 1), label, step_counter, "broadcast_A_right"))
            
            self._add_step(step_counter, messages, f"Ітерація {iteration+1}/{p}, Крок 1: Розсилка A  у рядках")   
            # локальні кроки
            step_counter += 1
            self._add_step(step_counter, [], f"Ітерація {iteration+1}/{p}, Крок 2: Локальне множення блоків")    
            # зсув В
            if iteration < p - 1:
                step_counter += 1
                messages = []
                new_B = processor_B.copy()
                
                for i in range(p):
                    for j in range(p):
                        proc_id = i * p + j
                        messages.append(Message(
                            proc_id, ((i - 1) % p) * p + j,
                            {"label": f"B{processor_B[proc_id]}"},
                            step_counter, "shift_B"
                        ))
                        new_B[proc_id] = processor_B[((i + 1) % p) * p + j]
                
                processor_B = new_B
                self._add_step(step_counter, messages, f"Ітерація {iteration+1}/{p}, Крок 3: Зсув B вгору")
        
        step_counter += 1
        self._add_step(step_counter, [], f"Множення матриць завершено (решітка {p}x{p})")
        
        return self.steps
    
    def _add_step(self, step_num, messages, description):
        self.steps.append(AlgorithmStep(step_num, messages, description))