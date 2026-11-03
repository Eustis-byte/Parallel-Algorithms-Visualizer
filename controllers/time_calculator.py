from models import TimeModel

class TimeCalculator:

    @staticmethod
    def create_model(params):
        return TimeModel(
            base_operation_time=params.get('base_operation_time', 10.0),
            latency=params.get('latency', 0.001) / 1000,
            bandwidth=params.get('bandwidth', 100.0)
        )

    def calculate(self, params):
        try:
            time_model = self.create_model(params)
            results = time_model.calculate(
                algorithm=params['method'],
                n=params['dimension'],
                p=params['num_processors']
            )
            return time_model.format_results(results)
        except Exception as e:
            return f"Помилка розрахунку часу: {str(e)}"