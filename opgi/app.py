import glfw
import OpenGL.GL as gl
from OpenGL import GLUT as glut


import glfw
import OpenGL.GL as gl
from OpenGL import GLUT as glut


class App:
    def __init__(self, width=800, height=600, title="Simple GUI"):
        self.width = width
        self.height = height
        self.original_width = width
        self.original_height = height
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
        glfw.set_window_size_callback(self.window, self.on_window_resize)
        glfw.set_cursor_pos_callback(self.window, self.on_mouse_move)

        gl.glClearColor(0.95, 0.95, 0.95, 1)
        self.setup_projection()

    def on_window_resize(self, window, width, height):
        """Handle window resize events"""
        if width > 0 and height > 0:  # Prevent division by zero
            self.width = width
            self.height = height
            self.setup_projection()
            self.update_layouts()
            print(f"Window resized to: {width}x{height}")  # Debug output

    def setup_projection(self):
        """Update OpenGL projection matrix for new window size"""
        gl.glViewport(0, 0, self.width, self.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, self.width, self.height, 0, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)

        # Clear the entire window to avoid black areas
        gl.glClearColor(1.0, 1.0, 1.0, 1.0)  # White background
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    def on_mouse_click(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            x, y = glfw.get_cursor_pos(window)
            self.focused_widget = None

            for widget in self.widgets:
                if hasattr(widget, "contains") and widget.contains(x, y):
                    self.focused_widget = widget
                    if hasattr(widget, "on_click"):
                        widget.on_click()
                    break

    def on_mouse_move(self, window, x, y):
        for widget in self.widgets:
            if hasattr(widget, "on_mouse_move"):
                widget.on_mouse_move(x, y)

    def on_key_press(self, window, key, scancode, action, mods):
        if self.focused_widget and hasattr(self.focused_widget, "on_key_press"):
            self.focused_widget.on_key_press(key, action)

    def on_char_input(self, window, char):
        if self.focused_widget and hasattr(self.focused_widget, "on_char_input"):
            self.focused_widget.on_char_input(char)

    def add_widget(self, widget):
        widget.app = self
        self.widgets.append(widget)
        return widget

    def update_layouts(self):
        """Update all layouts in the application"""
        for widget in self.widgets:
            if hasattr(widget, "update_layout"):
                widget.update_layout()
            # Update relative layouts
            if hasattr(widget, "update_from_window_size"):
                widget.update_from_window_size(self.width, self.height)

    def run(self):
        """Start the main application loop"""
        while not glfw.window_should_close(self.window):
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            # Draw all widgets
            for widget in self.widgets:
                if hasattr(widget, "visible") and not widget.visible:
                    continue
                if hasattr(widget, "draw"):
                    widget.draw()

            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.terminate()
