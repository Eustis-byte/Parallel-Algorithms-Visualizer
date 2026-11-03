from animation.algorithms.base_algorithm import BaseAlgorithm, AlgorithmStep, Message

class ShellSort(BaseAlgorithm):
    def __init__(self):
        super().__init__("Сортування Шелла")

    def _get_snake(self, n):
        if n == 4: return [0, 1, 3, 2]
        if n == 8: return [0, 1, 3, 2, 6, 7, 5, 4]
        if n == 16: return [0, 1, 3, 2, 6, 7, 5, 4, 12, 13, 15, 14, 10, 11, 9, 8]
        return list(range(n))

    def _make_messages(self, pairs, label, step):
        msgs = []
        for a, b in pairs:
            msgs.append(Message(a, b, {"label": label}, step, "exchange"))
            msgs.append(Message(b, a, {"label": label}, step, "exchange"))
        return msgs

    def _get_hypercube_pairs(self, n, gap):
        pairs, visited = [], set()
        for p in range(n):
            q = p ^ gap
            if q < n and p not in visited and q not in visited:
                visited.update([p, q])
                pairs.append((p, q))
        return pairs

    def _get_snake_pairs(self, n):
        snake = self._get_snake(n)
        even = [(snake[i], snake[i+1]) for i in range(0, len(snake)-1, 2)]
        odd  = [(snake[i], snake[i+1]) for i in range(1, len(snake)-1, 2)]
        return even, odd

    def generate_steps(self, topology, params):
        self.steps = []

        n = getattr(topology, 'num_processors', len(topology.processor_positions))
        if n & (n-1) != 0:
            raise ValueError("Shell sort requires power of 2 processors")

        d = (n - 1).bit_length()
        step = 0

        self._add_step(step, [], "Початковий розподіл даних")

        for bit in range(d):
            gap = 1 << bit
            pairs = self._get_hypercube_pairs(n, gap)
            msgs = self._make_messages(pairs, f"обмін gap={gap}", step+1)
            self._add_step(step+1, msgs, f"Обмін за gap={gap} (біт {bit})")
            self._add_step(step+2, [], f"Локальне сортування після gap={gap}")
            step += 2

        even_pairs, odd_pairs = self._get_snake_pairs(n)
        for i in range(1, 3):
            msgs_even = self._make_messages(even_pairs, "очистка even", step+1)
            self._add_step(step+1, msgs_even, f"Очистка {i}.A (парна)")
            msgs_odd = self._make_messages(odd_pairs, "очистка odd", step+2)
            self._add_step(step+2, msgs_odd, f"Очистка {i}.B (непарна)")
            step += 2

        self._add_step(step+1, [], "Сортування Шелла завершено")

        return self.steps

    def _add_step(self, num, msgs, desc):
        self.steps.append(AlgorithmStep(num, msgs, desc))