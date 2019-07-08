import wx

from ..lib import PanelButton, MenuButton



class SciPanel(wx.Panel):

    def __init__(self, parent, idx, config):
        super(wx.Panel, self).__init__(parent)
        
        self.config = config
        self.idx = idx
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)
        self.Hide()
        

    def on_erase_background(self, event):
        """Reduces flicker"""

        pass
    

    def on_paint(self, event):
        # Creating BufferedPaintDC object and drawing the panel.
        dc = wx.BufferedPaintDC(self)
        self.draw(dc)
    

    def draw(self, dc):
        """Drawing the panel."""

        width, height = self.GetClientSize()
        dc.SetBackground(wx.Brush(self.config.get_color('panel')))
        dc.Clear()

        dc.SetPen(wx.Pen(self.config.get_color('border'), width=4))
        dc.DrawLine((0, 0), (0, height))
        dc.DrawLine((0, height), (width, height))
        dc.DrawLine((width, height), (width, 0))
        dc.DrawText(str(self.idx), (width-10, height-20))




class SciPanelButtons(wx.Panel):
    
    """Panel containing panel switching buttons.""" 
    
    def __init__(self, parent, current, manager, config):
        super(wx.Panel, self).__init__(parent)
        
        self.config = config
        self.manager = manager
        
        self.display()
        self.panelButtons[current].isActive = True
        self.Bind(wx.EVT_BUTTON, self.button_pressed)
        
        
    def button_pressed(self, event):
        """Handler for panel switching and menu opening."""

        button = event.GetEventObject()
        if isinstance(button, PanelButton):
            assert button.isActive == True
                
            for butt in self.panelButtons:
                butt.isActive = False
            if not self.manager.menu_open:
                button.isActive = True
                self.manager.switch_to(button.idx)
                return
            self.panelButtons[self.manager.current].isActive = True
        elif isinstance(button, MenuButton):
            self.manager.toggle_menu()


    def display(self):
        """Displaying panel buttons."""

        self.sizer = wx.GridBagSizer(0, 0)
        self.menuButt = MenuButton(self, self.config, name='menu', size=(40, 40))
        self.panelButtons = [
            PanelButton(self, self.config, 'Panel I', idx=0, size=(120, 40)),
            PanelButton(self, self.config, 'Panel II', idx=1, size=(120, 40)),
            PanelButton(self, self.config, 'Panel III', idx=2, size=(120, 40)),
            PanelButton(self, self.config, 'Panel IV', idx=3, size=(120, 40)),
            PanelButton(self, self.config, 'Panel V', idx=4, size=(120, 40)),
            PanelButton(self, self.config, 'Panel VI', idx=5, size=(120, 40))]
        self.sizer.Add(self.menuButt, pos=(0, 0), flag=wx.EXPAND)
        for index, button in enumerate(self.panelButtons):
            self.sizer.Add(button, pos=(0, index+1), flag=wx.EXPAND)
            self.sizer.AddGrowableCol(index+1)
        self.SetSizer(self.sizer)
        self.Layout()