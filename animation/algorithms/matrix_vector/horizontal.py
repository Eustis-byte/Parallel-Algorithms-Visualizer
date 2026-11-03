import math
from animation.algorithms.base_algorithm import BaseAlgorithm, AlgorithmStep, Message

class MatrixVector(BaseAlgorithm):
    def __init__(self):
        super().__init__("Множення матриці на вектор")
    
    def generate_steps(self, topology, params):
        self.steps = []
        if hasattr(topology, 'num_processors'):
            num_processors = topology.num_processors
        else:
            num_processors = len(topology.processor_positions)
 
        n = params.get('dimension', 8)
        if isinstance(n, str):
            n = int(n)
        dim = 0
        temp = num_processors
        while temp > 1:
            temp >>= 1
            dim += 1
        
        step_counter = 0
        
        self._add_step(step_counter, [], "Початковий розподіл строк матриці і вектора")
        
        step_counter += 1
        self._add_step(step_counter, [], "Локальное множення")
        
        for bit in range(dim):
            step_counter += 1
            messages = []
            
            visited = set()
            for proc in range(num_processors):
                partner = proc ^ (1 << bit)
                if partner < num_processors and partner not in visited and proc not in visited:
                    visited.add(proc)
                    visited.add(partner)
                    
                    msg_data = {"label": f"Обмін по біту {bit}"}
                    
                    for src, dst in [(proc, partner), (partner, proc)]:
                        messages.append(Message(
                            from_processor=src,
                            to_processor=dst,
                            data=msg_data,
                            step=step_counter,
                            message_type="exchange"
                        ))
            
            self._add_step(step_counter, messages, f"Крок {bit+1}: Обмін по біту {bit}")
        
        step_counter += 1
        self._add_step(step_counter, [], "Процесори отримали повний результуючий вектор")
        
        return self.steps
    
    def _add_step(self, step_num, messages, description):
        step = AlgorithmStep(
            step_number=step_num,
            messages=messages,
            description=description
        )
        self.steps.append(step)