import math
from animation.algorithms.base_algorithm import BaseAlgorithm, AlgorithmStep, Message

class Cannon(BaseAlgorithm):

    def __init__(self):
        super().__init__("Алгоритм Кэннона")
    
    def generate_steps(self, topology, params):
        self.steps = []
        
        num_processors = getattr(topology, 'num_processors', len(topology.processor_positions))
        p = int(math.sqrt(num_processors))
        
        coords_A = {i * p + j: (i, j) for i in range(p) for j in range(p)}
        coords_B = coords_A.copy()
        
        step_counter = 0
        self._add_step(step_counter, [], "Початковий розподіл блоків матриць A і B")
        
        def shift_matrix(matrix_type, row_range, col_range, desc):
            nonlocal step_counter, coords_A, coords_B
            step_counter += 1
            messages = []
            
            if matrix_type == 'A':
                new_coords = coords_A.copy()
                for i in row_range:
                    for j in col_range:
                        proc_id = i * p + j
                        messages.append(Message(
                            proc_id, i * p + (j - 1) % p,
                            {"label": f"A{coords_A[proc_id]}"},
                            step_counter, "shift_A"
                        ))
                        new_coords[proc_id] = coords_A[i * p + (j + 1) % p]
                coords_A = new_coords
            else:
                new_coords = coords_B.copy()
                for j in col_range:
                    for i in row_range:
                        proc_id = i * p + j
                        messages.append(Message(
                            proc_id, ((i - 1) % p) * p + j,
                            {"label": f"B{coords_B[proc_id]}"},
                            step_counter, "shift_B"
                        ))
                        new_coords[proc_id] = coords_B[((i + 1) % p) * p + j]
                coords_B = new_coords
                
            self._add_step(step_counter, messages, desc)
        # Вирівнювання A
        for shift in range(1, p):
            shift_matrix('A', range(shift, p), range(p), f"Початкове вирівнювання A вліво на {p-1} (рядки {shift}-{p-1})") 
        # Вирівнювання B
        for shift in range(1, p):
            shift_matrix('B', range(p), range(shift, p), f"Початкове вирівнювання B вгору на {p-1} (стовпці {shift}-{p-1})")
        # Основні ітерації
        for iteration in range(p):
            step_counter += 1
            self._add_step(step_counter, [], f"Ітерація {iteration+1}/{p}, Крок 1: Локальне множення блоків A та В")
            
            if iteration < p - 1:
                shift_matrix('A', range(p), range(p), f"Ітерація {iteration+1}/{p}, Крок 2: Зсув A вліво на 1")
                shift_matrix('B', range(p), range(p), f"Ітерація {iteration+1}/{p}, Крок 3: Зсув B вгору на 1")
        
        step_counter += 1
        self._add_step(step_counter, [], f"Множення матриць завершено (решітка {p}x{p})")
        
        return self.steps
    
    def _add_step(self, step_num, messages, description):
        self.steps.append(AlgorithmStep(step_num, messages, description))