import wx
import os
import json

from ..lib import ScrolledPanel
from ..lib import SimpleButton


PATH = __file__ .replace('core/widgetdescriptors.py', 'widgets/')


class WidgetCard(wx.Control):

    def __init__(self, parent, name, author, version, filename, icon, config):
        super().__init__(parent, size=(150, 80))

        self.config = config

        self.filename = filename
        self.icon = icon
        self.parent = parent
        self.name = name
        self.version = version
        self.author = author

        self.name_font = config.get_font('small')
        self.name_font.SetPointSize(10)
        self.version_font = config.get_font('small')
        self.version_font.SetPointSize(9)
        self.author_font = config.get_font('small')
        self.author_font.SetPointSize(9)

        self.Bind(wx.EVT_LEFT_DOWN, self.mouse_down)
        self.Bind(wx.EVT_LEFT_UP, self.mouse_up)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.erase_background)
        self.Bind(wx.EVT_PAINT, self.on_paint)

        self.active = False

    def mouse_down(self, event):
        self.Refresh()

    def mouse_up(self, event):
        self.selected = True
        self.Refresh()
        self.send_event()

    def send_event(self):
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, self.GetId())
        event.SetInt(0)
        event.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(event)

    def erase_background(self, event):
        pass

    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.draw(dc)

    def draw(self, dc):
        dc.SetBackground(wx.Brush(self.config.get_color('button')))
        dc.SetTextForeground(self.config.get_color('text'))
        dc.Clear()

        width, height = self.GetClientSize()
        if self.active:
            dc.SetPen(wx.Pen(self.config.get_color('select'), width=4))
        else:
            dc.SetPen(wx.Pen(self.config.get_color('border'), width=4))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(0, 0, width, height)

        padding = (self.GetClientSize()[1] - 48) / 2
        dc.DrawBitmap(self.icon, padding, padding)

        dc.SetFont(self.name_font)
        name_width, name_height = dc.GetTextExtent(self.name)
        name_x, name_y = 2 * padding + 48, padding
        dc.DrawText(self.name, name_x, name_y)

        dc.SetFont(self.version_font)
        version_width, version_height = dc.GetTextExtent(self.version)
        version_x, version_y = width - version_width - padding, padding
        dc.DrawText(self.version, version_x, version_y)

        dc.SetFont(self.author_font)
        author_width, author_height = dc.GetTextExtent('by ' + self.author)
        author_x, author_y = name_x + padding, name_y + name_height + padding
        dc.DrawText('by ' + self.author, author_x, author_y)


class WidgetPanel(wx.Panel):

    def __init__(self, parent, widget, config, manager):
        super().__init__(parent)

        self.config = config
        self.manager = manager

        data = get_widget_data(widget)

        self.file = widget
        self.name = data['name']
        self.icon = data['icon']

        sizer = wx.BoxSizer(wx.VERTICAL)

        butt1 = SimpleButton(self, label='Add To Panel',
                             config=self.config, size=(200, 60))
        butt2 = SimpleButton(self, label='Show Description',
                             config=self.config, size=(200, 60))
        butt3 = SimpleButton(self, label='View Source',
                             config=self.config, size=(200, 60))
        butt4 = SimpleButton(self, label='Remove Widget',
                             config=self.config, size=(200, 60))

        sizer.Add((-1, 120))
        sizer.Add(butt1, 0, flag=wx.EXPAND | wx.TOP |
                  wx.RIGHT | wx.LEFT, border=20)
        sizer.Add(butt2, 0, flag=wx.EXPAND | wx.TOP |
                  wx.RIGHT | wx.LEFT, border=20)
        sizer.Add(butt3, 0, flag=wx.EXPAND | wx.TOP |
                  wx.RIGHT | wx.LEFT, border=20)
        sizer.Add(butt4, 0, flag=wx.EXPAND | wx.TOP |
                  wx.RIGHT | wx.LEFT, border=20)

        self.SetSizer(sizer)

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.erase_background)
        self.Bind(wx.EVT_BUTTON, self.button_pressed)

    def button_pressed(self, e):
        button = e.GetEventObject()
        action = button.label
        if action == 'Add To Panel':
            data = {'file': self.file, 'pos': (20, 20), 'size': 'default'}
            self.manager.add_widget(data, self.manager.current)
        elif action == 'Show Description':
            pass
        elif action == 'View Source':
        	pass
        elif action == 'Remove Widget':
        	pass

    def erase_background(self, e):
        pass

    def on_paint(self, e):
        dc = wx.BufferedPaintDC(self)
        self.draw(dc)

    def draw(self, dc):
        dc.SetBackground(wx.Brush(self.config.get_color('panel')))
        dc.SetTextForeground(self.config.get_color('text'))
        dc.Clear()

        width, height = self.GetClientSize()
        dc.SetPen(wx.Pen(self.config.get_color('border'), width=4))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(0, 0, width, height)

     
        padding = (120-48)/6
        dc.DrawBitmap(self.icon, padding, padding)

        dc.SetFont(self.config.get_font('large'))
        name_width, name_height = dc.GetTextExtent(self.name)
        name_x, name_y = (width+48+padding*2 - name_width)/2, padding + (48-name_height)/2
        dc.DrawText(self.name, name_x, name_y)



class ScrolledList(ScrolledPanel):

    def __init__(self, parent, config):
        super().__init__(parent, size=(200, 40))
        self.config = config
        self.cards = []

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.erase_background)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_BUTTON, self.button_pressed)

    def load_widget_cards(self):
        for card in self.cards:
            try:
                self.sizer.Detach(card)
            finally:
                self.sizer.Add(card, 0, flag=wx.EXPAND | wx.ALL, border=2)

    def button_pressed(self, e):
        for card in self.cards:
            card.active = False
            card.Refresh()
        e.GetEventObject().active = True
        e.GetEventObject().Refresh()
        e.Skip()

    def erase_background(self, e):
        pass

    def on_paint(self, e):
        dc = wx.BufferedPaintDC(self)
        self.draw(dc)

    def draw(self, dc):
        dc.SetBackground(wx.Brush(self.config.get_color('panel')))
        dc.Clear()


class WidgetsList(wx.Panel):

    def __init__(self, parent, config, manager):
        super().__init__(parent, size=(300, 40))

        self.parent = parent
        self.config = config
        self.manager = manager
        self.widget_files = os.listdir(PATH)
        self.scrolled_list = ScrolledList(self, self.config)
        for widget in self.widget_files:
            widget_card = create_widget_card(
                self.scrolled_list, self.config, widget)
            self.scrolled_list.cards.append(widget_card)
        self.scrolled_list.load_widget_cards()

        self.display()

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.erase_background)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_BUTTON, self.widget_selected)

    def display(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.scrolled_list, 1, flag=wx.EXPAND | wx.ALL, border=6)
        self.SetSizer(sizer)
        self.Layout()

    def widget_selected(self, e):
        button = e.GetEventObject()
        create_widget_panel(self.parent, self.config,
                            self.manager, button.filename)
        pass

    def erase_background(self, e):
        """Removes flicker."""

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


def get_widget_data(widget):
    path = PATH + widget + '/'
    with open(path + 'info.json', 'r') as info_file:
        data = json.load(info_file)
    with open(path + 'description.htm') as description_file:
        code = ''
        for line in description_file:
            code += line
        data['html'] = code
    data['icon'] = wx.Bitmap(path + 'icon.png')
    return data


def create_widget_card(parent, config, file):
    path = PATH + file + '/'

    with open(path + 'info.json') as info_file:
        data = json.load(info_file)
        name = data['name']
        version = data['version']
        author = data['author']
    icon = wx.Bitmap(path + 'icon.png')


    return WidgetCard(parent, name=name, author=author, icon=icon,
                      filename=file, version=version, config=config)


def create_widget_panel(parent, config, manager, filename):
    try:
        parent.sizer.Detach(parent.widget_panel)
        parent.widget_panel.Destroy()
    finally:
        parent.widget_panel = WidgetPanel(parent, filename, config, manager)
        parent.sizer.Add(parent.widget_panel, pos=(0, 2), span=(8, 8),
                         flag=wx.EXPAND | wx.ALL, border=10)

        parent.Layout()
