import wx
from widget import WidgetBaseClass
from widgets.matrices.panel import Panel



class Widget(WidgetBaseClass):

    name = __name__

    def __init__(self, parent, _conf):

        # inheriting from wx.Panel | not from WidgetBaseClass
        super(wx.Panel, self).__init__(parent)

        # initializing the widget
        self.InitWidget(_conf, __name__)

        # Adding the Panel
        self.AddPanel(Panel(self, _conf, self.widgetConf))
        
        # fixing the layout
        self.Layout()