import math
import tkinter as tk

class TopologyDrawer:
    def __init__(self, num_processors):
        self.num_processors = num_processors
        self.processor_positions = []

    def draw(self, canvas, width, height):
        canvas.delete("all")
        self._calculate_positions(width, height)
        self._draw_connections(canvas)
        self._draw_processors(canvas)

    def _calculate_positions(self, width, height):
        raise NotImplementedError

    def _draw_processors(self, canvas):
        for i, (x, y) in enumerate(self.processor_positions):
            canvas.create_oval(x-15, y-15, x+15, y+15,
                               fill="lightblue", outline="black", width=2,
                               tags=f"proc_{i}")
            canvas.create_text(x, y, text=str(i), font=("Arial", 10, "bold"),
                               tags=f"proc_label_{i}")

    def _draw_connections(self, canvas):
        pass
    
    def _calculate_circle_positions(self, width, height, radius_factor=0.35):
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) * radius_factor
        self.processor_positions = []
        for i in range(self.num_processors):
            angle = 2 * math.pi * i / self.num_processors
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.processor_positions.append((x, y))

class GridDrawer(TopologyDrawer):
  
    def __init__(self, num_processors, numbering="normal"):
        self.numbering = numbering  # "normal" / "snake"
        super().__init__(num_processors)
    
    def _calculate_positions(self, width, height):
        n = self.num_processors
        
        best_rows = 1
        best_cols = n
        min_diff = float('inf')
        
        for rows in range(1, int(math.sqrt(n)) + 1):
            if n % rows == 0:
                cols = n // rows
                diff = abs(rows - cols)
                if diff < min_diff:
                    min_diff = diff
                    best_rows = rows
                    best_cols = cols
        
        self.rows = best_rows
        self.cols = best_cols
        
        margin = 40
        cell_width = (width - 2*margin) / self.cols
        cell_height = (height - 2*margin) / self.rows
        
        if self.numbering == "snake":
            self._calculate_snake_positions(margin, cell_width, cell_height)
        else:
            self._calculate_normal_positions(margin, cell_width, cell_height)
    
    def _calculate_normal_positions(self, margin, cell_width, cell_height):
        n = self.num_processors
        self.processor_positions = []
        self.position_to_proc = {}
        
        for i in range(n):
            r = i // self.cols
            c = i % self.cols
            x = margin + c * cell_width + cell_width/2
            y = margin + r * cell_height + cell_height/2
            self.processor_positions.append((x, y))
            self.position_to_proc[(r, c)] = i
    
    def _calculate_snake_positions(self, margin, cell_width, cell_height):
        n = self.num_processors
        
        grid_positions = []
        for r in range(self.rows):
            row_positions = []
            for c in range(self.cols):
                x = margin + c * cell_width + cell_width/2
                y = margin + r * cell_height + cell_height/2
                row_positions.append((x, y))
            grid_positions.append(row_positions)
        
        self.processor_positions = [None] * n
        self.position_to_proc = {}
        
        for r in range(self.rows):
            for c in range(self.cols):
                x, y = grid_positions[r][c]
                
                if r % 2 == 0:
                    proc_num = r * self.cols + c
                else:  
                    proc_num = r * self.cols + (self.cols - 1 - c)
                
                self.processor_positions[proc_num] = (x, y)
                self.position_to_proc[(r, c)] = proc_num
    
    def _draw_connections(self, canvas):
        for r in range(self.rows):
            for c in range(self.cols):
                current_proc = self.position_to_proc.get((r, c))
                if current_proc is None:
                    continue
                
                x1, y1 = self.processor_positions[current_proc]
                
                if c + 1 < self.cols:
                    right_proc = self.position_to_proc.get((r, c + 1))
                    if right_proc is not None:
                        x2, y2 = self.processor_positions[right_proc]
                        canvas.create_line(x1, y1, x2, y2, fill="gray", width=2)
                
                if r + 1 < self.rows:
                    bottom_proc = self.position_to_proc.get((r + 1, c))
                    if bottom_proc is not None:
                        x2, y2 = self.processor_positions[bottom_proc]
                        canvas.create_line(x1, y1, x2, y2, fill="gray", width=2)

class RingDrawer(TopologyDrawer):
    def _calculate_positions(self, width, height):
        self._calculate_circle_positions(width, height, 0.35)

    def _draw_connections(self, canvas):
        n = self.num_processors
        for i in range(n):
            x1, y1 = self.processor_positions[i]
            j = (i + 1) % n
            x2, y2 = self.processor_positions[j]
            canvas.create_line(x1, y1, x2, y2, fill="gray", width=1)

class LineDrawer(TopologyDrawer):
    def _calculate_positions(self, width, height):
        margin = 60
        start_x = margin
        end_x = width - margin
        if self.num_processors > 1:
            step = (end_x - start_x) / (self.num_processors - 1)
        else:
            step = 0
        y = height / 2
        self.processor_positions = []
        for i in range(self.num_processors):
            x = start_x + i * step
            self.processor_positions.append((x, y))

    def _draw_connections(self, canvas):
        for i in range(self.num_processors - 1):
            x1, y1 = self.processor_positions[i]
            x2, y2 = self.processor_positions[i+1]
            canvas.create_line(x1, y1, x2, y2, fill="gray", width=1)

class CubeDrawer(TopologyDrawer):
    
    def __init__(self, num_processors, numbering="normal"):
        self.numbering = numbering  # "normal" / "snake"
        self.original_order = None
        super().__init__(num_processors)
    
    def _calculate_positions(self, width, height):
        n = self.num_processors
        
        if n == 4:
            self._draw_2d_cube(width, height)
        elif n == 8:
            self._draw_3d_cube(width, height)
        elif n == 16:
            self._draw_4d_hypercube(width, height)
        else:
            self._calculate_circle_positions(width, height, 0.3)
        
        if self.numbering == "snake":
            self._apply_snake_numbering()
        
        self._create_position_map(width, height)
    
    def _apply_snake_numbering(self):
        n = self.num_processors
        
        snake_paths = {
            4: [0, 1, 3, 2],
            8: [0, 1, 3, 2, 6, 7, 5, 4],
            16: [0, 1, 3, 2, 6, 7, 5, 4, 12, 13, 15, 14, 10, 11, 9, 8]
        }
        
        snake_order = snake_paths.get(n)
        if not snake_order:
            return
        
        self.original_order = snake_order
        
        old_positions = self.processor_positions.copy()
        self.processor_positions = [None] * n
        
        for new_idx, old_idx in enumerate(snake_order):
            if old_idx < len(old_positions):
                self.processor_positions[new_idx] = old_positions[old_idx]
    
    def _create_position_map(self, width, height):
        self.position_to_proc = {}
        
        margin = 40
        for i, (x, y) in enumerate(self.processor_positions):
            grid_x = int((x - margin) // 100)
            grid_y = int((y - margin) // 100)
            self.position_to_proc[(grid_y, grid_x)] = i

    def _draw_2d_cube(self, width, height):
        center_x = width / 2
        center_y = height / 2
        size = min(width, height) * 0.3
        
        offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        
        self.processor_positions = []
        for dx, dy in offsets:
            x = center_x + dx * size
            y = center_y + dy * size
            self.processor_positions.append((x, y))

    def _draw_3d_cube(self, width, height):
        center_x = width / 2
        center_y = height / 2
        scale = min(width, height) * 0.25
        
        self.processor_positions = []
        offsets = [
            (-1, -1, -1), (1, -1, -1), (-1, 1, -1), (1, 1, -1),
            (-1, -1, 1), (1, -1, 1), (-1, 1, 1), (1, 1, 1)
        ]
        
        for dx, dy, dz in offsets:
            x = center_x + (dx * 0.8 + dy * 0.4) * scale
            y = center_y + (dz * 0.7 + dy * 0.3) * scale
            self.processor_positions.append((x, y))

    def _draw_4d_hypercube(self, width, height):
        center_x = width / 2
        center_y = height / 2
        scale = min(width, height) * 0.2
        
        self.processor_positions = []
        
        vertices_4d = []
        for w in [-1, 1]:
            for z in [-1, 1]:
                for y in [-1, 1]:
                    for x in [-1, 1]:
                        vertices_4d.append((x, y, z, w))
        
        for x, y, z, w in vertices_4d:
            w_factor = 1.0 - w * 0.3  # для w=-1: 1.3, для w=1: 0.7
            
            x2d = center_x + (x * 0.8 + y * 0.4) * scale * w_factor
            y2d = center_y + (z * 0.7 + y * 0.3) * scale * w_factor
            
            self.processor_positions.append((x2d, y2d))

    def _get_hypercube_connections(self):
        n = self.num_processors
        
        dim = 0
        temp = n
        while temp > 1:
            temp >>= 1
            dim += 1
        
        connections = []
        drawn_pairs = set()
        
        if self.numbering == "snake" and self.original_order:
            original_to_current = {}
            for new_idx, old_idx in enumerate(self.original_order):
                original_to_current[old_idx] = new_idx
            
            for old_i in range(n):
                for bit in range(dim):
                    old_j = old_i ^ (1 << bit)
                    if old_j > old_i:
                        if old_i in original_to_current and old_j in original_to_current:
                            curr_i = original_to_current[old_i]
                            curr_j = original_to_current[old_j]
                            pair = (min(curr_i, curr_j), max(curr_i, curr_j))
                            if pair not in drawn_pairs:
                                drawn_pairs.add(pair)
                                connections.append(pair)
        else:
            for i in range(n):
                for bit in range(dim):
                    j = i ^ (1 << bit)
                    if j > i and j < n:
                        pair = (min(i, j), max(i, j))
                        if pair not in drawn_pairs:
                            drawn_pairs.add(pair)
                            connections.append(pair)
        
        return connections

    def _draw_connections(self, canvas):
        n = self.num_processors
        connections = self._get_hypercube_connections()
        
        for i, j in connections:
            if i < len(self.processor_positions) and j < len(self.processor_positions):
                x1, y1 = self.processor_positions[i]
                x2, y2 = self.processor_positions[j]
                
                if n == 16:
                    canvas.create_line(x1, y1, x2, y2, fill="gray", width=1, dash=(2, 2))
                else:
                    canvas.create_line(x1, y1, x2, y2, fill="gray", width=1)             

class CompleteGraphDrawer(TopologyDrawer):
    def _calculate_positions(self, width, height):
        self._calculate_circle_positions(width, height, 0.35)

    def _draw_connections(self, canvas):
        n = self.num_processors
        for i in range(n):
            for j in range(i+1, n):
                x1, y1 = self.processor_positions[i]
                x2, y2 = self.processor_positions[j]
                canvas.create_line(x1, y1, x2, y2, fill="lightgray", width=1,
                                   dash=(2, 2))

class StarDrawer(TopologyDrawer):
    def _calculate_positions(self, width, height):
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) * 0.3
        self.processor_positions = []
 
        self.processor_positions.append((center_x, center_y))

        for i in range(1, self.num_processors):
            angle = 2 * math.pi * (i-1) / max(1, self.num_processors - 1)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.processor_positions.append((x, y))

    def _draw_connections(self, canvas):
        if self.num_processors < 2:
            return
        cx, cy = self.processor_positions[0]
        for i in range(1, self.num_processors):
            x, y = self.processor_positions[i]
            canvas.create_line(cx, cy, x, y, fill="gray", width=1)