from animation.algorithms.base_algorithm import BaseAlgorithm, AlgorithmStep, Message

class BubbleSort(BaseAlgorithm):
    def __init__(self):
        super().__init__("Бульбашкове сортування")

    def _get_even_pairs(self, n):
        return [(i, i + 1) for i in range(0, n - 1, 2)]

    def _get_odd_pairs(self, n):
        return [(i, i + 1) for i in range(1, n - 1, 2)]

    def _make_messages(self, pairs, label, step):
        msgs = []
        for a, b in pairs:
            msgs.append(Message(a, b, {"label": label}, step, "compare"))
            msgs.append(Message(b, a, {"label": label}, step, "compare"))
        return msgs

    def generate_steps(self, topology, params):
        self.steps = []

        n = getattr(topology, 'num_processors', len(topology.processor_positions))
        step = 0

        self._add_step(step, [], "Початковий розподіл даних")

        for phase in range(n):
            if phase % 2 == 0:
                pairs = self._get_odd_pairs(n)
                phase_name = "Непарна"
            else:
                pairs = self._get_even_pairs(n)
                phase_name = "Парна"

            msgs = self._make_messages(pairs, f"{phase_name.lower()}", step + 1)
            self._add_step(step + 1, msgs, f"{phase_name} фаза {phase + 1}: {len(pairs)} пар")
            step += 1

        self._add_step(step + 1, [], "Сортування завершено")

        return self.steps

    def _add_step(self, num, msgs, desc):
        self.steps.append(AlgorithmStep(num, msgs, desc))