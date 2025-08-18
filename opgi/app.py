import glfw
import OpenGL.GL as gl
from OpenGL import GLUT as glut


class App:
    def __init__(self, width=800, height=600, title="Simple GUI"):
        self.width = width
        self.height = height
        self.widgets = []
        self.focused_widget = None

        if not glfw.init():
            raise RuntimeError("GLFW init failed")

        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Window creation failed")

        glfw.make_context_current(self.window)
        glut.glutInit()

        # Set callbacks
        glfw.set_mouse_button_callback(self.window, self.on_mouse_click)
        glfw.set_key_callback(self.window, self.on_key_press)
        glfw.set_char_callback(self.window, self.on_char_input)

        gl.glClearColor(0.95, 0.95, 0.95, 1)
        self.setup_projection()

    def setup_projection(self):
        gl.glViewport(0, 0, self.width, self.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, self.width, self.height, 0, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def add_widget(self, widget):
        widget.app = self
        self.widgets.append(widget)
        return widget

    def run(self):
        while not glfw.window_should_close(self.window):
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            for widget in self.widgets:
                widget.draw()

            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.terminate()
