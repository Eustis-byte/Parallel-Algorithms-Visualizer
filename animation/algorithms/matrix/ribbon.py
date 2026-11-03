from animation.algorithms.base_algorithm import BaseAlgorithm, AlgorithmStep, Message

class Ribbon(BaseAlgorithm):
    def __init__(self):
        super().__init__("Ленточный алгоритм")
    
    def generate_steps(self, topology, params):
        self.steps = []
        
        num_processors = getattr(topology, 'num_processors', len(topology.processor_positions))
        
        coords_B = {proc: proc for proc in range(num_processors)}
        
        step_counter = 0
        self._add_step(step_counter, [], "Початковий розподіл стрічок матриць A і B")
        
        for iteration in range(num_processors):
            # множення
            step_counter += 1
            self._add_step(step_counter, [], f"Ітерація {iteration+1}/{num_processors}, Крок 1: Локальне множення стрічок")
            # зсув В
            if iteration < num_processors - 1:
                step_counter += 1
                messages = []
                new_coords_B = coords_B.copy()
                
                for proc in range(num_processors):
                    target_proc = (proc + 1) % num_processors
                    source_proc = (proc - 1) % num_processors
                    
                    messages.append(Message(
                        proc, target_proc,
                        {"label": f"B{coords_B[proc]}"},
                        step_counter, "shift_B"
                    ))
                    new_coords_B[proc] = coords_B[source_proc]
                
                coords_B = new_coords_B
                self._add_step(step_counter, messages, f"Ітерація {iteration+1}/{num_processors}, Крок 2: Передача стрічок B по кільцю")
        
        step_counter += 1
        self._add_step(step_counter, [], f"Множення матриць завершено ({num_processors} процесорів)")
        
        return self.steps
    
    def _add_step(self, step_num, messages, description):
        step = AlgorithmStep(
            step_number=step_num,
            messages=messages,
            description=description
        )
        self.steps.append(step)