"""Assorted UI elements."""
import urwid


class PrettyButton(urwid.WidgetWrap):
    """Prettified urwid Button."""
    def __init__(self, label, on_press=None, user_data=None):
        self.label = ""
        self.text = urwid.Text("")
        self.set_label(label)
        self.widget = urwid.AttrMap(self.text, '', 'highlight')

        # use a hidden button for evt handling
        self._hidden_btn = urwid.Button(f"hidden {self.label}",
                                        on_press, user_data)

        super().__init__(self.widget)

    def selectable(self):
        """Make button selectable."""
        return True

    def keypress(self, *args, **kw):
        """Handle keypresses."""
        return self._hidden_btn.keypress(*args, **kw)

    def mouse_event(self, *args, **kw):
        """Handle mouse events."""
        return self._hidden_btn.mouse_event(*args, **kw)

    def get_label(self):
        """Return current input label."""
        return self.label

    def set_label(self, label):
        """Return current input label."""
        self.label = label
        self.text.set_text(f"[ {label} ]")
