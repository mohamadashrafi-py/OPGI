from OpenGL import GLUT as glut
import glfw
import OpenGL.GL as gl
import math


from OpenGL import GLUT as glut
import glfw
import OpenGL.GL as gl
import math


class Layout:
    """Base class for all layout managers"""

    def __init__(self, x=0, y=0, width=100, height=100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.widgets = []
        self.padding = 5
        self.spacing = 5
        self.app = None
        self.visible = True

        # Relative positioning/sizing
        self.relative_x = None
        self.relative_y = None
        self.relative_width = None
        self.relative_height = None

    def set_relative_position(self, rel_x, rel_y):
        """Set position as percentage of window size (0.0 to 1.0)"""
        self.relative_x = rel_x
        self.relative_y = rel_y

    def set_relative_size(self, rel_width, rel_height):
        """Set size as percentage of window size (0.0 to 1.0)"""
        self.relative_width = rel_width
        self.relative_height = rel_height

    def update_from_window_size(self, window_width, window_height):
        """Update layout based on window size"""
        if self.relative_x is not None:
            self.x = int(window_width * self.relative_x)
        if self.relative_y is not None:
            self.y = int(window_height * self.relative_y)
        if self.relative_width is not None:
            self.width = int(window_width * self.relative_width)
        if self.relative_height is not None:
            self.height = int(window_height * self.relative_height)

        self.update_layout()

    def add_widget(self, widget):
        self.widgets.append(widget)
        widget.app = self.app
        return widget

    def remove_widget(self, widget):
        if widget in self.widgets:
            self.widgets.remove(widget)

    def clear(self):
        self.widgets.clear()

    def update_layout(self):
        pass

    def draw(self):
        if not self.visible:
            return

        for widget in self.widgets:
            if hasattr(widget, "visible") and not widget.visible:
                continue
            if hasattr(widget, "draw"):
                widget.draw()

    def contains(self, x, y):
        return (
            self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
        )


class VerticalLayout(Layout):
    def __init__(self, x=0, y=0, width=100, height=100):
        super().__init__(x, y, width, height)

    def update_layout(self):
        if not self.widgets:
            return

        total_spacing = self.spacing * (len(self.widgets) - 1)
        available_height = self.height - total_spacing - (self.padding * 2)
        widget_height = available_height / len(self.widgets)

        current_y = self.y + self.padding

        for widget in self.widgets:
            widget.x = self.x + self.padding
            widget.y = current_y
            widget.width = self.width - (self.padding * 2)
            widget.height = widget_height

            current_y += widget_height + self.spacing

            if hasattr(widget, "update_layout"):
                widget.update_layout()


class HorizontalLayout(Layout):
    def __init__(self, x=0, y=0, width=100, height=100):
        super().__init__(x, y, width, height)

    def update_layout(self):
        if not self.widgets:
            return

        total_spacing = self.spacing * (len(self.widgets) - 1)
        available_width = self.width - total_spacing - (self.padding * 2)
        widget_width = available_width / len(self.widgets)

        current_x = self.x + self.padding

        for widget in self.widgets:
            widget.x = current_x
            widget.y = self.y + self.padding
            widget.width = widget_width
            widget.height = self.height - (self.padding * 2)

            current_x += widget_width + self.spacing

            if hasattr(widget, "update_layout"):
                widget.update_layout()


class GridLayout(Layout):
    def __init__(self, x=0, y=0, width=100, height=100, rows=2, cols=2):
        super().__init__(x, y, width, height)
        self.rows = rows
        self.cols = cols

    def update_layout(self):
        if not self.widgets:
            return

        total_row_spacing = self.spacing * (self.rows - 1)
        total_col_spacing = self.spacing * (self.cols - 1)

        cell_width = (self.width - total_col_spacing - (self.padding * 2)) / self.cols
        cell_height = (self.height - total_row_spacing - (self.padding * 2)) / self.rows

        for i, widget in enumerate(self.widgets):
            if i >= self.rows * self.cols:
                break

            row = i // self.cols
            col = i % self.cols

            widget.x = self.x + self.padding + col * (cell_width + self.spacing)
            widget.y = self.y + self.padding + row * (cell_height + self.spacing)
            widget.width = cell_width
            widget.height = cell_height

            if hasattr(widget, "update_layout"):
                widget.update_layout()
