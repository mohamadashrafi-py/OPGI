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

    def add_widget(self, widget):
        """Add a widget to the layout"""
        self.widgets.append(widget)
        widget.app = self.app
        return widget

    def remove_widget(self, widget):
        """Remove a widget from the layout"""
        if widget in self.widgets:
            self.widgets.remove(widget)

    def clear(self):
        """Remove all widgets from the layout"""
        self.widgets.clear()

    def update_layout(self):
        """Update the positions and sizes of all widgets (to be implemented by subclasses)"""
        pass

    def draw(self):
        """Draw the layout and all its widgets"""
        if not self.visible:
            return

        for widget in self.widgets:
            if hasattr(widget, "visible") and not widget.visible:
                continue
            if hasattr(widget, "draw"):
                widget.draw()

    def contains(self, x, y):
        """Check if point is within layout bounds"""
        return (
            self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
        )


class VerticalLayout(Layout):
    """Arranges widgets vertically with equal width"""

    def __init__(self, x=0, y=0, width=100, height=100):
        super().__init__(x, y, width, height)
        self.alignment = "stretch"  # 'stretch', 'left', 'center', 'right'

    def update_layout(self):
        if not self.widgets:
            return

        total_spacing = self.spacing * (len(self.widgets) - 1)
        available_height = self.height - total_spacing
        widget_height = available_height / len(self.widgets)

        current_y = self.y

        for widget in self.widgets:
            widget.height = widget_height

            # Set horizontal position based on alignment
            if self.alignment == "stretch":
                widget.x = self.x
                widget.width = self.width
            elif self.alignment == "left":
                widget.x = self.x
            elif self.alignment == "center":
                widget.x = self.x + (self.width - widget.width) // 2
            elif self.alignment == "right":
                widget.x = self.x + self.width - widget.width

            widget.y = current_y
            current_y += widget_height + self.spacing

            # Update widget's layout if it has one
            if hasattr(widget, "update_layout"):
                widget.update_layout()


class HorizontalLayout(Layout):
    """Arranges widgets horizontally with equal height"""

    def __init__(self, x=0, y=0, width=100, height=100):
        super().__init__(x, y, width, height)
        self.alignment = "stretch"  # 'stretch', 'top', 'center', 'bottom'

    def update_layout(self):
        if not self.widgets:
            return

        total_spacing = self.spacing * (len(self.widgets) - 1)
        available_width = self.width - total_spacing
        widget_width = available_width / len(self.widgets)

        current_x = self.x

        for widget in self.widgets:
            widget.width = widget_width

            # Set vertical position based on alignment
            if self.alignment == "stretch":
                widget.y = self.y
                widget.height = self.height
            elif self.alignment == "top":
                widget.y = self.y
            elif self.alignment == "center":
                widget.y = self.y + (self.height - widget.height) // 2
            elif self.alignment == "bottom":
                widget.y = self.y + self.height - widget.height

            widget.x = current_x
            current_x += widget_width + self.spacing

            # Update widget's layout if it has one
            if hasattr(widget, "update_layout"):
                widget.update_layout()


class GridLayout(Layout):
    """Arranges widgets in a grid with specified rows and columns"""

    def __init__(self, x=0, y=0, width=100, height=100, rows=2, cols=2):
        super().__init__(x, y, width, height)
        self.rows = rows
        self.cols = cols
        self.row_spacing = 5
        self.col_spacing = 5

    def update_layout(self):
        if not self.widgets:
            return

        # Calculate cell dimensions
        total_row_spacing = self.row_spacing * (self.rows - 1)
        total_col_spacing = self.col_spacing * (self.cols - 1)

        cell_width = (self.width - total_col_spacing) / self.cols
        cell_height = (self.height - total_row_spacing) / self.rows

        # Position widgets in grid
        for i, widget in enumerate(self.widgets):
            if i >= self.rows * self.cols:
                break  # Don't position more widgets than grid cells

            row = i // self.cols
            col = i % self.cols

            widget.x = self.x + col * (cell_width + self.col_spacing)
            widget.y = self.y + row * (cell_height + self.row_spacing)
            widget.width = cell_width
            widget.height = cell_height

            # Update widget's layout if it has one
            if hasattr(widget, "update_layout"):
                widget.update_layout()


class BoxLayout(Layout):
    """A flexible box layout that can arrange widgets with different sizes"""

    def __init__(self, x=0, y=0, width=100, height=100, direction="horizontal"):
        super().__init__(x, y, width, height)
        self.direction = direction  # 'horizontal' or 'vertical'
        self.widget_sizes = []  # List of size weights or fixed sizes

    def update_layout(self):
        if not self.widgets:
            return

        if self.direction == "horizontal":
            self._update_horizontal_layout()
        else:
            self._update_vertical_layout()

    def _update_horizontal_layout(self):
        total_fixed_size = sum(
            size for size in self.widget_sizes if isinstance(size, (int, float))
        )
        total_weight = sum(
            size
            for size in self.widget_sizes
            if isinstance(size, str) and size.endswith("%")
        )

        available_width = self.width - (self.spacing * (len(self.widgets) - 1))
        weighted_width = (
            (available_width - total_fixed_size) / (total_weight / 100)
            if total_weight > 0
            else 0
        )

        current_x = self.x

        for i, widget in enumerate(self.widgets):
            if i < len(self.widget_sizes):
                size_spec = self.widget_sizes[i]
                if isinstance(size_spec, (int, float)):
                    widget.width = size_spec
                elif isinstance(size_spec, str) and size_spec.endswith("%"):
                    weight = float(size_spec[:-1])
                    widget.width = weighted_width * (weight / 100)
                else:
                    widget.width = (available_width - total_fixed_size) / len(
                        [
                            s
                            for s in self.widget_sizes
                            if not isinstance(s, (int, float))
                        ]
                    )
            else:
                # Default equal distribution
                widget.width = available_width / len(self.widgets)

            widget.x = current_x
            widget.y = self.y
            widget.height = self.height

            current_x += widget.width + self.spacing

            if hasattr(widget, "update_layout"):
                widget.update_layout()

    def _update_vertical_layout(self):
        # Similar implementation for vertical direction
        total_fixed_size = sum(
            size for size in self.widget_sizes if isinstance(size, (int, float))
        )
        total_weight = sum(
            size
            for size in self.widget_sizes
            if isinstance(size, str) and size.endswith("%")
        )

        available_height = self.height - (self.spacing * (len(self.widgets) - 1))
        weighted_height = (
            (available_height - total_fixed_size) / (total_weight / 100)
            if total_weight > 0
            else 0
        )

        current_y = self.y

        for i, widget in enumerate(self.widgets):
            if i < len(self.widget_sizes):
                size_spec = self.widget_sizes[i]
                if isinstance(size_spec, (int, float)):
                    widget.height = size_spec
                elif isinstance(size_spec, str) and size_spec.endswith("%"):
                    weight = float(size_spec[:-1])
                    widget.height = weighted_height * (weight / 100)
                else:
                    widget.height = (available_height - total_fixed_size) / len(
                        [
                            s
                            for s in self.widget_sizes
                            if not isinstance(s, (int, float))
                        ]
                    )
            else:
                widget.height = available_height / len(self.widgets)

            widget.x = self.x
            widget.y = current_y
            widget.width = self.width

            current_y += widget.height + self.spacing

            if hasattr(widget, "update_layout"):
                widget.update_layout()
