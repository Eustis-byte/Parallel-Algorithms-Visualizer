from animation.algorithms.base_algorithm import BaseAlgorithm, AlgorithmStep, Message

class Gauss(BaseAlgorithm):
    
    def __init__(self):
        super().__init__("Метод Гауса")
    
    def generate_steps(self, topology, params):
        self.steps = []
        
        num_processors = getattr(topology, 'num_processors', 
                                 len(topology.processor_positions))
        n = int(params.get('dimension', 6))
        
        self._add_step(0, [], "Початок розв'язання СЛАУ (циклічний розподіл)")
        
        step_counter = 0
        
        for k in range(1, n):
            owner = (k - 1) % num_processors
            step_counter += 1
            
            msgs = []
            for p in range(num_processors):
                if p != owner:
                    
                    first_row_p = p + 1

                    max_row_of_p = first_row_p + ((n - first_row_p) // num_processors) * num_processors
                    
                    if max_row_of_p > k:
                        msgs.append(Message(
                            owner, p, 
                            {"label": f"STR{k}"}, 
                            step_counter, "send"
                        ))
            
            desc = f"Прямий хід, Крок {k}: Виключення x{k} (ведучий рядок {k} від P{owner})"
            self._add_step(step_counter, msgs, desc)
        
        for i in range(n, 0, -1):
            owner = (i - 1) % num_processors
            step_counter += 1
            
            msgs = []
            if i > 1:
                for p in range(num_processors):
                    if p != owner:
                        if (p + 1) < i:
                            msgs.append(Message(
                                owner, p, 
                                {"label": f"X{i}"}, 
                                step_counter, "send"
                            ))
            
            desc = f"Зворотній хід, Крок {n-i+1}: Знаходження та розсилка x{i} від P{owner}"
            self._add_step(step_counter, msgs, desc)
        
        step_counter += 1
        self._add_step(step_counter, [], "Решіння знайдено. Система розв'язана.")
        
        return self.steps
    
    def _add_step(self, step_num, messages, description):
        self.steps.append(AlgorithmStep(
            step_number=step_num, 
            messages=messages, 
            description=description
        ))