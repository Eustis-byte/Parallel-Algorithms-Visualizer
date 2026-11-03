from animation.algorithms.base_algorithm import BaseAlgorithm, AlgorithmStep, Message

class QuickSort(BaseAlgorithm):

    def __init__(self):
        super().__init__("Швидке сортування")

    def _get_pairs_for_bit(self, num_processors, bit):
        visited = set()
        pairs = []
        for proc in range(num_processors):
            partner = proc ^ (1 << bit)
            if partner < num_processors and proc not in visited and partner not in visited:
                visited.update({proc, partner})
                pairs.append((proc, partner))
        return pairs

    def _make_messages(self, pairs, label, step):
        msgs = []
        for a, b in pairs:
            msgs.extend([
                Message(a, b, {"label": label}, step, "exchange"),
                Message(b, a, {"label": label}, step, "exchange")
            ])
        return msgs

    def generate_steps(self, topology, params):
        self.steps = []

        num_processors = getattr(topology, 'num_processors', len(topology.processor_positions))

        d = (num_processors - 1).bit_length()
        step_counter = 0

        self._add_step(step_counter, [], "Початковий розподіл даних")

        for bit in range(d):
            step_counter += 1
            self._add_step(
                step_counter, [],
                f"Вибір півота та локальне розділення за виміром {bit}"
            )
            step_counter += 1
            pairs = self._get_pairs_for_bit(num_processors, bit)
            msgs = self._make_messages(pairs, f"обмін bit{bit}", step_counter)
            self._add_step(
                step_counter, msgs,
                f"Обмін частинами даних за виміром {bit}"
            )
            step_counter += 1
            self._add_step(
                step_counter, [],
                f"Локальне сортування після обміну за виміром {bit}"
            )

        step_counter += 1
        self._add_step(step_counter, [], "Швидке сортування завершено")

        return self.steps

    def _add_step(self, step_num, messages, description):
        step = AlgorithmStep(step_num, messages, description)
        self.steps.append(step)