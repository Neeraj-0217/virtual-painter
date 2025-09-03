import numpy as np
import cv2

colors = [
    (0,0,255),  # Red
    (0,255,0),  # Green
    (255,0,0),  # Blue
    (0,255,255) # Yellow
]

class Canvas:
    def __init__(self, width: int, height: int, bg_color=(0,0,0)):
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.canvas = np.full((height, width, 3), bg_color, dtype=np.uint8)

        # Toolbar properties
        self.colors = colors
        self.color_idx = 0
        self.box_size = 60
        self.padding = 10
        self.toolbar_y = 10
        self.toolbar_x = 10

    def draw_line(self, start_point, end_point, thickness = 5):
        cv2.line(self.canvas, start_point, end_point, self.colors[self.color_idx], thickness)

    def overlay_on(self, frame):
        # Combine canvas with current frame
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
        canvas_fg = cv2.bitwise_and(self.canvas, self.canvas, mask=mask)
        output = cv2.add(frame_bg, canvas_fg)

        return self.draw_toolbar(output)
    
    def erase(self, start_point, end_point, thickness=20):
        cv2.line(self.canvas, start_point, end_point, self.bg_color, thickness)

    def draw_toolbar(self, frame):
        for i, color in enumerate(self.colors):
            top_left = (self.toolbar_x + i*(self.box_size+self.padding), self.toolbar_y)
            bottom_right = (top_left[0]+self.box_size, top_left[1]+self.box_size)

            cv2.rectangle(frame, top_left, bottom_right, color, -1)

            if i == self.color_idx:
                cv2.rectangle(frame, top_left, bottom_right, (0, 0, 0), 3)

        return frame
    
    def check_toolbar_selection(self, x, y):
        for i, color in enumerate(self.colors):
            left = self.toolbar_x + i*(self.box_size+self.padding)
            right = left + self.box_size
            top = self.toolbar_y
            bottom = self.toolbar_y + self.box_size

            if left <= x <= right and top <= y <= bottom:
                self.color_idx = i
                return True
            
        return False
        
    def reset(self):
        self.canvas = np.full((self.height, self.width, 3), self.bg_color, dtype=np.uint8)

    def save(self, filename):
        cv2.imwrite(filename, self.canvas)


