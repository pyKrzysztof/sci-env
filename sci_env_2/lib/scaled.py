import wx

class ScaledStaticText(wx.Control):
    
    def __init__(self, parent, label, font=None, bgColor=None, textColor=None, conf=None, size=(100, 40)):
        super().__init__(parent, style=wx.NO_BORDER, size=size)
        
        self.label = label
        self.font = font
        self.color = textColor
        self.bgColor = bgColor
        self.conf = conf
        self.sizeConfigured = False

        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        
    def _OnEraseBackground(self, event):
        pass
    
    def _OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)
        
    def Draw(self, dc):
        if self.bgColor:
            dc.SetBackground(wx.Brush(self.bgColor))
        elif self.conf:
            dc.SetBackground(wx.Brush(self.conf.get_color('menu')))
        dc.Clear()
        
        if self.font:
            dc.SetFont(self.font)
        elif self.conf:
            dc.SetFont(self.conf.get_font('small'))
            
        if self.color:
            dc.SetTextForeground(self.color)
        elif self.conf:
            dc.SetTextForeground(self.conf.get_color('text'))

        width, height = self.GetClientSize()
        textWidth, textHeight = dc.GetTextExtent(self.label)
        if width > textWidth:
            posX = (width - textWidth) / 2
            posY = (height - textHeight) / 2
            dc.DrawText(self.label, posX, posY)
        
        elif not self.sizeConfigured:
            height = height * 2.5
            self.SetMinClientSize((width, height))
            self.SetClientSize((width, height))
            self.GetParent().Layout()
            length = len(self.label)
            
            for i, s in enumerate(self.label):
                if s == ' ' and dc.GetTextExtent(self.label[:i])[0] < width:
                    last_space = i

            self.label_0 = self.label[:last_space]
            self.label_1 = self.label[last_space:]

            label_0_width, label_0_height = dc.GetTextExtent(self.label_0)
            label_1_width, label_1_height = dc.GetTextExtent(self.label_1)
            self.posX_0 = (width - label_0_width) / 2
            self.posY_0 = (height/2 - label_0_height) / 2
            self.posX_1 = (width - label_1_width) / 2
            self.posY_1 = (height*1.5 - label_1_height) / 2
            dc.DrawText(self.label_0, self.posX_0, self.posY_0)
            dc.DrawText(self.label_1, self.posX_1, self.posY_1)
            self.sizeConfigured = True

        elif self.sizeConfigured:
            dc.DrawText(self.label_0, self.posX_0, self.posY_0)
            dc.DrawText(self.label_1, self.posX_1, self.posY_1)




def ScaledTextCtrl(self, value=None, style=0, font=None):
    """Use with StaticText only!"""
    
    if not font:
        font = self.cnf['regFont']
        
    # TEMP ITEM
    temp = wx.TextCtrl(self, value=value, style=style, size=(0, 0))
    temp.SetFont(font)
    bestSize = temp.GetBestSize()
    temp.Destroy()
    
    # ACTUAL ITEM
    text = wx.TextCtrl(self, value=value, style=style, size=bestSize)
    text.SetFont(font)
    return text