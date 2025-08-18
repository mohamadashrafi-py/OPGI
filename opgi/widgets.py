import math

import glfw
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


class TextInput(Widget):
    def __init__(self, x, y, width=200, height=30):
        super().__init__(x, y, width, height)
        self.text = ""
        self.active = False

    def on_key_press(self, key, action):
        if action == glfw.PRESS and key == glfw.KEY_BACKSPACE:
            self.text = self.text[:-1]

    def on_char_input(self, char):
        self.text += chr(char)

    def draw(self):
        # Draw background
        gl.glColor3f(1, 1, 1)
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(self.x, self.y)
        gl.glVertex2f(self.x + self.width, self.y)
        gl.glVertex2f(self.x + self.width, self.y + self.height)
        gl.glVertex2f(self.x, self.y + self.height)
        gl.glEnd()

        # Draw border (blue if active, gray if not)
        border_color = (
            (0.2, 0.5, 0.8) if (self.app.focused_widget == self) else (0.7, 0.7, 0.7)
        )
        gl.glColor3f(*border_color)
        gl.glLineWidth(2)
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glVertex2f(self.x, self.y)
        gl.glVertex2f(self.x + self.width, self.y)
        gl.glVertex2f(self.x + self.width, self.y + self.height)
        gl.glVertex2f(self.x, self.y + self.height)
        gl.glEnd()

        # Draw text
        gl.glColor3f(0, 0, 0)
        gl.glRasterPos2f(self.x + 5, self.y + self.height // 2 + 5)
        for char in self.text:
            glut.glutBitmapCharacter(glut.GLUT_BITMAP_HELVETICA_18, ord(char))

        # Draw cursor if focused
        if self.app.focused_widget == self:
            text_width = sum(
                glut.glutBitmapWidth(glut.GLUT_BITMAP_HELVETICA_18, ord(c))
                for c in self.text
            )
            cursor_x = self.x + 5 + text_width
            alpha = 0.5 + 0.5 * math.sin(glfw.get_time() * 5)  # Blinking effect
            gl.glColor4f(0.2, 0.2, 0.2, alpha)
            gl.glBegin(gl.GL_QUADS)
            gl.glVertex2f(cursor_x, self.y + 5)
            gl.glVertex2f(cursor_x + 2, self.y + 5)
            gl.glVertex2f(cursor_x + 2, self.y + self.height - 5)
            gl.glVertex2f(cursor_x, self.y + self.height - 5)
            gl.glEnd()
