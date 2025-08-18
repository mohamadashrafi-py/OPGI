import OpenGL.GL as gl
from OpenGL import GLUT as glut


class Widget:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.app = None

    def contains(self, x, y):
        return (
            self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
        )

    def draw(self):
        pass


class Label(Widget):
    def __init__(self, text, x, y, color=(0, 0, 0)):
        super().__init__(x, y, 0, 0)  # Width/height not used for label
        self.text = text
        self.color = color

    def draw(self):
        gl.glColor3f(*self.color)
        gl.glRasterPos2f(self.x, self.y)
        for char in self.text:
            glut.glutBitmapCharacter(glut.GLUT_BITMAP_HELVETICA_18, ord(char))


class Button(Widget):
    def __init__(self, text, x, y, width=100, height=40):
        super().__init__(x, y, width, height)
        self.text = text
        self.color = (0.2, 0.5, 0.8)
        self.pressed = False
        self.on_click_callback = None

    def on_click(self):
        if self.on_click_callback:
            self.on_click_callback()

    def set_on_click(self, callback):
        self.on_click_callback = callback

    def draw(self):
        # Draw button background
        gl.glColor3f(*self.color)
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(self.x, self.y)
        gl.glVertex2f(self.x + self.width, self.y)
        gl.glVertex2f(self.x + self.width, self.y + self.height)
        gl.glVertex2f(self.x, self.y + self.height)
        gl.glEnd()

        # Draw button text
        text_width = sum(
            glut.glutBitmapWidth(glut.GLUT_BITMAP_HELVETICA_18, ord(c))
            for c in self.text
        )
        text_x = self.x + (self.width - text_width) // 2
        text_y = self.y + self.height // 2 + 5

        gl.glColor3f(1, 1, 1)
        gl.glRasterPos2f(text_x, text_y)
        for char in self.text:
            glut.glutBitmapCharacter(glut.GLUT_BITMAP_HELVETICA_18, ord(char))
