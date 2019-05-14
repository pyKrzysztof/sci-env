import wx
import os
import pickle
import json




class ItemNotFoundError(Exception):
    pass



class ConfigManager():
    

    def __init__(self):
        self.config = self.ReadConfig()
        if not self.config:
            self.FactoryReset()
        pass
    

    def ReadConfig(self):
        try:
            with open('properties.json', 'r') as cnf:
                config = json.load(cnf)
                if not config:
                    return None
            return config
        except:
            return None
    

    def WriteConfig(self, config):
        with open('properties.json', 'w') as cnf:
            print('!DEBUG: Config updated.')
            json.dump(config, cnf, separators=(',\n',':'))
    

    def FactoryReset(self):
        config = {"textColor":"#dedede",
                  "panelColor":"#474747",
                  "menuColor":"#767676",
                  "borderColor":"#000000",
                  "inactiveColor":"#333333",
                  "buttonColor":"#313131",
                  "selectColor":"#bbbbbb",
                  "highlightColor":"#a3a3a3",
                  "widgetFrameColor":"#353535",
                  "widgetTextColor":"black",
                  "widgetColor1":"#cccccc",
                  "widgetColor2":"#000000",
                  "widgetColor3":"#e46969",
                  "saveWidgets":True,
                  "regFont":"wx.Font(13, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)",
                  "titleFont":"wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD)",
                  "menuButtonFontBig":"wx.Font(20, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)"}
        
        self.WriteConfig(config)
        self.ReadConfig()
        

    def Get(self, item, evaluate=False):
        self.config = self.ReadConfig()
        if not self.config:
            self.FactoryReset()
        if item in self.config:
            if evaluate:
                return eval(self.config[item])
            return self.config[item]
        raise ItemNotFoundError(item)




class WidgetManager():
    

    def __init__(self, frame, conf, widgets=None):
        self.frame = frame
        self.panelManager = self.frame.panelManager
        self.conf = conf
        if widgets is not None:
            self._AddWidgets(widgets)
        self.widgets = []
        try:
            self.LoadWidgets()
        except:
            raise


    def LoadWidgets(self):
        if not self.conf.Get('saveWidgets'):
            return

        with open('preserved.txt', 'rb') as file:
            try:
                data = pickle.load(file)
                for name, pos, size, panel_idx in data:
                    self.AddWidget(name, panel_idx)
                    self.widgets[-1].SetPosition(pos)
                    self.widgets[-1].SetSize(size)
            except:
                pass


    def SaveWidgets(self):
        if not self.conf.Get('saveWidgets'):
            return

        data = []
        for widget in self.widgets:
            try:
                data.append( [widget.name, widget.GetPosition(), widget.GetSize(), widget.GetParent().idx] )
            except:
                data = data
        with open('preserved.txt', 'wb') as file:
            pickle.dump(data, file)
    

    def GetWidgetList(self):
        names = []
        for file in os.listdir(path='widgets/'):
            names.append(file)
        return names
        

    def AddWidget(self, name, idx=None):
        if not idx:
            idx = self.panelManager.current

        # import the widget module
        exec(f'import {name}')
        wrapper = eval(f'{name}.Widget')
        
        # next use that wrapper, the parent has to be current panel from panel manager.
        self.widgets.append(wrapper(self.panelManager.panels[idx], self.conf))
        self.widgets[-1].Fit()