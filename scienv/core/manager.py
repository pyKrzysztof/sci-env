import wx
import pickle

from .scipanel import SciPanel
from .scipanel import SciPanelButtons
from .menu import MenuPanel


class WindowManager:
    """Manages panels (excluding widgets) inside the frame."""

    def __init__(self, frame, config):
        self.frame = frame
        self.config = config
        self.widgets = []
        self.widget_objects = []

        

    def init_windows(self):
        """Initializes the SciPanels, buttons panel, and displays them."""

        self.panels = [SciPanel(self.frame, idx, self.config)
                       for idx in range(0, 6)]
        self.buttons = SciPanelButtons(self.frame, 0, self, self.config)
        self.frame.sizer.Add(self.buttons, 0, flag=wx.EXPAND)
        self.menu_open = False
        self.current = None
        self.switch_to(0)
        self.load_widgets()

    def switch_to(self, idx):
        """Switched panel from current to idx."""

        # Basic assertion, must never happen.
        assert -1 < idx < 6
        assert self.current != idx
        assert self.menu_open != True

        # Execute this block if there was no previous panel.
        if self.current is None:
            self.frame.sizer.Add(self.panels[idx], 1, wx.EXPAND)
            self.panels[idx].Show()
            self.current = idx
            self.frame.Layout()
            return

        # Execute this block if there was previous panel, to avoid exceptions from frame.sizer
        self.frame.sizer.Replace(
            self.panels[self.current], self.panels[idx])
        self.panels[self.current].Hide()
        self.panels[idx].Show()
        self.current = idx
        self.frame.Layout()

    def open_menu(self):
        """Opens menu."""

        assert self.menu_open == False

        # Detach and hide current panel and display the menu.
        self.frame.sizer.Detach(self.panels[self.current])
        self.panels[self.current].Hide()
        menuPanel = MenuPanel(self.frame, config=self.config, manager=self)
        self.frame.sizer.Add(menuPanel, 1, flag=wx.EXPAND)
        menuPanel.show_side_panel(0)
        self.menu_open = True
        self.frame.Layout()

    def close_menu(self, redirect):
        """Closes menu."""

        for child in self.frame.GetChildren():
            if child.Name != 'menu':
                continue
            self.frame.sizer.Detach(child)
            child.Destroy()

        self.menu_open = False
        self.current = None
        self.switch_to(redirect)

    def toggle_menu(self):
        """Handles opening and closing menu."""

        if not self.menu_open:
            self.open_menu()
        else:
            self.close_menu(redirect=self.current)

    def add_widget(self, data, panel_idx):
        exec(f'from ..widgets.{data["file"]}.main import Widget as {data["file"]}')
        widget = eval(data['file'])(self.panels[panel_idx],
                                    self.config)

        self.widgets.append([data, panel_idx])
        self.widget_objects.append(widget)

        widget.SetPosition(data['pos'])
        widget.Fit()
        if data['size'] != 'default':
            widget.SetSize(data['size'])

    def load_widgets(self):
        if not self.config.save_widgets_on_exit:
            return

        try:
            with open('cache.txt', 'rb') as cache:
                data = pickle.load(cache)
                for widget_data in data:
                    self.add_widget(widget_data[0], 
                                    widget_data[1])
        except:
            pass

    def save_widgets(self):
        widgets = []
        for index, widget in enumerate(self.widget_objects):
            if widget:
                widgets.append(self.widgets[index])
                widgets[-1][0]['pos'] = widget.GetPosition()
                widgets[-1][0]['size'] = widget.GetSize()

        with open('cache.txt', 'wb') as cache:
            pickle.dump(widgets, cache)