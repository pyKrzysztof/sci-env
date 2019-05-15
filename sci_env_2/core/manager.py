import wx

from .scipanel import SciPanel
from .scipanel import SciPanelButtons
from .menu import MenuPanel


class WindowManager:
    """Manages panels (excluding widgets) inside the frame."""

    def __init__(self, frame, config):
        self.frame = frame
        self.config = config

    def init_windows(self):
        """Initializes the SciPanels, buttons panel, and displays them."""

        self.panels = [SciPanel(self.frame, idx, self.config)
                       for idx in range(0, 6)]
        self.buttons = SciPanelButtons(self.frame, 0, self, self.config)
        self.frame.sizer.Add(self.buttons, 0, flag=wx.EXPAND)
        self.menu_open = False
        self.current = None
        self.switch_to(0)

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
