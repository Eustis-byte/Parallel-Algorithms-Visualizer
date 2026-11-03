from animation.factories.algorithm_factory import AlgorithmFactory
from animation.core.animator import Animator
from animation.core.message_animator import MessageAnimator

class AnimationController:
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.animator = None
        self.is_playing = False
        self.speed = 1.0
        self.canvas = None
        self._local_step_wait_counter = 0  # Лічильник затримки для локальних кроків
    
    def set_canvas(self, canvas):
        self.canvas = canvas
    
    def load_animation(self, params, topology):
        if self.canvas is None:
            raise ValueError("Полотно не встановлено")
        
        algorithm = AlgorithmFactory.create(params['method'], params['task'])
        
        message_animator = MessageAnimator(self.canvas)
        message_animator.show_labels = (params['task'] in ["Матриця * матриця", "СЛАР"])
        
        if hasattr(topology, 'processor_positions'):
            message_animator.processor_positions = topology.processor_positions
        
        self.animator = Animator(algorithm, message_animator)
        steps = algorithm.generate_steps(topology, params)
        self.animator.set_steps(steps)
        
        # Оновлюємо панель
        self._update_panel()
        
        return steps, self.animator
    
    def get_step(self, step_num):
        if self.animator and 0 <= step_num < len(self.animator.steps):
            return self.animator.steps[step_num]
        return None
    
    def full_reset(self):
        self.is_playing = False
        self._local_step_wait_counter = 0
        if self.animator:
            if hasattr(self.animator, 'visualizer'):
                self.animator.visualizer.clear_messages()
        self.animator = None

    def _update_panel(self): # Оновлює панель анімації
        if not self.animator:
            return
        panel = self.main_window.animation_panel
        if panel:
            step = self.animator.current_step
            total = len(self.animator.steps)
            description = self.animator.steps[step].description if self.animator.steps else ""
            if panel.total_steps != total:
                panel.set_steps(total)
            panel.update_step(step, description)
    
    def draw_step(self, step_num): # Отрисовывает шаг
        if not self.animator:
            return
        if self.animator.go_to_step(step_num):
            self.animator.visualizer.clear_messages()
            self.animator.visualizer.draw_messages(self.animator.get_current_messages())
            self._update_panel()
    
    def play(self): # Запускает воспроизведение
        if not self.animator or not self.animator.steps:
            return
        
        if self.animator.current_step == len(self.animator.steps) - 1:
            self.animator.reset()
            self.draw_step(0)
        
        self.is_playing = True
        self._local_step_wait_counter = 0
        self.main_window.animation_panel.set_playing(True)
        self.animate()
    
    def pause(self):
        self.is_playing = False
        self.main_window.animation_panel.set_playing(False)
    
    def stop(self): # Остановка
        self.is_playing = False
        self._local_step_wait_counter = 0
        self.animator.reset()
        self.draw_step(0)
        self.main_window.animation_panel.set_playing(False)
        self._update_panel()
    
    def step_forward(self): # Шаг вперед
        if self.animator.next_step():
            self.draw_step(self.animator.current_step)
            self._update_panel()
    
    def go_to_step(self, step_num): # Переход к шагу
        if self.animator.go_to_step(step_num):
            self.draw_step(step_num)
            self._update_panel()
    
    def set_speed(self, speed):
        self.speed = speed
    
    def animate(self): # Цикл анимации
        if not self.is_playing:
            return
        current_messages = self.animator.get_current_messages()
        # Перевірка: якщо крок локальний (немає повідомлень у дорозі)
        if not current_messages and self.animator.current_step < len(self.animator.steps) - 1:
            # Визначаємо кількість тіків очікування (наприклад, базово 20 тіків)
            max_wait_ticks = int(8 / self.speed)
            if self._local_step_wait_counter < max_wait_ticks:
                self._local_step_wait_counter += 1
            else:
                # Час очікування минув, переходимо до наступного кроку
                self._local_step_wait_counter = 0
                self.animator.next_step()
                self.draw_step(self.animator.current_step)
                self._update_panel()
        else:
            # Звичайний рух повідомлень
            self._local_step_wait_counter = 0
            delivered = []
            for msg in current_messages:
                msg.progress += 0.02 * self.speed
                if msg.progress >= 1.0:
                    delivered.append(msg)
            
            for msg in delivered:
                self.animator.messages_in_transit.remove(msg)
            
            if not current_messages and self.animator.current_step < len(self.animator.steps) - 1:
                self.animator.next_step()
                self.draw_step(self.animator.current_step)
                self._update_panel()
            else:
                self.animator.visualizer.clear_messages()
                self.animator.visualizer.draw_messages(current_messages)
        
        delay = int(50 / self.speed)
        self.main_window.after(delay, self.animate)