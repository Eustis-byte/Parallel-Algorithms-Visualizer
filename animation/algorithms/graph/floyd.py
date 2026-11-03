from animation.algorithms.base_algorithm import BaseAlgorithm, AlgorithmStep, Message
import math


class Floyd(BaseAlgorithm):
    
    def __init__(self):
        super().__init__("Алгоритм Флойда")
    
    def generate_steps(self, topology, params):
        self.steps = []
        
        num_processors = getattr(topology, 'num_processors', len(topology.processor_positions))
        
        n = int(params.get('dimension', 9))
        grid_size = int(math.sqrt(num_processors))
        
        def add_message(messages, from_proc, to_row, to_col, data_label, msg_type):
            if 0 <= to_row < grid_size and 0 <= to_col < grid_size:
                target = to_row * grid_size + to_col
                if target != from_proc:
                    messages.append(Message(
                        from_processor=from_proc,
                        to_processor=target,
                        data={"label": data_label},
                        step=step_counter,
                        message_type=msg_type
                    ))

        step_counter = 0
        self._add_step(step_counter, [], "Матриця відстаней розподілена циклічно по ґратах процесорів")
        
        for k in range(n):
            step_counter += 1
            messages = []
            
            k_row = k % grid_size
            k_col = k % grid_size
            
            for proc in range(num_processors):
                row, col = proc // grid_size, proc % grid_size
                
                if row == k_row:
                    add_message(messages, proc, 0, col, f"row_{k}", "broadcast_vertical_top")
                    add_message(messages, proc, grid_size-1, col, f"row_{k}", "broadcast_vertical_bottom")
                
                if col == k_col:
                    add_message(messages, proc, row, 0, f"col_{k}", "broadcast_horizontal_left")
                    add_message(messages, proc, row, grid_size-1, f"col_{k}", "broadcast_horizontal_right")

            description = (f"Ітерація {k+1}/{n}, Крок 1: Циклічний розподіл - розсилка k-го рядка від {k_row} ряду"
                           f"та k-го стовпця від {k_col} колонки")
            self._add_step(step_counter, messages, description)
            
            step_counter += 1
            self._add_step(step_counter, [], f"Ітерація {k+1}/{n}, Крок 2: Локальна обробка блоків даних за формулою Флойда")
        
        step_counter += 1
        self._add_step(step_counter, [], "Алгоритм Флойда завершено. Найкоротші шляхи між усіма парами вершин знайдено")
        
        return self.steps
    
    def _add_step(self, step_num, messages, description):
        step = AlgorithmStep(
            step_number=step_num,
            messages=messages,
            description=description
        )
        self.steps.append(step)