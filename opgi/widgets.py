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


class SpinBox(Widget):
    def __init__(self, x, y, width=120, height=30, min_val=0, max_val=100, step=1):
        super().__init__(x, y, width, height)
        self.value = min_val
        self.min = min_val
        self.max = max_val
        self.step = step
        self.active = False
        self.button_width = 25
        self.up_hover = False
        self.down_hover = False

    def draw(self):
        # Main box
        gl.glColor3f(1, 1, 1)
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(self.x, self.y)
        gl.glVertex2f(self.x + self.width, self.y)
        gl.glVertex2f(self.x + self.width, self.y + self.height)
        gl.glVertex2f(self.x, self.y + self.height)
        gl.glEnd()

        # Border
        border_color = (
            (0.2, 0.5, 0.8) if (self.app.focused_widget == self) else (0.7, 0.7, 0.7)
        )
        gl.glColor3f(*border_color)
        gl.glLineWidth(1)
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glVertex2f(self.x, self.y)
        gl.glVertex2f(self.x + self.width, self.y)
        gl.glVertex2f(self.x + self.width, self.y + self.height)
        gl.glVertex2f(self.x, self.y + self.height)
        gl.glEnd()

        # Value text
        value_str = str(self.value)
        text_width = sum(
            glut.glutBitmapWidth(glut.GLUT_BITMAP_HELVETICA_18, ord(c))
            for c in value_str
        )
        text_x = self.x + 10
        text_y = self.y + self.height // 2 + 5

        gl.glColor3f(0, 0, 0)
        gl.glRasterPos2f(text_x, text_y)
        for char in value_str:
            glut.glutBitmapCharacter(glut.GLUT_BITMAP_HELVETICA_18, ord(char))

        # Up/Down buttons with better icons
        self._draw_button(
            self.x + self.width - self.button_width, self.y, "u", hover=self.up_hover
        )
        self._draw_button(
            self.x + self.width - self.button_width,
            self.y + self.height // 2,
            "d",
            hover=self.down_hover,
        )

    def _draw_button(self, x, y, symbol, hover=False):
        # Button background
        btn_color = (0.85, 0.85, 0.85) if hover else (0.9, 0.9, 0.9)
        gl.glColor3f(*btn_color)
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(x, y)
        gl.glVertex2f(x + self.button_width, y)
        gl.glVertex2f(x + self.button_width, y + self.height // 2)
        gl.glVertex2f(x, y + self.height // 2)
        gl.glEnd()

        # Button border
        gl.glColor3f(0.7, 0.7, 0.7)
        gl.glLineWidth(1)
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glVertex2f(x, y)
        gl.glVertex2f(x + self.button_width, y)
        gl.glVertex2f(x + self.button_width, y + self.height // 2)
        gl.glVertex2f(x, y + self.height // 2)
        gl.glEnd()

        # Button icon (centered)
        text_width = glut.glutBitmapWidth(glut.GLUT_BITMAP_HELVETICA_18, ord(symbol))
        text_x = x + (self.button_width - text_width) // 2
        text_y = y + self.height // 4 + 5

        gl.glColor3f(0, 0, 0)
        gl.glRasterPos2f(text_x, text_y)
        glut.glutBitmapCharacter(glut.GLUT_BITMAP_HELVETICA_18, ord(symbol))

    def on_click(self):
        x, y = glfw.get_cursor_pos(self.app.window)

        # Check if up button was clicked
        up_button_x = self.x + self.width - self.button_width
        self.up_hover = (
            up_button_x <= x <= up_button_x + self.button_width
            and self.y <= y <= self.y + self.height // 2
        )

        # Check if down button was clicked
        down_button_x = self.x + self.width - self.button_width
        self.down_hover = (
            down_button_x <= x <= down_button_x + self.button_width
            and self.y + self.height // 2 <= y <= self.y + self.height
        )

        if self.up_hover:
            self.value = min(self.value + self.step, self.max)
        elif self.down_hover:
            self.value = max(self.value - self.step, self.min)


class CheckButton(Widget):
    def __init__(self, x, y, text="Checkbox", checked=False):
        super().__init__(x, y, 20, 20)
        self.text = text
        self.checked = checked
        self.on_change_callback = None

    def draw(self):
        # Checkbox square
        gl.glColor3f(1, 1, 1)
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(self.x, self.y)
        gl.glVertex2f(self.x + self.width, self.y)
        gl.glVertex2f(self.x + self.width, self.y + self.height)
        gl.glVertex2f(self.x, self.y + self.height)
        gl.glEnd()

        # Checkbox border
        border_color = (
            (0.2, 0.5, 0.8) if (self.app.focused_widget == self) else (0.7, 0.7, 0.7)
        )
        gl.glColor3f(*border_color)
        gl.glLineWidth(1)
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glVertex2f(self.x, self.y)
        gl.glVertex2f(self.x + self.width, self.y)
        gl.glVertex2f(self.x + self.width, self.y + self.height)
        gl.glVertex2f(self.x, self.y + self.height)
        gl.glEnd()

        # Checkmark
        if self.checked:
            gl.glColor3f(0.2, 0.5, 0.8)
            gl.glLineWidth(2)
            gl.glBegin(gl.GL_LINES)
            gl.glVertex2f(self.x + 5, self.y + 10)
            gl.glVertex2f(self.x + 10, self.y + 15)
            gl.glVertex2f(self.x + 10, self.y + 15)
            gl.glVertex2f(self.x + 15, self.y + 5)
            gl.glEnd()

        # Label text
        gl.glColor3f(0, 0, 0)
        gl.glRasterPos2f(self.x + self.width + 10, self.y + self.height // 2 + 5)
        for char in self.text:
            glut.glutBitmapCharacter(glut.GLUT_BITMAP_HELVETICA_18, ord(char))

    def on_click(self):
        self.checked = not self.checked
        if self.on_change_callback:
            self.on_change_callback(self.checked)

    def set_on_change(self, callback):
        self.on_change_callback = callback


class RadioButton(Widget):
    def __init__(self, x, y, text="Radio", group=None, selected=False):
        super().__init__(x, y, 20, 20)
        self.text = text
        self.selected = selected
        self.group = group if group is not None else []
        self.group.append(self)
        self.on_select_callback = None

    def draw(self):
        # Radio circle
        gl.glColor3f(1, 1, 1)
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        cx, cy = self.x + self.width // 2, self.y + self.height // 2
        radius = self.width // 2
        for i in range(0, 360, 10):
            angle = math.radians(i)
            gl.glVertex2f(cx + math.cos(angle) * radius, cy + math.sin(angle) * radius)
        gl.glEnd()

        # Radio border
        border_color = (
            (0.2, 0.5, 0.8) if (self.app.focused_widget == self) else (0.7, 0.7, 0.7)
        )
        gl.glColor3f(*border_color)
        gl.glLineWidth(1)
        gl.glBegin(gl.GL_LINE_LOOP)
        for i in range(0, 360, 10):
            angle = math.radians(i)
            gl.glVertex2f(cx + math.cos(angle) * radius, cy + math.sin(angle) * radius)
        gl.glEnd()

        # Selected indicator
        if self.selected:
            gl.glColor3f(0.2, 0.5, 0.8)
            gl.glBegin(gl.GL_TRIANGLE_FAN)
            inner_radius = radius // 2
            for i in range(0, 360, 10):
                angle = math.radians(i)
                gl.glVertex2f(
                    cx + math.cos(angle) * inner_radius,
                    cy + math.sin(angle) * inner_radius,
                )
            gl.glEnd()

        # Label text
        gl.glColor3f(0, 0, 0)
        gl.glRasterPos2f(self.x + self.width + 10, self.y + self.height // 2 + 5)
        for char in self.text:
            glut.glutBitmapCharacter(glut.GLUT_BITMAP_HELVETICA_18, ord(char))

    def on_click(self):
        if not self.selected:
            for rb in self.group:
                rb.selected = False
            self.selected = True
            if self.on_select_callback:
                self.on_select_callback()

    def set_on_select(self, callback):
        self.on_select_callback = callback


class ComboBox(Widget):
    def __init__(self, x, y, width=150, height=30, items=None):
        super().__init__(x, y, width, height)
        self.items = items or ["Option 1", "Option 2", "Option 3"]
        self.selected_index = 0
        self.expanded = False
        self.item_height = 25
        self.dropdown_shadow = True

    def draw(self):
        # Main box
        gl.glColor3f(1, 1, 1)
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(self.x, self.y)
        gl.glVertex2f(self.x + self.width, self.y)
        gl.glVertex2f(self.x + self.width, self.y + self.height)
        gl.glVertex2f(self.x, self.y + self.height)
        gl.glEnd()

        # Border
        border_color = (
            (0.2, 0.5, 0.8)
            if (self.expanded or self.app.focused_widget == self)
            else (0.7, 0.7, 0.7)
        )
        gl.glColor3f(*border_color)
        gl.glLineWidth(1)
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glVertex2f(self.x, self.y)
        gl.glVertex2f(self.x + self.width, self.y)
        gl.glVertex2f(self.x + self.width, self.y + self.height)
        gl.glVertex2f(self.x, self.y + self.height)
        gl.glEnd()

        # Selected item text
        selected_text = self.items[self.selected_index]
        text_x = self.x + 10
        text_y = self.y + self.height // 2 + 5

        gl.glColor3f(0, 0, 0)
        gl.glRasterPos2f(text_x, text_y)
        for char in selected_text:
            glut.glutBitmapCharacter(glut.GLUT_BITMAP_HELVETICA_18, ord(char))

        # Arrow symbol (better looking)
        arrow = "▼" if self.expanded else "▲"
        arrow_x = self.x + self.width - 25
        arrow_y = self.y + self.height // 2 + 5
        gl.glRasterPos2f(arrow_x, arrow_y)
        glut.glutBitmapCharacter(glut.GLUT_BITMAP_HELVETICA_18, ord(arrow))

        # Dropdown items if expanded
        if self.expanded:
            # Draw shadow overlay first
            if self.dropdown_shadow:
                gl.glColor4f(0, 0, 0, 0.2)
                gl.glBegin(gl.GL_QUADS)
                gl.glVertex2f(0, 0)
                gl.glVertex2f(self.app.width, 0)
                gl.glVertex2f(self.app.width, self.app.height)
                gl.glVertex2f(0, self.app.height)
                gl.glEnd()

            for i, item in enumerate(self.items):
                item_y = self.y + self.height + i * self.item_height

                # Highlight selected item
                if i == self.selected_index:
                    gl.glColor3f(0.9, 0.9, 0.9)
                else:
                    gl.glColor3f(1, 1, 1)

                gl.glBegin(gl.GL_QUADS)
                gl.glVertex2f(self.x, item_y)
                gl.glVertex2f(self.x + self.width, item_y)
                gl.glVertex2f(self.x + self.width, item_y + self.item_height)
                gl.glVertex2f(self.x, item_y + self.item_height)
                gl.glEnd()

                # Item border
                gl.glColor3f(0.8, 0.8, 0.8)
                gl.glLineWidth(1)
                gl.glBegin(gl.GL_LINE_LOOP)
                gl.glVertex2f(self.x, item_y)
                gl.glVertex2f(self.x + self.width, item_y)
                gl.glVertex2f(self.x + self.width, item_y + self.item_height)
                gl.glVertex2f(self.x, item_y + self.item_height)
                gl.glEnd()

                # Item text
                gl.glColor3f(0, 0, 0)
                gl.glRasterPos2f(self.x + 10, item_y + self.item_height // 2 + 5)
                for char in item:
                    glut.glutBitmapCharacter(glut.GLUT_BITMAP_HELVETICA_18, ord(char))

    def on_click(self):
        x, y = glfw.get_cursor_pos(self.app.window)

        if not self.expanded:
            # Check if main box was clicked
            if self.contains(x, y):
                self.expanded = True
                # Bring to front by re-adding to widget list
                if self in self.app.widgets:
                    # self.app.widgets.remove(self)
                    self.app.add_widget(self)
        else:
            # Check if an item was clicked
            item_clicked = False
            for i in range(len(self.items)):
                item_y = self.y + self.height + i * self.item_height
                if (
                    self.x <= x <= self.x + self.width
                    and item_y <= y <= item_y + self.item_height
                ):
                    self.selected_index = i
                    item_clicked = True
                    break

            # Collapse if item was clicked or click was outside
            if item_clicked or not (
                self.x <= x <= self.x + self.width
                and self.y
                <= y
                <= self.y + self.height + len(self.items) * self.item_height
            ):
                self.expanded = False
