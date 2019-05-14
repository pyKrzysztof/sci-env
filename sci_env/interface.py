import os
import json
import wx
import wx.html as html
from lib.buttons import PanelButton, SimpleButton, MenuButton, MenuPanelSwitchButton, ConfigColorSwitcher, CheckBox
from lib.scrolled import ScrolledPanel
from lib.scaled import ScaledStaticText
from managers import WidgetManager, ConfigManager




def StartInterface(debug=False):
    app = SciEnv()
    app.OnStart()
    if debug:
        import wx.lib.inspection
        wx.lib.inspection.InspectionTool().Show()    
    app.MainLoop()



#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


class SciEnv(wx.App):

    """SciEnv App Class"""
    
    def OnStart(self):
        frame = SciFrame()
        frame.Show()
###############################################################################################
###############################################################################################


###############################################################################################
###############################################################################################
class SciFrame(wx.Frame):
    
    def __init__(self, current=0, refresh=False, widgets=None):
        super(wx.Frame, self).__init__(parent=None, title='SciEnv', size=(1050, 650))
        self.SetMinSize((1050, 650))
        
        self.conf = ConfigManager()
        self.mainPanel = MainPanel(self, self.conf)
        self.panelManager = PanelManager(self, current)
        self.buttons = SciPanelButtons(self, current, self.panelManager, self.conf)
        self.widgetManager = WidgetManager(self, self.conf)
        
        self.OnInit()
    
    def OnInit(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.buttons, 0, flag=wx.EXPAND)
        sizer.Add(self.mainPanel, 1, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()
###############################################################################################
###############################################################################################


###############################################################################################
###############################################################################################
class PanelManager():
    

    def __init__(self, frame, current):
        self.frame = frame
        self._CreatePanels()
        self._menuOpen = False
        self.current = None
        self.SwitchTo(current)
    

    def _CreatePanels(self):
        # Creating the list of panels
        self.panels = [SciPanel(self.frame.mainPanel, idx, self.frame.conf) for idx in range(0, 6)]
        print('!DEBUG: panels created')
    

    def SwitchTo(self, idx):  
        # Basic assertion, must never happen.
        assert -1 < idx < 6
        assert self.current != idx
        assert self._menuOpen != True 
        
        # Execute this block if there was no previous panel.
        if self.current is None:
            print('!DEBUG: starting at', idx)
            self.frame.mainPanel.sizer.Add(self.panels[idx], 1, wx.EXPAND)
            self.panels[idx].Show()
            self.current = idx
            self.frame.mainPanel.Layout()
            return
        
        # Execute this block if there was previous panel, to avoid exceptions from mainPanel.sizer
        print('!DEBUG: switching from', self.current, 'to', idx)
        self.frame.mainPanel.sizer.Replace(self.panels[self.current], self.panels[idx])
        self.panels[self.current].Hide()
        self.panels[idx].Show()
        self.current = idx
        self.frame.mainPanel.Layout()
    

    def ToggleMenu(self):
        # Open menu if it is closed, and close it if it's open.
        if not self._menuOpen:
            self.OpenMenu()
        else:
            self.CloseMenu(redirect=self.current)
            

    def OpenMenu(self):
        # Make sure that menu is closed.
        assert self._menuOpen == False
        
        # Detach and hide current panel and display the menu.
        self.frame.mainPanel.sizer.Detach(self.panels[self.current])
        self.panels[self.current].Hide()
        menuPanel = MenuPanel(self.frame, self.frame.conf)
        self.frame.mainPanel.sizer.Add(menuPanel, 0, flag=wx.ALL|wx.EXPAND, border=20)
        menuPanel.ShowSidePanel(0)
        
        self._menuOpen = True
        
        self.frame.mainPanel.Layout()
        
        print('!DEBUG: menu opened')
    
    
    def CloseMenu(self, redirect):
        # iterate through the children of mainPanel, if it is a 
        for child in self.frame.mainPanel.GetChildren():
            if child.Name != 'menuPanel':
                continue
            self.frame.mainPanel.sizer.Detach(child)
            child.Destroy()
        
        self._menuOpen = False
        self.current = None
        self.SwitchTo(redirect)
        print('!DEBUG: menu closed')
###############################################################################################
###############################################################################################


###############################################################################################
###############################################################################################
class SciPanel(wx.Panel):
    
    def __init__(self, parent, idx, conf):
        super(wx.Panel, self).__init__(parent)
        
        self.conf = conf
        self.idx = idx
        
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
        
        self.sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        self.Hide()
        
    def _OnEraseBackground(self, event):
        # Reduce flicker.
        pass
    
    def _OnPaint(self, event):
        # Creating BufferedPaintDC object and drawing the panel.
        dc = wx.BufferedPaintDC(self)
        self._Draw(dc)
        
    def _Draw(self, dc):
        # Getting width and height of the panel.
        width, height = self.GetClientSize()
        
        # Setting the background color and clearing the panel of previous draws.
        dc.SetBackground(wx.Brush(self.conf.Get('panelColor')))
        dc.Clear()
        
        # Drawing the border.
        dc.SetPen(wx.Pen(self.conf.Get('borderColor'), width=4))
        dc.DrawLine((0, 0), (0, height))
        dc.DrawLine((0, height), (width, height))
        dc.DrawLine((width, height), (width, 0))
        
        # Drawing the panel index for testing purpose.  
        dc.SetTextForeground('white')
        dc.DrawText(str(self.idx), (width-10, height-20))
###############################################################################################
###############################################################################################


###############################################################################################
###############################################################################################
class MainPanel(wx.Panel):
    
    def __init__(self, parent, conf):
        super(wx.Panel, self).__init__(parent)
        
        self.conf = conf
        
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
        
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        
        
    def _OnEraseBackground(self, event):
        # reduce flicker
        pass
    
    def _OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self._Draw(dc)
        
    def _Draw(self, dc):
        width, height = self.GetClientSize()
        
        dc.SetBackground(wx.Brush(self.conf.Get('panelColor')))
        dc.Clear()
        
        dc.SetPen(wx.Pen(self.conf.Get('borderColor'), width=4))
        dc.DrawLine((0, 0), (0, height))
        dc.DrawLine((0, height), (width, height))
        dc.DrawLine((width, height), (width, 0))
###############################################################################################
###############################################################################################


###############################################################################################
###############################################################################################
class SciPanelButtons(wx.Panel):
    
    
    def __init__(self, parent, current, manager, conf):
        super(wx.Panel, self).__init__(parent)
        
        self.conf = conf
        self.manager = manager
        
        self.OnDisplay()
        self.panelButtons[current].isActive = True
        self.Bind(wx.EVT_BUTTON, self._OnButtonPressed)
        
        
    def _OnButtonPressed(self, event):
        button = event.GetEventObject()
        
        if isinstance(button, PanelButton):
            assert button.isActive == True
                
            for butt in self.panelButtons:
                butt.isActive = False
            if not self.manager._menuOpen:
                button.isActive = True
                self.manager.SwitchTo(button.idx)
                return
            self.panelButtons[self.manager.current].isActive = True
            
        elif isinstance(button, MenuButton):
            self.manager.ToggleMenu()
    
    
    def OnDisplay(self):
        self.sizer = wx.GridBagSizer(0, 0)
        
        self.menuButt = MenuButton(self, self.conf, name='menu', size=(40, 40))
        self.panelButtons = [
            PanelButton(self, self.conf, 'Panel I', idx=0, size=(120, 40)),
            PanelButton(self, self.conf, 'Panel II', idx=1, size=(120, 40)),
            PanelButton(self, self.conf, 'Panel III', idx=2, size=(120, 40)),
            PanelButton(self, self.conf, 'Panel IV', idx=3, size=(120, 40)),
            PanelButton(self, self.conf, 'Panel V', idx=4, size=(120, 40)),
            PanelButton(self, self.conf, 'Panel VI', idx=5, size=(120, 40))]
        
        self.sizer.Add(self.menuButt, pos=(0, 0), flag=wx.EXPAND)
        for index, button in enumerate(self.panelButtons):
            self.sizer.Add(button, pos=(0, index+1), flag=wx.EXPAND)
            self.sizer.AddGrowableCol(index+1)
        
        self.SetSizer(self.sizer)
        self.Layout()




#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


class MenuPanel(wx.Panel):
    
    def __init__(self, frame, conf, **kwargs):
        super(wx.Panel, self).__init__(parent=frame.mainPanel)
        
        self.Name = 'menuPanel'
        self.frame = frame
        self.conf = conf
        
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_BUTTON, self.OnButtonPressed)
        
        self.Display()
        
    
    def Display(self):
        self.sizer = wx.GridBagSizer(0, 0)
        
        butt1 = MenuPanelSwitchButton(self, self.conf, 'Return', size=(240, 60))
        butt2 = MenuPanelSwitchButton(self, self.conf, 'Quit', size=(240, 60))        
        self.switchable = [MenuPanelSwitchButton(self, self.conf, 'Widgets', size=(240, 60)),
                           MenuPanelSwitchButton(self, self.conf, 'Options', size=(240, 60))]
        
        
        self.sizer.Add(self.switchable[0], pos=(0, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)
        self.sizer.Add(self.switchable[1], pos=(1, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)
        self.sizer.Add(butt1, pos=(2, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)
        self.sizer.Add(butt2, pos=(4, 0), flag=wx.EXPAND|wx.ALL, border=10)
        self.sizer.AddGrowableRow(3)
        
        self.SetSizer(self.sizer)
        self.Layout()

    
    def ShowSidePanel(self, idx):
        try:
            self.frame.mainPanel.sizer.Detach(self.sidePanel)
            self.sidePanel.Destroy()
        except:
            pass
        finally:
            if idx == 0:
                self.sidePanel = TitleMenuPanel(self.frame, self.conf)
            elif idx == 1:
                self.sidePanel = OptionsMenuPanel(self.frame, self.conf)
            elif idx == 2:
                self.sidePanel = WidgetsMenuPanel(self.frame, self.conf)
            
            self.frame.mainPanel.sizer.Add(self.sidePanel, proportion=1, flag=wx.EXPAND|wx.TOP|wx.BOTTOM|wx.RIGHT, border=20)
            self.frame.mainPanel.Layout()
    
    def OnButtonPressed(self, event):
        operation = event.GetEventObject().label
        for switch in self.switchable:
            switch.isActive = False           
            
        if operation == 'Return':
            wx.CallLater(100, self.frame.panelManager.ToggleMenu)
            
        elif operation == 'Quit':          
            # add a dialog box later.
            self.frame.widgetManager.SaveWidgets()
            wx.CallLater(100, self.frame.Destroy)
            
        elif operation == 'Options':
                    
            if isinstance(self.sidePanel, OptionsMenuPanel):
                self.ShowSidePanel(0)
            else:
                event.GetEventObject().isActive = True
                self.ShowSidePanel(1)
            
        elif operation == 'Widgets':
            if isinstance(self.sidePanel, WidgetsMenuPanel):
                self.ShowSidePanel(0)
            else:
                event.GetEventObject().isActive = True
                self.ShowSidePanel(2)
        
    def _OnEraseBackground(self, event):
        pass
    
    def _OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self._Draw(dc)
    
    def _Draw(self, dc):
        width, height = self.GetClientSize()
        dc.SetBackground(wx.Brush(self.conf.Get('menuColor')))
        dc.Clear()
        
        dc.SetPen(wx.Pen(self.conf.Get('borderColor'), width=4))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(0, 0, width, height)
###############################################################################################
###############################################################################################


###############################################################################################
###############################################################################################
class OptionsButtonsPanel(wx.Panel):
    
    def __init__(self, parent, conf):
        super(wx.Panel, self).__init__(parent)
        
        self.Name = 'menuPanel'
        self.conf = conf
        
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_BUTTON, self.OnButtonPressed)
        
        self.Display()      
        
    def Display(self):
        butt1 = SimpleButton(self, self.conf, "Factory Defaults", size=(240, 40))
        butt2 = SimpleButton(self, self.conf, "Apply", size=(80, 40))
        butt3 = SimpleButton(self, self.conf, "Cancel", size=(80, 40))
        
        sizer = wx.GridBagSizer(0, 0)
        sizer.Add(butt1, pos=(0, 0), flag=wx.EXPAND)
        sizer.Add(butt2, pos=(0, 2), flag=wx.EXPAND)
        sizer.Add(butt3, pos=(0, 3), flag=wx.EXPAND|wx.LEFT, border=7)
        sizer.AddGrowableCol(1)
        self.SetSizer(sizer)
        self.Layout()
        
    def OnButtonPressed(self, event):
        if event.GetEventObject().label == "Factory Defaults":
            #!TODO: show a dialog window asking whether you are sure to reset.
            return
        event.Skip()
        
    def _OnEraseBackground(self, event):
        pass
    
    def _OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)
        
    def Draw(self, dc):
        dc.SetBackground(wx.Brush(self.conf.Get('menuColor')))
        dc.Clear()
###############################################################################################
###############################################################################################


###############################################################################################
###############################################################################################
class ConfigPanel(ScrolledPanel):
    

    def __init__(self, parent, conf):
        super().__init__(parent)
        
        self.Name = 'menuPanel'
        self.conf = conf
        
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
        self.Bind(wx.EVT_BUTTON, self.OnButtonPressed)

        self.Display()
        self.SetupScrolling(scroll_x=False, scrollToTop=False, rate_y=10)



    def Display(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.frameColorsPanel = FrameColors(self, self.conf)
        self.widgetSettingsPanel = WidgetSettings(self, self.conf)
        self.fontsPanel = FontSettingsPanel(self, self.conf)

        sizer.Add(self.frameColorsPanel, 1, flag=wx.EXPAND)
        sizer.Add(-1, 50)
        sizer.Add(self.widgetSettingsPanel, 1, flag=wx.EXPAND)
        sizer.Add(-1, 50)
        sizer.Add(self.fontsPanel, 1, flag=wx.EXPAND)

        self.SetSizer(sizer)
        self.Layout()

    
    def CollectConfig(self):
        config = {}
        config = self.frameColorsPanel.CollectColors(config)
        config = self.widgetSettingsPanel.CollectConfig(config)
        config = self.fontsPanel.CollectFonts(config)
        return config
    

    def RefreshColors(self):
        for child in self.frameColorsPanel.GetChildren():
            if child.label == 'Frame Colors':
                continue
            child.color = self.conf.Get(child.label.lower() + 'Color')
            
    
    def OnButtonPressed(self, event):
        button = event.GetEventObject()
        color = button.color
        colorData = wx.ColourData()
        colorData.SetColour(color)
        
        dialog = wx.ColourDialog(self, data=colorData)
        if dialog.ShowModal() == wx.ID_OK:
            colorData = dialog.GetColourData()
            color = colorData.GetColour()
            color = '#{0:02x}{1:02x}{2:02x}'.format(color[0], color[1], color[2])     
        button.color = color
        button.Refresh()
        
    def _OnEraseBackground(self, event):
        pass
    
    def _OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)
        
    def Draw(self, dc):
        dc.SetBackground(wx.Brush(self.conf.Get('menuColor')))
        dc.Clear()
###############################################################################################
###############################################################################################


###############################################################################################
###############################################################################################
class FrameColors(wx.Panel):

    def __init__(self, parent, conf):
        super().__init__(parent)
        self.conf = conf
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
        self.Display()

    def Display(self):
        sizer = wx.GridBagSizer(5, 5)
        
        headerFont = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD)
        colorsHeader = ScaledStaticText(self, 'Frame Colors', headerFont, conf=self.conf)
        
        size = (140, 30)
        textColor = ConfigColorSwitcher(self, 'Text', self.conf.Get('textColor'), self.conf, size)
        panelColor = ConfigColorSwitcher(self, 'Panel', self.conf.Get('panelColor'), self.conf, size)
        menuColor = ConfigColorSwitcher(self, 'Menu', self.conf.Get('menuColor'), self.conf, size)
        borderColor = ConfigColorSwitcher(self, 'Border', self.conf.Get('borderColor'), self.conf, size)
        inactiveColor = ConfigColorSwitcher(self, 'Inactive', self.conf.Get('inactiveColor'), self.conf, size)
        buttonColor = ConfigColorSwitcher(self, 'Button', self.conf.Get('buttonColor'), self.conf, size)
        selectColor = ConfigColorSwitcher(self, 'Select', self.conf.Get('selectColor'), self.conf, size)
        highlightColor = ConfigColorSwitcher(self, 'Highlight', self.conf.Get('highlightColor'), self.conf, size)    
        
        sizer.Add(colorsHeader, pos=(0, 0), span=(3, 5), flag=wx.EXPAND, border=80)
        
        sizer.Add(textColor, pos=(4, 1), flag=wx.EXPAND|wx.RIGHT, border=40)
        sizer.Add(panelColor, pos=(4, 3), flag=wx.EXPAND|wx.RIGHT, border=40)
        sizer.Add(borderColor, pos=(5, 1), flag=wx.EXPAND|wx.RIGHT, border=40)
        sizer.Add(menuColor, pos=(5, 3), flag=wx.EXPAND|wx.RIGHT, border=40)
        sizer.Add(buttonColor, pos=(6, 1), flag=wx.EXPAND|wx.RIGHT, border=40)
        sizer.Add(inactiveColor, pos=(6, 3), flag=wx.EXPAND|wx.RIGHT, border=40)
        sizer.Add(highlightColor, pos=(7, 1), flag=wx.EXPAND|wx.RIGHT, border=40)
        sizer.Add(selectColor, pos=(7, 3), flag=wx.EXPAND|wx.RIGHT, border=40)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableCol(2)
        sizer.AddGrowableCol(4)
        
        self.SetSizer(sizer)
        self.Layout()


    def CollectColors(self, config):
        for child in self.GetChildren():
            if child.label == 'Frame Colors':
                continue
            key = child.label.lower() + 'Color'
            config[key] = child.color
        return config


    def _OnEraseBackground(self, event):
        pass
    def _OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)
    def Draw(self, dc):
        dc.SetBackground(wx.Brush(self.conf.Get('menuColor')))
        dc.Clear()
###############################################################################################
###############################################################################################


###############################################################################################
###############################################################################################
class WidgetSettings(wx.Panel):


    def __init__(self, parent, conf):
        super().__init__(parent)
        self.conf = conf
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
        self.Display()
        print('widgetSettings')


    def Display(self):
        sizer = wx.GridBagSizer(5, 5)
        
        headerFont = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD)
        header = ScaledStaticText(self, 'Widget Settings', headerFont, conf=self.conf)

        size = (140, 30)
        self.frameColor = ConfigColorSwitcher(self, 'Frame', self.conf.Get('widgetFrameColor'), self.conf, size)
        self.textColor = ConfigColorSwitcher(self, 'Text', self.conf.Get('widgetTextColor'), self.conf, size)
        self.color1 = ConfigColorSwitcher(self, 'Color 1', self.conf.Get('widgetColor1'), self.conf, size)
        self.color2 = ConfigColorSwitcher(self, 'Color 2', self.conf.Get('widgetColor2'), self.conf, size)
        self.color3 = ConfigColorSwitcher(self, 'Color 3', self.conf.Get('widgetColor3'), self.conf, size)
        self.saveWidgetsCheck = CheckBox(self, 'Save Widgets//On Exit', self.conf.Get('saveWidgets'), self.conf)

        sizer.Add(header, pos=(0, 0), span=(3, 7), flag=wx.EXPAND, border=80)
        sizer.Add(self.frameColor, pos=(4, 1), flag=wx.EXPAND|wx.RIGHT, border=40)
        sizer.Add(self.textColor, pos=(4, 3), flag=wx.EXPAND|wx.RIGHT, border=40)
        sizer.Add(self.color1, pos=(5, 1), flag=wx.EXPAND|wx.RIGHT, border=40)
        sizer.Add(self.color2, pos=(5, 3), flag=wx.EXPAND|wx.RIGHT, border=40)
        sizer.Add(self.color3, pos=(5, 5), flag=wx.EXPAND|wx.RIGHT, border=40)
        sizer.Add(self.saveWidgetsCheck, pos=(7, 1), span=(1, 3), flag=wx.ALIGN_CENTER)

        sizer.AddGrowableCol(0)
        # sizer.AddGrowableCol(2)
        # sizer.AddGrowableCol(4)
        sizer.AddGrowableCol(6)
        self.SetSizer(sizer)
        self.Layout()


    def CollectConfig(self, config):
        config['widgetFrameColor'] = self.frameColor.color
        config['widgetTextColor'] = self.textColor.color
        config['widgetColor1'] = self.color1.color
        config['widgetColor2'] = self.color2.color
        config['widgetColor3'] = self.color3.color
        config['saveWidgets'] = self.saveWidgetsCheck.value
        return config


    def _OnEraseBackground(self, event):
        pass
    

    def _OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)
        

    def Draw(self, dc):
        dc.SetBackground(wx.Brush(self.conf.Get('menuColor')))
        dc.Clear()
###############################################################################################
###############################################################################################


###############################################################################################
###############################################################################################
class FontSettingsPanel(wx.Panel):


    def __init__(self, parent, conf):
        super().__init__(parent)
        self.conf = conf
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
        self.Display()


    def Display(self):
        sizer = wx.GridBagSizer(5, 5)
        
        headerFont = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD)
        header = ScaledStaticText(self, 'Fonts', headerFont, conf=self.conf)

        sizer.Add(header, pos=(0, 0), span=(3, 5), flag=wx.EXPAND, border=80)

        sizer.AddGrowableCol(0)
        sizer.AddGrowableCol(2)
        sizer.AddGrowableCol(4)
        self.SetSizer(sizer)
        self.Layout()


    def CollectFonts(self, config):
        # config["regFont"] = "wx.Font(13, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)"
        # config['titleFont'] = "wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD)"
        # config['menuButtonFontBig'] = "wx.Font(20, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)"
        config["regFont"] = self.conf.Get('regFont')
        config['titleFont'] = self.conf.Get('titleFont')
        config['menuButtonFontBig'] = self.conf.Get('menuButtonFontBig')
        return config


    def _OnEraseBackground(self, event):
        pass
    

    def _OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)
        

    def Draw(self, dc):
        dc.SetBackground(wx.Brush(self.conf.Get('menuColor')))
        dc.Clear()
###############################################################################################
###############################################################################################


###############################################################################################
###############################################################################################
class OptionsMenuPanel(wx.Panel):
    
    def __init__(self, frame, conf, **kwargs):
        super(wx.Panel, self).__init__(parent=frame.mainPanel)
        
        self.Name = 'menuPanel'
        self.frame = frame
        self.conf = conf
        
        self.configPanel = ConfigPanel(self, self.conf)
        self.Display()
        
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_BUTTON, self.OnButtonPressed)
        
    def Display(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.configPanel, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=2)
        sizer.Add(OptionsButtonsPanel(self, self.conf), proportion=0, flag=wx.EXPAND|wx.ALL, border=10)
        self.SetSizer(sizer)
        self.Layout()

    def OnButtonPressed(self, event):
        operation = event.GetEventObject().label
        if operation == 'Apply':
            config = self.configPanel.CollectConfig()
            self.conf.WriteConfig(config)
            for child in self.frame.GetChildren():
                child.Refresh()
        elif operation == 'Cancel':
            self.configPanel.RefreshColors()
            for child in self.frame.GetChildren():
                self.Refresh()           
        
    def _OnEraseBackground(self, event):
        pass
        

    def _OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)
        
    def Draw(self, dc):
        width, height = self.GetClientSize()
        dc.SetBackground(wx.Brush(self.conf.Get('menuColor')))
        dc.Clear()
        
        dc.SetPen(wx.Pen(self.conf.Get('borderColor'), width=4))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(0, 0, width, height)
###############################################################################################
###############################################################################################


###############################################################################################
###############################################################################################
class TitleMenuPanel(wx.Panel):
    
    def __init__(self, frame, conf, **kwargs):
        super(wx.Panel, self).__init__(frame.mainPanel, **kwargs)
        
        self.Name = 'menuPanel'
        self.conf = conf

        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        
    def _OnEraseBackground(self, event):
        pass
    
    def _OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)
        
    def Draw(self, dc):
        width, height = self.GetClientSize()
        
        dc.SetBackground(wx.Brush(self.conf.Get('menuColor')))
        dc.Clear()
        
        dc.SetPen(wx.Pen(self.conf.Get('borderColor'), width=4))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(0, 0, width, height)
        
        dc.SetFont(wx.Font(50, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        dc.SetTextForeground(self.conf.Get('textColor'))
        
        textWidth, textHeight = dc.GetTextExtent('SciEnv')
        textX = (width - textWidth) / 2
        textY = (height - textHeight) / 3
        
        dc.DrawText('SciEnv', (textX, textY))
###############################################################################################
###############################################################################################


###############################################################################################
###############################################################################################
class SelectedWidgetButtons(wx.Panel):
    def __init__(self, parent, conf, **kwargs):
        super().__init__(parent=parent)
        
        self.Name = 'menuPanel'
        self.conf = conf
        
        self.Display()
        self.Bind(wx.EVT_BUTTON, self.OnButtonPressed)
        
    def OnButtonPressed(self, event):
        event.Skip()
            
    def Display(self):
        self.SetBackgroundColour(self.conf.Get('menuColor'))
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        butt1 = SimpleButton(self, self.conf, 'Options', size=(120, 40))
        butt2 = SimpleButton(self, self.conf, 'Add Widget', size=(120, 40))
        
        self.sizer.Add(butt1, 0, wx.EXPAND|wx.ALL, border=5)
        self.sizer.Add(butt2, 1, wx.EXPAND|wx.ALL, border=5)
        self.SetSizer(self.sizer)
        self.Layout()
###############################################################################################
###############################################################################################
class WidgetDescription(wx.Panel):


    def __init__(self, parent, conf, name):
        super().__init__(parent)

        self.conf = conf
        self.SetBackgroundColour(self.conf.Get('menuColor'))

        if not name:
            self.name = 'Choose a widget from the left panel.\nYou can get new widgets at\n[...]'
        elif name:
            self.name = name
            self.r_desc()
            print('!!!:  ', self.title, self.version, self.author)
            self.display_all()


    def display_all(self):
        self.sizer = wx.GridBagSizer(0, 0)
        
        self.sizer.Add(ScaledStaticText(self, self.title, font=self.conf.Get('titleFont', True), conf=self.conf), 
                                        pos=(0, 0), span=(0, 10), flag=wx.EXPAND)
        
        self.sizer.Add(ScaledStaticText(self, "by " + self.author, conf=self.conf), 
                                        pos=(1, 0), span=(1, 7), flag=wx.EXPAND)
        
        self.sizer.Add(ScaledStaticText(self, "version - " + self.version, conf=self.conf), 
                                        pos=(1, 7), span=(1, 3), flag=wx.EXPAND)
        
        self.sizer.Add(self.description, pos=(2, 0), span=(1, 10), flag=wx.EXPAND)

        for i in range(0, 10):
            self.sizer.AddGrowableCol(i)
        self.sizer.AddGrowableRow(2)
        
        self.SetSizer(self.sizer)
        self.sizer.Layout()


    def r_desc(self):
        path = f'widgets/{self.name}'
        try:
            with open(path + '/config.json', 'r') as file:
                    data = json.load(file)
                    self.title = data['description_title']
                    self.version = data['version']
                    self.author = data['author']

        except:
            self.title = self.name.title()
            self.version = '1.0'
            self.author = 'Unknown'

        if os.path.isfile(path + '/description.htm'):
            print('has description')
            with open(path + '/description.htm', 'r') as file:
                htmlCode = ''
                for line in file:
                    htmlCode += line

                self.description = html.HtmlWindow(self)
                htmlCode = self.ConvertHTML(htmlCode)
                self.description.SetPage(htmlCode)
                self.description.SetBackgroundColour(self.conf.Get('menuColor'))

        else:
            self.description = StaticText(self, label='add <description.htm> file.', conf=self.conf)


    def ConvertHTML(self, code):
        code = f'<font color={self.conf.Get("textColor")} size="+2">' \
             + code \
             + f'</font>'        

        return code
        

###############################################################################################
###############################################################################################
class WidgetPanelRight(wx.Panel):


    def __init__(self, parent, conf, **kwargs):
        super(wx.Panel, self).__init__(parent=parent)
        
        self.Name = 'menuPanel'
        self.conf = conf

        self.Display()
        self.buttonsPanel.Hide()
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_BUTTON, self.OnButtonPressed)  
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self._OnPaint)  


    def OnButtonPressed(self, event):
        event.Skip()
    

    def Display(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.widgetPanel = WidgetDescription(self, self.conf, name=0)
        self.buttonsPanel = SelectedWidgetButtons(self, self.conf)
        
        self.sizer.Add(self.widgetPanel, 1, wx.EXPAND)
        self.sizer.Add(self.buttonsPanel, 0, wx.EXPAND)           
        self.SetSizer(self.sizer)
        self.Layout()
             

    def _OnEraseBackground(self, event):
        pass


    def _OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)
        

    def Draw(self, dc):
        dc.SetBackground(wx.Brush(self.conf.Get('menuColor')))
        dc.Clear()
###############################################################################################
###############################################################################################


###############################################################################################    
###############################################################################################
class WidgetsMenuPanel(wx.Panel):
    

    def __init__(self, frame, conf, **kwargs):
        super(wx.Panel, self).__init__(parent=frame.mainPanel)
        
        self.Name = 'menuPanel'
        self.frame = frame
        self.conf = conf
        
        self.manager = frame.widgetManager
        self.widgetsSelection = WidgetSelection(self, self.conf, 200)
        
        self.Display()
        
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_BUTTON, self.OnButtonPressed)
        

    def OnButtonPressed(self, event):
        button = event.GetEventObject()
        if isinstance(button, SimpleButton):
            if button.label == 'Add Widget':
                name = self.widgetsSelection.GetSelected()
                self.manager.AddWidget(f'widgets.{name}.main')
        else:

            # display widget description panel
            self.rightPanel.sizer.Detach(self.rightPanel.widgetPanel)
            self.rightPanel.sizer.Detach(self.rightPanel.buttonsPanel)
            self.rightPanel.widgetPanel.Destroy()
            self.rightPanel.widgetPanel = WidgetDescription(self.rightPanel, self.conf, name=self.widgetsSelection.GetSelected())
            self.rightPanel.sizer.Add(self.rightPanel.widgetPanel, 1, flag=wx.EXPAND)
            self.rightPanel.sizer.Add(self.rightPanel.buttonsPanel, 0, flag=wx.EXPAND)

            self.rightPanel.buttonsPanel.Show()
            self.rightPanel.Layout()
        

    def Display(self):
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.widgetsSelection, proportion=0, flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, border=2)
        self.rightPanel = WidgetPanelRight(self, self.conf)
        
        self.sizer.Add(self.rightPanel, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.SetSizer(self.sizer)
        

    def _OnEraseBackground(self, event):
        pass


    def _OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)
        

    def Draw(self, dc):
        width, height = self.GetClientSize()
        dc.SetBackground(wx.Brush(self.conf.Get('menuColor')))
        dc.Clear()
        
        dc.SetPen(wx.Pen(self.conf.Get('borderColor'), width=4))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(0, 0, width, height) 
###############################################################################################
###############################################################################################

###############################################################################################
###############################################################################################
class WidgetNamePanel(PanelButton):
    

    def __init__(self, parent, name, conf, size=(200, 75), **kwargs):
        wx.Control.__init__(self, parent, size=size, id=wx.ID_ANY, style=wx.NO_BORDER, **kwargs)

        self.name = name
        self.conf = conf
        self.size = size

        self.Bind(wx.EVT_LEFT_UP, self._onMouseUp)
        self.Bind(wx.EVT_ERASE_BACKGROUND,self._onEraseBackground)
        self.Bind(wx.EVT_PAINT,self._onPaint)
        
        self._active = False
        

    def Draw(self, dc):
        if self.isActive:
            dc.SetBackground(wx.Brush(self.conf.Get('highlightColor')))
        else:
            dc.SetBackground(wx.Brush(self.conf.Get('panelColor')))
        dc.Clear()

        dc.SetFont(wx.Font(20, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        dc.SetTextForeground(self.conf.Get('textColor'))
        nameWidth, nameHeight = dc.GetTextExtent(self.name)
        nameX, nameY = (self.size[0]-nameWidth) / 2, (self.size[1] - nameHeight) / 5
        
        dc.DrawText(self.name, nameX, nameY)
        
        dc.SetPen(wx.Pen(self.conf.Get('borderColor'), width=4))
        dc.DrawLine(0, self.size[1], self.size[0], self.size[1])
###############################################################################################
###############################################################################################


###############################################################################################
###############################################################################################
class WidgetSelection(wx.Panel):
    

    def __init__(self, parent, conf, width):
        super(wx.Panel, self).__init__(parent, style=wx.NO_BORDER)
        
        self.width = width
        self.parent = parent
        self.conf = conf
        
        self.Display()
        
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_BUTTON, self.OnPanelPressed)
        

    def OnPanelPressed(self, event):
        widget = event.GetEventObject()
        for child in self.GetChildren():
            child.isActive = False
        widget.isActive = True
        event.Skip()
    

    def GetSelected(self):
        for child in self.GetChildren():
            if child.isActive:
                return child.name
        

    def Display(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        widgetList = self.parent.manager.GetWidgetList()
        for name in widgetList:
            self.sizer.Add(WidgetNamePanel(self, name, self.conf), 0, wx.EXPAND|wx.RIGHT, border=2)
        self.SetSizer(self.sizer)
        self.Layout()
        

    def _OnEraseBackground(self, event):
        pass
    

    def _OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)

    
    def Draw(self, dc):
        dc.Clear()
        size = (self.width, self.parent.frame.mainPanel.GetSize()[1] - 45)
        self.SetClientSize(size)   
        dc.SetBackground(wx.Brush(self.conf.Get('menuColor')))
        dc.Clear()
        
        dc.SetPen(wx.Pen(self.conf.Get('borderColor'), width=4))
        dc.DrawLine(self.width, 0, self.width, size[1])