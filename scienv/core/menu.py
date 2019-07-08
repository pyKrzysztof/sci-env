import wx
import os

from ..lib import MenuPanelSwitchButton
from ..lib import ScrolledPanel
from ..lib import SimpleButton
from ..lib import ConfigColorSwitcher
from ..lib import ScaledStaticText
from ..lib import CheckBox

from .widgetdescriptors import WidgetsList


PATH = __file__.replace('core/menu.py', 'widgets/')


class MenuPanel(wx.Panel):
    """Container for menu related panels."""

    def __init__(self, parent, config, manager):
        super().__init__(parent=parent, name='menu')

        self.parent = parent
        self.config = config
        self.manager = manager

        self.Bind(wx.EVT_BUTTON, self.button_pressed)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.erase_background)
        self.Bind(wx.EVT_PAINT, self.on_paint)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = Buttons(self, self.config)
        self.sizer.Add(self.buttons, 0, flag=wx.EXPAND | wx.ALL, border=20)
        self.SetSizer(self.sizer)
        self.Layout()

    def show_side_panel(self, idx):
        """Shows selected menu panel."""

        try:
            self.sizer.Detach(self.current_menu)
            self.current_menu.Destroy()
        except:
            pass
        finally:
            if idx == 0:
                self.current_menu = TitleMenu(self, self.config)
            elif idx == 1:
                self.current_menu = OptionsMenu(self, self.config)
            elif idx == 2:
                self.current_menu = WidgetsMenu(
                    self, self.config, self.manager)

            self.sizer.Add(self.current_menu, proportion=1,
                           flag=wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, border=20)
            self.Layout()

    def button_pressed(self, event):
        """Handles button presses."""

        operation = event.GetEventObject().label
        for switch in self.buttons.GetChildren():
            switch.isActive = False
        event.GetEventObject().isActive = False

        if operation == 'Return':
            wx.CallLater(100, self.manager.toggle_menu)

        elif operation == 'Quit':
            self.manager.save_widgets()
            wx.CallLater(100, self.parent.Destroy)

        elif operation == 'Options':

            if isinstance(self.current_menu, OptionsMenu):
                self.show_side_panel(0)
            else:
                event.GetEventObject().isActive = True
                self.show_side_panel(1)

        elif operation == 'Widgets':
            if isinstance(self.current_menu, WidgetsMenu):
                self.show_side_panel(0)
            else:
                event.GetEventObject().isActive = True
                self.show_side_panel(2)

    def erase_background(self, event):
        """Reduces flicker."""

        pass

    def on_paint(self, event):
        """Handles refreshing."""

        dc = wx.BufferedPaintDC(self)
        self.draw(dc)

    def draw(self, dc):
        """Handles drawing."""

        width, height = self.GetClientSize()
        dc.SetBackground(wx.Brush(self.config.get_color('panel')))
        dc.Clear()

        dc.SetPen(wx.Pen(self.config.get_color('border'), width=4))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(0, 0, width, height)
        dc.SetPen(wx.Pen(self.config.get_color('panel'), width=4))
        dc.DrawLine(3, 0, width - 6, 0)


class Buttons(wx.Panel):
    """Constantly visible menu selection buttons panel."""

    def __init__(self, parent, config, **kwargs):
        super(wx.Panel, self).__init__(parent=parent)

        self.Name = 'menuPanel'
        self.parent = parent
        self.config = config

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.erase_background)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_BUTTON, self.button_pressed)

        self.display()

    def display(self):
        """Displays buttons."""

        self.sizer = wx.GridBagSizer(0, 0)
        butt1 = MenuPanelSwitchButton(
            self, self.config, 'Return', size=(240, 60))
        butt2 = MenuPanelSwitchButton(
            self, self.config, 'Quit', size=(240, 60))
        butt3 = MenuPanelSwitchButton(
            self, self.config, 'Widgets', size=(240, 60))
        butt4 = MenuPanelSwitchButton(
            self, self.config, 'Options', size=(240, 60))

        self.sizer.Add(butt3, pos=(0, 0), flag=wx.EXPAND |
                       wx.TOP | wx.LEFT | wx.RIGHT, border=10)
        self.sizer.Add(butt4, pos=(1, 0), flag=wx.EXPAND |
                       wx.TOP | wx.LEFT | wx.RIGHT, border=10)
        self.sizer.Add(butt1, pos=(2, 0), flag=wx.EXPAND |
                       wx.TOP | wx.LEFT | wx.RIGHT, border=10)
        self.sizer.Add(butt2, pos=(4, 0), flag=wx.EXPAND | wx.ALL, border=10)
        self.sizer.AddGrowableRow(3)

        self.SetSizer(self.sizer)
        self.Layout()

    def button_pressed(self, event):
        """Skips all button presses to menu container."""

        event.Skip()

    def erase_background(self, event):
        """Reduces flicker"""

        pass

    def on_paint(self, event):
        """Handles refreshing."""

        dc = wx.BufferedPaintDC(self)
        self.draw(dc)

    def draw(self, dc):
        """Handles drawing."""

        width, height = self.GetClientSize()
        dc.SetBackground(wx.Brush(self.config.get_color('menu')))
        dc.Clear()

        dc.SetPen(wx.Pen(self.config.get_color('border'), width=4))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(0, 0, width, height)


class TitleMenu(wx.Panel):
    """Default menu panel, displays application name."""

    def __init__(self, parent, config):
        super(wx.Panel, self).__init__(parent)
        self.config = config

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.erase_background)
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def erase_background(self, event):
        """Reduces flicker."""

        pass

    def on_paint(self, event):
        """Handles refreshing."""

        dc = wx.BufferedPaintDC(self)
        self.draw(dc)

    def draw(self, dc):
        """Handles drawing."""

        width, height = self.GetClientSize()

        dc.SetBackground(wx.Brush(self.config.get_color('menu')))
        dc.Clear()

        dc.SetPen(wx.Pen(self.config.get_color('border'), width=4))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(0, 0, width, height)

        dc.SetFont(wx.Font(50, wx.FONTFAMILY_DECORATIVE,
                           wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        dc.SetTextForeground(self.config.get_color('text'))

        textWidth, textHeight = dc.GetTextExtent('SciEnv')
        textX = (width - textWidth) / 2
        textY = (height - textHeight) / 3

        dc.DrawText('SciEnv', (textX, textY))


class OptionsMenu(wx.Panel):

    def __init__(self, parent, config):
        super().__init__(parent=parent)

        self.parent = parent
        self.config = config

        self.SetBackgroundColour(self.config.get_color('menu'))

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.erase_background)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_BUTTON, self.button_pressed)

        self.display()

    def display(self):
        """Displays configuration panel and buttons."""

        sizer = wx.GridBagSizer()
        self.config_panel = OptionsConfigPanel(self, self.config)
        reset_button = SimpleButton(
            parent=self, config=self.config, label='Reset Settings', size=(40, 40))
        save_button = SimpleButton(
            parent=self, config=self.config, label='Save Changes', size=(40, 40))
        cancel_button = SimpleButton(
            parent=self, config=self.config, label='Cancel', size=(40, 40))

        sizer.Add(self.config_panel, pos=(0, 0), span=(8, 10),
                  flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=4)
        sizer.Add(reset_button, pos=(8, 0), span=(1, 3),
                  flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(cancel_button, pos=(8, 6), span=(1, 2),
                  flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(save_button, pos=(8, 8), span=(1, 2), flag=wx.EXPAND |
                  wx.TOP | wx.BOTTOM | wx.RIGHT, border=10)

        for i in range(10):
            sizer.AddGrowableCol(i)
        for i in range(8):
            sizer.AddGrowableRow(i)

        self.SetSizer(sizer)
        self.Layout()

    def button_pressed(self, e):
        button = e.GetEventObject()
        operation = button.label
        if operation == 'Save Changes':
            self.config = self.config_panel.collect_config(self.config)
            self.config.write_config()
            self.GetParent().GetParent().Refresh()
            self.GetParent().GetParent().Layout()
        elif operation == 'Cancel':
            return
        elif operation == 'Reset Settings':
            return

    def erase_background(self, e):
        """Reduces flicker."""

        pass

    def on_paint(self, e):
        """Handles refreshing."""

        dc = wx.BufferedPaintDC(self)
        self.draw(dc)

    def draw(self, dc):
        """Handles drawing."""

        dc.SetBackground(wx.Brush(self.config.get_color('menu')))
        dc.Clear()

        width, height = self.GetClientSize()

        dc.SetPen(wx.Pen(self.config.get_color('border'), width=4))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(0, 0, width, height)


class OptionsConfigPanel(ScrolledPanel):

    def __init__(self, parent, config):
        super().__init__(parent)
        self.config = config

        self.SetBackgroundColour(self.config.get_color('menu'))

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.erase_background)
        self.Bind(wx.EVT_PAINT, self.on_paint)

        self.display()
        self.setup_scrolling(scroll_x=False)

    def display(self):
        """Handles display."""

        sizer = wx.GridBagSizer()

        header = ScaledStaticText(self,
                                  label='Settings',
                                  font=self.config.get_font('large'),
                                  conf=self.config)
        text1 = ScaledStaticText(self,
                                 label='Theme: ',
                                 font=self.config.get_font('medium'),
                                 conf=self.config)
        self.theme_selection = wx.Choice(self,
                                         choices=self.config.get_theme_list(),
                                         size=(120, 40))
        add_themes = SimpleButton(self,
                                  label='Add New Theme',
                                  config=self.config,
                                  size=(120, 40))

        self.save_widgets = CheckBox(
            self, 'Save Widgets//On Exit', self.config.save_widgets_on_exit, self.config)

        text2 = ScaledStaticText(self,
                                 label='Small Font',
                                 font=self.config.get_font('medium'),
                                 conf=self.config)
        text3 = ScaledStaticText(self,
                                 label='Medium Font',
                                 font=self.config.get_font('medium'),
                                 conf=self.config)
        text4 = ScaledStaticText(self,
                                 label='Large Font',
                                 font=self.config.get_font('medium'),
                                 conf=self.config)

        self.font_picker_small = wx.FontPickerCtrl(
            self, font=self.config.get_font('small'), size=(200, 40))
        self.font_picker_medium = wx.FontPickerCtrl(
            self, font=self.config.get_font('medium'), size=(200, 40))
        self.font_picker_large = wx.FontPickerCtrl(
            self, font=self.config.get_font('large'), size=(200, 40))
        self.font_picker_small.SetBackgroundColour(
            self.config.get_color('menu'))
        self.font_picker_medium.SetBackgroundColour(
            self.config.get_color('menu'))
        self.font_picker_large.SetBackgroundColour(
            self.config.get_color('menu'))

        for index, theme in enumerate(self.theme_selection.GetItems()):
            if theme == self.config.get_current_theme():
                self.theme_selection.SetSelection(index)
                break

        sizer.Add(header, pos=(0, 0), span=(1, 2),
                  flag=wx.EXPAND | wx.ALL, border=60)
        sizer.Add(text1, pos=(1, 0), flag=wx.EXPAND | wx.LEFT, border=20)
        sizer.Add(self.theme_selection, pos=(1, 1),
                  flag=wx.EXPAND | wx.RIGHT, border=40)
        sizer.Add(add_themes, pos=(2, 1), flag=wx.EXPAND | wx.RIGHT, border=40)
        sizer.Add((-1, 60), pos=(3, 0), span=(1, 2), flag=wx.EXPAND)
        sizer.Add(text2, pos=(4, 0), flag=wx.EXPAND | wx.LEFT, border=20)
        sizer.Add(text3, pos=(5, 0), flag=wx.EXPAND | wx.LEFT, border=20)
        sizer.Add(text4, pos=(6, 0), flag=wx.EXPAND | wx.LEFT, border=20)
        sizer.Add(self.font_picker_small, pos=(4, 1),
                  flag=wx.EXPAND | wx.RIGHT, border=40)
        sizer.Add(self.font_picker_medium, pos=(5, 1),
                  flag=wx.EXPAND | wx.RIGHT, border=40)
        sizer.Add(self.font_picker_large, pos=(6, 1),
                  flag=wx.EXPAND | wx.RIGHT, border=40)
        sizer.Add((-1, 60), pos=(7, 0), span=(1, 2), flag=wx.EXPAND)
        sizer.Add(self.save_widgets, pos=(8, 0), flag=wx.EXPAND)

        for i in range(2):
            sizer.AddGrowableCol(i)

        self.SetSizer(sizer)
        self.Layout()

    def collect_config(self, config):
        """Collects all the configuration across the panels' children."""

        config._config.set('General', 'Theme', self.theme_selection.GetString(
            self.theme_selection.GetSelection()))
        do_save_widgets = 'yes' if self.save_widgets.value else 'no'
        config._config.set('General', 'savewidgetsonexit', do_save_widgets)
        small_font = self.font_picker_small.GetSelectedFont()
        medium_font = self.font_picker_medium.GetSelectedFont()
        large_font = self.font_picker_large.GetSelectedFont()
        config.set_font('Small Font',
                        small_font.GetPointSize(),
                        small_font.GetFamily(),
                        small_font.GetStyle(),
                        small_font.GetWeight())
        config.set_font('Medium Font',
                        medium_font.GetPointSize(),
                        medium_font.GetFamily(),
                        medium_font.GetStyle(),
                        medium_font.GetWeight())
        config.set_font('Large Font',
                        large_font.GetPointSize(),
                        large_font.GetFamily(),
                        large_font.GetStyle(),
                        large_font.GetWeight())
        return config

    def erase_background(self, e):
        """Remove flicker."""

        pass

    def on_paint(self, e):
        """Handles refreshing."""

        dc = wx.BufferedPaintDC(self)
        self.draw(dc)

    def draw(self, dc):
        """Handles drawing."""

        dc.SetBackground(wx.Brush(self.config.get_color('menu')))
        dc.Clear()


class WidgetsMenu(wx.Panel):

    def __init__(self, parent, config, manager):
        super().__init__(parent=parent)

        self.parent = parent
        self.config = config
        self.manager = manager

        widgets = os.listdir(PATH)
        if not widgets:
            self.widget_panel = NoWidgetsPanel(self, self.config)
        else:
            self.widget_panel = EmptyPanel(self, self.config)

        self.SetBackgroundColour(self.config.get_color('menu'))

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.erase_background)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_BUTTON, self.button_pressed)

        self.display()

    def display(self):

        self.sizer = wx.GridBagSizer()

        self.widget_list = WidgetsList(self, self.config, self.manager)
        self.button = SimpleButton(
            self, label='Download Widgets', config=self.config, size=(200, 40))

        self.sizer.Add(self.widget_list, pos=(0, 0), span=(7, 2),
                  flag=wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT, border=10)
        self.sizer.Add(self.widget_panel, pos=(0, 2), span=(8, 8), 
                  flag=wx.EXPAND | wx.ALL, border=10)
        self.sizer.Add(self.button, pos=(7, 0), span=(1, 2),
                  flag=wx.EXPAND | wx.BOTTOM | wx.LEFT, border=10)

        for i in range(7):
            self.sizer.AddGrowableRow(i)
        for i in range(2, 10):
            self.sizer.AddGrowableCol(i)

        self.SetSizer(self.sizer)
        self.Layout()

    def button_pressed(self, e):
        pass

    def erase_background(self, e):
        """Reduces flicker."""

        pass

    def on_paint(self, e):
        """Handles refreshing."""

        dc = wx.BufferedPaintDC(self)
        self.draw(dc)

    def draw(self, dc):
        """Handles drawing."""

        dc.SetBackground(wx.Brush(self.config.get_color('menu')))
        dc.Clear()

        width, height = self.GetClientSize()

        dc.SetPen(wx.Pen(self.config.get_color('border'), width=4))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(0, 0, width, height)


class NoWidgetsPanel(wx.Panel):

    def __init__(self, parent, config):
        super().__init__(parent)

        self.config = config
        text1 = ScaledStaticText(self, 
                                 label='No widgets installed.', 
                                 font=self.config.get_font('large'),
                                 conf=self.config)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text1, 1, flag=wx.EXPAND|wx.ALL, border=20)
        self.SetSizer(sizer)
        self.Layout()

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.erase_background)
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def erase_background(self, e):
        pass

    def on_paint(self, e):
        dc = wx.BufferedPaintDC(self)
        self.draw(dc)

    def draw(self, dc):
        dc.SetBackground(wx.Brush(self.config.get_color('menu')))
        dc.Clear()


class EmptyPanel(wx.Panel):

    def __init__(self, parent, config):
        super().__init__(parent)

        self.SetBackgroundColour(config.get_color('menu'))