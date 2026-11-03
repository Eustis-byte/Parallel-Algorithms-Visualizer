class MessageAnimator:
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.processor_positions = []
        self.message_ids = []
        self.show_labels = False
    
    def draw_message(self, msg, from_pos, to_pos):
        x = from_pos[0] + (to_pos[0] - from_pos[0]) * msg.progress
        y = from_pos[1] + (to_pos[1] - from_pos[1]) * msg.progress
        
        circle_id = self.canvas.create_oval(
            x-14, y-14, x+14, y+14,
            fill="red", outline="darkred", width=2,
            tags="message"
        )
        self.message_ids.append(circle_id)
        
        if self.show_labels and msg.data and isinstance(msg.data, dict):
            label = msg.data.get("label")
            if label:
                text_id = self.canvas.create_text(
                    x, y, text=label,
                    font=("Arial", 8, "bold"),
                    fill="white", tags="message"
                )
                self.message_ids.append(text_id)
        
        return circle_id
    
    def draw_messages(self, messages):
        for msg in messages:
            if msg.from_processor < len(self.processor_positions) and \
               msg.to_processor < len(self.processor_positions):
                from_pos = self.processor_positions[msg.from_processor]
                to_pos = self.processor_positions[msg.to_processor]
                self.draw_message(msg, from_pos, to_pos)
    
    def clear_messages(self):
        self.canvas.delete("message")
        self.message_ids.clear()