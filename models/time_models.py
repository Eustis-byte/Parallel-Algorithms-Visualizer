import math

class TimeModel:
    
    def __init__(self, base_operation_time=1.0, latency=0.001, bandwidth=100.0):
        self.base_operation_time = base_operation_time  # нс
        self.latency = latency                  # с
        self.bandwidth = bandwidth              # МБ/с
        self.word_size = 8                      # байт (double)
    
    def calculate(self, algorithm, n, p, topology='hypercube', l=None, k=None):
       
        params = self._get_algorithm_params(algorithm, n, p, topology, l, k)
        
        W1 = params['W1']
        W = params['W']
        K = params['K']
        m = params['m']
        
        tau = self.base_operation_time * 1e-9
        # Час розрахунку
        Tcalc = W * tau 
        # МБ/с в байт/с
        bandwidth_bytes = self.bandwidth * 1e6
        # час комунікації
        Tcomm = K * (self.latency + (self.word_size * m) / bandwidth_bytes)
        # загальний час
        Tp = Tcalc + Tcomm
        # gослідовний час
        T1 = W1 * tau
        # прискорення та ефективність
        Sp = T1 / Tp if Tp > 0 else 0
        Ep = Sp / p if p > 0 else 0
              
        return {
            'W1': W1,
            'W': W,
            'K': K,
            'm': m,
            'Tcalc': Tcalc,
            'Tcomm': Tcomm,
            'Tp': Tp,
            'T1': T1,
            'Sp': Sp,
            'Ep': Ep
        }
    
    def _get_algorithm_params(self, algorithm, n, p, topology='hypercube', l=None, k=None):
        
        if l is None:
            l = p/2
        if k is None:
            k = math.log2(p) if p > 1 else 1
        
        params = {
            'Кеннона': {
                'W1': 2 * n**3 - n**2,
                'W': (2 * n**3 - n**2) / p,
                'K': 2 * (math.sqrt(p) - 1),
                'm': n**2 / p
            },
            'Фокса': {
                'W1': 2 * n**3 - n**2,
                'W': (2 * n**3 - n**2) / p,
                'K': math.sqrt(p) * math.log2(math.sqrt(p)) + math.sqrt(p) - 1,
                'm': n**2 / p
            },
            'Стрічковий': {
                'W1': 2 * n**3 - n**2,
                'W': (2 * n**3 - n**2) / p,
                'K': p - 1,
                'm': n**2 / p
            },
            
            'Бульбашкове': {
                'W1': n * math.log2(n),
                'W': (n / p) * math.log2(n / p) + 2 * n,
                'K': p,
                'm': n / p
            },
            'Швидке': {
                'W1': n * math.log2(n),
                'W': (n / p) * math.log2(n),        # = (n/p)log2(n/p) + (n/p)log2(p)
                'K': math.log2(p),
                'm': n / (2 * p)
            },
            'Шелла': {
                'W1': n * math.log2(n),
                'W': (n / p) * math.log2(n / p) + (math.log2(p) + l) * (2 * n / p),
                'K': math.log2(p) + l,
                'm': n / p
            },
            
            'Гауса': {
                'W1': (2 * n**3 + 3 * n**2 - 5 * n) / 3 + (n**2 + n) / 2,
                'W': (2 * n**3 + 3 * n**2 - 5 * n) / (3 * min(n, p)) + (n**2 + n) / 2, #min
                'K': 2 * (n - 1),
                'm': (n - 1) / 2
            },
                       
            'Дейкстри': {
                'W1': (n - 1) * 2 * n,
                'W': (n - 1) * ((3 * n / min(n, p)) + math.log2(min(n, p))),   # гіперкуб  #min
                'K': (n - 1) * math.log2(p),                   # гіперкуб
                'm': 2
            },
            'Пріма': {
                'W1': (n - 1) * 2 * n,
                'W': (n - 1) * ((2 * n / min(n, p)) + math.log2(min(n, p))),   # гіперкуб  #min
                'K': (n - 1) * math.log2(p),                   # гіперкуб
                'm': 2
            },
            'Флойда': {
                'W1': 2 * n**3,
                'W': (2 * n**3) / p,
                'K': n * math.log2(math.sqrt(p)),
                'm': n / math.sqrt(p)
            },
            
            'Горизонтальний розподіл': {
                'W1': n**2,
                'W': n**2 / p,
                'K': math.log2(p),
                'm': 2**(k - 1) * (n / p)
            },
        }

        if algorithm not in params:
            raise ValueError(f"Невідомий алгоритм: {algorithm}")
        
        alg_params = params[algorithm].copy()

        if algorithm in ['Дейкстри', 'Пріма']:
            if topology == 'star':
                # зірка
                if algorithm == 'Дейкстри':
                    alg_params['W'] = (n - 1) * ((3 * n / min(n, p)) + p - 1) #min
                else:  # Пріма
                    alg_params['W'] = (n - 1) * ((2 * n / min(n, p)) + p - 1) #min
                alg_params['K'] = (n - 1) * 2
            
        return alg_params
    
    def format_time(self, seconds):
        if seconds < 1e-6:
            return f"{seconds * 1e9:.2f} нс"
        elif seconds < 1e-3:
            return f"{seconds * 1e6:.2f} мкс"
        elif seconds < 1:
            return f"{seconds * 1e3:.2f} мс"
        elif seconds < 60:
            return f"{seconds:.4f} с"
        elif seconds < 3600:
            return f"{seconds / 60:.2f} хв"
        else:
            return f"{seconds / 3600:.2f} год"
    
    def format_results(self, results):
        return (
            "─" * 35 + "\n"
            "Результати аналітичної моделі\n\n"
            f"Обчислення:\n"
            f"  W (операцій): {results['W']:,.0f}\n"
            f"  Tcalc: {self.format_time(results['Tcalc'])}\n\n"
            f"Комунікації:\n"
            f"  K (актів комунікації): {results['K']:.0f}\n"
            f"  m (розмір повідомлення): {results['m']:.2f}\n"
            f"  Tcomm: {self.format_time(results['Tcomm'])}\n\n"
            f"Загальний час:\n"
            f"  Tp: {self.format_time(results['Tp'])}\n"
            f"  T1 (послідовно): {self.format_time(results['T1'])}\n\n"
            f"Прискорення: Sp = {results['Sp']:.2f}x\n"
            f"Ефективність: Ep = {results['Ep']:.2%}\n"
        )