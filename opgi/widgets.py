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
