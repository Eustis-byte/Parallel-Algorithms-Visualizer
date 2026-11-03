from animation.algorithms.base_algorithm import BaseAlgorithm, AlgorithmStep, Message

class Prim(BaseAlgorithm):
    def __init__(self):
        super().__init__("Алгоритм Пріма")
    
    def generate_steps(self, topology, params):
        self.steps = []
        
        if hasattr(topology, 'num_processors'):
            num_processors = topology.num_processors
        else:
            num_processors = len(topology.processor_positions)
        
        n = params.get('dimension', 5)
        if isinstance(n, str):
            n = int(n)
        
        if hasattr(topology, 'position_to_proc'):
            if self._is_star(topology, num_processors):
                self._generate_star_steps(n, num_processors)
            else:
                self._generate_hypercube_steps(n, num_processors)
        else:
            self._generate_star_steps(n, num_processors)
        
        return self.steps
    
    def _is_star(self, topology, num_processors):
        if hasattr(topology, 'get_neighbors'):
            neighbors_0 = topology.get_neighbors(0)
            if len(neighbors_0) >= num_processors - 1:
                return True
        return False
    
    def _generate_star_steps(self, n, num_processors):
        step_counter = 0
        active_processors = min(n, num_processors)
        
        self._add_step(step_counter, [], "Початок алгоритму (зірка)")
        
        for k in range(1, n):
            step_counter += 1
            messages = []
            
            for proc in range(1, active_processors):
                messages.append(Message(
                    from_processor=proc,
                    to_processor=0,
                    data={"label": f"дані від {proc}"},
                    step=step_counter,
                    message_type="send_to_center"
                ))
            
            self._add_step(step_counter, messages, f"Ітерація {k}, Крок 1: Збір даних на процесорі 0 ")
            
            step_counter += 1
            messages = []
            
            for proc in range(1, active_processors):
                messages.append(Message(
                    from_processor=0,
                    to_processor=proc,
                    data={"label": f"рішення {k}"},
                    step=step_counter,
                    message_type="broadcast_from_center"
                ))
            
            self._add_step(step_counter, messages, f"Ітерація {k}, Крок 2: Розсилка від процесора 0 ")
        
        step_counter += 1
        self._add_step(step_counter, [], "Алгоритм завершено (зірка)")
    
    def _generate_hypercube_steps(self, n, num_processors):
        step_counter = 0
        dim = 0
        temp = num_processors
        
        while temp > 1:
            temp >>= 1
            dim += 1
        
        self._add_step(step_counter, [], "Початок алгоритму (гіперкуб)")
        
        for k in range(1, n):
            for bit in range(dim):
                step_counter += 1
                messages = []
                visited = set()
                
                for proc in range(num_processors):
                    partner = proc ^ (1 << bit)
                    if partner < num_processors and partner not in visited and proc not in visited:
                        visited.add(proc)
                        visited.add(partner)
                        
                        messages.append(Message(
                            from_processor=proc,
                            to_processor=partner,
                            data={"label": f"обмін по біту {bit}"},
                            step=step_counter,
                            message_type="exchange"
                        ))
                        messages.append(Message(
                            from_processor=partner,
                            to_processor=proc,
                            data={"label": f"обмін по біту {bit}"},
                            step=step_counter,
                            message_type="exchange"
                        ))
                
                self._add_step(step_counter, messages, f"Ітерація {k}, Крок {bit+1}: Двосторонній обмін за виміром {bit}")
        
        step_counter += 1
        self._add_step(step_counter, [], "Алгоритм завершено (гіперкуб)")
            
    def _add_step(self, step_num, messages, description):
        step = AlgorithmStep(
            step_number=step_num,
            messages=messages,
            description=description
        )
        self.steps.append(step)