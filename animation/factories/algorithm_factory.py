class AlgorithmFactory:
    @staticmethod
    def create(method_name, task_name):
        if task_name == "Сортування":
            if method_name == "Бульбашкове":
                from animation.algorithms import BubbleSort
                return BubbleSort()
            elif method_name == "Швидке":
                from animation.algorithms.sorting import QuickSort
                return QuickSort()
            elif method_name == "Шелла":
                from animation.algorithms.sorting import ShellSort
                return ShellSort()
        if task_name == "Матриця * матриця":
            if method_name == "Кеннона":
                from animation.algorithms.matrix import Cannon
                return Cannon()
            elif method_name == "Фокса":
                from animation.algorithms.matrix import Fox
                return Fox()
            elif method_name == "Стрічковий":
                from animation.algorithms.matrix import Ribbon
                return Ribbon()
        if task_name == "СЛАР":
            if method_name == "Гауса":
                from animation.algorithms.linear import Gauss
                return Gauss()
        if task_name == "Граф":    
            if method_name == "Флойда":
                from animation.algorithms.graph import Floyd
                return Floyd()
            elif method_name == "Пріма":
                from animation.algorithms.graph import Prim
                return Prim()
            elif method_name == "Дейкстри":
                from animation.algorithms.graph import Dijkstra
                return Dijkstra()
        if task_name == "Матриця * вектор":
            if method_name == "Горизонтальний розподіл":
                from animation.algorithms.matrix_vector import MatrixVector
                return MatrixVector()

        raise NotImplementedError(f"{method_name} для {task_name} в розробці")    