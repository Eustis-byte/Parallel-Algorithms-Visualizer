class Animator:
    def __init__(self, algorithm, visualizer):
        self.algorithm = algorithm
        self.visualizer = visualizer
        self.current_step = 0
        self.steps = []
        self.messages_in_transit = []
    
    def set_steps(self, steps):
        self.steps = steps
        if steps and steps[0].messages:
            self.messages_in_transit = steps[0].messages.copy()
    
    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            step = self.steps[self.current_step]
            self.messages_in_transit = step.messages.copy()
            return True
        return False
    
    def go_to_step(self, step_num):
        if 0 <= step_num < len(self.steps):
            self.current_step = step_num
            step = self.steps[step_num]
            self.messages_in_transit = step.messages.copy()
            return True
        return False
    
    def get_current_messages(self):
        return self.messages_in_transit
    
    def reset(self):
        if self.steps:
            self.current_step = 0
            self.messages_in_transit = self.steps[0].messages.copy()