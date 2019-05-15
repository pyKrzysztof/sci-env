import wx


class ButtonBase(wx.Control):

    def __init__(self, parent, config, label, **kwargs):
        wx.Control.__init__(self, parent, id=wx.ID_ANY,
                            style=wx.NO_BORDER, **kwargs)

        self.label = label
        self.config = config
        self._mouseIn = self._mouseDown = False
        self.font = config.get_font('small')
        if label == '☰':
            self.font.SetPointSize(16)

        self.Bind(wx.EVT_LEFT_DOWN, self._onMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self._onMouseUp)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._onMouseLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self._onMouseEnter)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._onEraseBackground)
        self.Bind(wx.EVT_PAINT, self._onPaint)

    def _onMouseEnter(self, event):
        self._mouseIn = True
        self.Refresh()

    def _onMouseLeave(self, event):
        self._mouseIn = False
        self.Refresh()

    def _onMouseDown(self, event):
        self._mouseDown = True
        self.Refresh()

    def _onMouseUp(self, event):
        self._mouseDown = False
        self.Refresh()
        self.sendButtonEvent()

    def sendButtonEvent(self):
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, self.GetId())
        event.SetInt(0)
        event.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(event)

    def _onEraseBackground(self, event):
        # reduce flicker
        pass

    def _onPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self._GetBestSize(dc)
        self.Draw(dc)

    def _GetBestSize(self, dc):
        dc.SetFont(self.font)
        textWidth, textHeight = dc.GetTextExtent(self.label)
        width, height = self.GetClientSize()
        if not width or not height:
            width, height = (textWidth + 12, textHeight + 12)
            print(width, height)
            self.SetMinClientSize((width, height))

    def Draw(self, dc):
        """Overwrite this"""


#< Simple Button >---------------------------------------------------
class SimpleButton(ButtonBase):

    def Draw(self, dc):
        dc.SetFont(self.font)
        dc.SetTextForeground(self.config.get_color('text'))
        dc.SetBackground(wx.Brush(self.config.get_color('button')))
        if self._mouseIn:
            dc.SetBackground(wx.Brush(self.config.get_color('highlight')))
        if self._mouseDown:
            dc.SetBackground(wx.Brush(self.config.get_color('select')))
        dc.Clear()

        width, height = self.GetClientSize()
        textWidth, textHeight = dc.GetTextExtent(self.label)
        textX, textY = (width - textWidth) / 2, (height - textHeight) / 2
        dc.DrawText(self.label, textX, textY)

        dc.SetPen(wx.Pen(self.config.get_color('border'), width=3))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(0, 0, width, height)


#< Panel Button >----------------------------------------------------
class PanelButton(wx.Control):

    def __init__(self, parent, config, label, idx, **kwargs):
        wx.Control.__init__(self, parent, id=wx.ID_ANY,
                            style=wx.NO_BORDER, **kwargs)

        self.idx = idx
        self.label = label
        self.conf = config

        self.Bind(wx.EVT_LEFT_UP, self._onMouseUp)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._onEraseBackground)
        self.Bind(wx.EVT_PAINT, self._onPaint)

        self._active = False

    def _onMouseUp(self, event):
        if self.isActive:
            return
        self.isActive = True
        self.sendButtonEvent()

    def sendButtonEvent(self):
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, self.GetId())
        event.SetInt(0)
        event.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(event)

    def _onEraseBackground(self, event):
        # reduce flicker
        pass

    def _onPaint(self, event):
        dc = wx.BufferedPaintDC(self)

        self.Draw(dc)

    def Draw(self, dc):
        # Getting the width and the height, if None, than set them accordingly.
        width, height = self.GetClientSize()
        if not width or not height:
            width, height = (textWidth + 12, textHeight + 12)
            self.SetSize((width, height))

        dc.SetFont(self.conf.get_font('small'))
        dc.SetTextForeground(self.conf.get_color('text'))
        if self.isActive:
            dc.SetBackground(wx.Brush(self.conf.get_color('panel')))
        else:
            dc.SetBackground(wx.Brush(self.conf.get_color('inactive')))
        dc.Clear()

        dc.SetPen(wx.Pen(self.conf.get_color('border'), width=4))
        dc.DrawLine((0, 0), (width, 0))
        dc.DrawLine((width, 0), (width, height))
        if not self.isActive:
            dc.DrawLine((width, height), (0, height))

        textWidth, textHeight = dc.GetTextExtent(self.label)
        textX, textY = (width - textWidth) / 2, (height - textHeight) / 2
        dc.DrawText(self.label, textX, textY)

    def __get_isActive(self):
        return self._active

    def __set_isActive(self, value):
        self._active = value
        self.Refresh()

    isActive = property(__get_isActive, __set_isActive)

#< Menu Button, the one displayed in the buttons panel.>-------------


class MenuButton(ButtonBase):

    """
    This class should not be used in custom widgets. 
    It's only used in the upper left corner of the screen.\
    """

    def __init__(self, parent, config, **kwargs):
        ButtonBase.__init__(self, parent=parent,
                            config=config, label='☰', **kwargs)

    def Draw(self, dc):

        width, height = self.GetClientSize()

        dc.SetFont(self.font)
        dc.SetTextForeground(self.config.get_color('text'))
        dc.SetBackground(wx.Brush(self.config.get_color('menu')))
        dc.Clear()

        textWidth, textHeight = dc.GetTextExtent(self.label)
        textX = (width - textWidth) / 2
        textY = (height - textHeight) / 2
        dc.DrawText(self.label, textX, textY)

        dc.SetPen(wx.Pen(self.config.get_color('border'), width=3))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(0, 0, width, height)

#< Menu Switch Button >----------------------------------------------


class MenuPanelSwitchButton(ButtonBase):

    def __init__(self, parent, config, label, **kwargs):
        ButtonBase.__init__(self, parent, config, label, **kwargs)
        self._active = False

    def _onMouseUp(self, event):
        self._mouseDown = False
        if self.isActive:
            self.isActive = False
        else:
            self.isActive = True
        self.sendButtonEvent()

    def Draw(self, dc):
        width, height = self.GetClientSize()

        dc.SetFont(self.config.get_font('large'))
        dc.SetTextForeground(self.config.get_color('text'))
        dc.SetBackground(wx.Brush(self.config.get_color('button')))
        if self._mouseIn:
            dc.SetBackground(wx.Brush(self.config.get_color('highlight')))
        if self._mouseDown or self.isActive:
            dc.SetBackground(wx.Brush(self.config.get_color('select')))

        dc.Clear()

        textWidth, textHeight = dc.GetTextExtent(self.label)
        textX, textY = (width - textWidth) / 2, (height - textHeight) / 2

        dc.DrawText(self.label, textX, textY)

        dc.SetPen(wx.Pen(self.config.get_color('border'), width=5))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(0, 0, width, height)

    def __get_isActive(self):
        return self._active

    def __set_isActive(self, value):
        self._active = value
        self.Refresh()

    isActive = property(__get_isActive, __set_isActive)

#< Config Label/Color >----------------------------------------------


class ConfigColorSwitcher(wx.Control):

    def __init__(self, parent, label, color, conf, size, **kwargs):
        wx.Control.__init__(self, parent, id=wx.ID_ANY,
                            size=size, style=wx.NO_BORDER, **kwargs)

        self.label = label
        self.color = color
        self.conf = conf

        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
        self.Bind(wx.EVT_ENTER_WINDOW, self._onMouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._onMouseLeave)
        self.Bind(wx.EVT_LEFT_DOWN, self._onMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self._onMouseUp)

        self._mouseIn = False

    def _onMouseEnter(self, event):
        self._mouseIn = True
        self.Refresh()

    def _onMouseLeave(self, event):
        self._mouseIn = False
        self.Refresh()

    def _onMouseDown(self, event):
        #self._mouseDown = True
        self._mouseIn = False
        self.Refresh()

    def _onMouseUp(self, event):
        #self._mouseDown = False
        self.Refresh()
        self.sendButtonEvent()

    def sendButtonEvent(self):
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, self.GetId())
        event.SetInt(0)
        event.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(event)

    def _OnEraseBackground(self, event):
        pass

    def _OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)

    def Draw(self, dc):
        dc.SetBackground(wx.Brush(self.conf.get_color('menu')))
        dc.SetTextForeground(self.conf.get_color('text'))
        dc.SetFont(self.conf.get_font('small'))
        dc.Clear()

        width, height = self.GetClientSize()
        textWidth, textHeight = dc.GetTextExtent(self.label)
        if textWidth > width - height:
            width = textWidth + height + 30
            self.SetMinSize((width, height))
            width, height = self.GetClientSize()
        textX = ((width - height) - textWidth) / 2
        textY = (height - textHeight) / 2

        dc.DrawText(self.label, (textX, textY))

        if self._mouseIn:
            dc.SetPen(wx.Pen(self.conf.get_color('highlight'), width=1))
            dc.DrawLine((textX, textHeight + 5),
                        (textX + textWidth, textHeight + 5))

        dc.SetPen(wx.Pen(self.conf.get_color('border'), width=2))
        dc.SetBrush(wx.Brush(self.color))
        dc.DrawRectangle((width - height), 0, height, height)


class CheckBox(wx.Control):

    def __init__(self, parent, label, value, conf):
        super().__init__(parent, id=wx.ID_ANY, style=wx.NO_BORDER)

        self.label = label
        self.conf = conf
        self.value = value
        self.font = conf.get_font('small')
        self.rectSize = 20

        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
        self.Bind(wx.EVT_ENTER_WINDOW, self._OnMouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._OnMouseLeave)
        self.Bind(wx.EVT_LEFT_UP, self._OnMouseUp)

        self._mouseIn = self._mouseDown = False

    def _OnMouseEnter(self, e):
        self._mouseIn = True
        self.Refresh()

    def _OnMouseLeave(self, e):
        self._mouseIn = False
        self.Refresh()

    def _OnMouseUp(self, e):
        self.value = False if self.value else True
        self.Refresh()

    def _OnEraseBackground(self, e):
        pass

    def _OnPaint(self, e):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)

    def Draw(self, dc):
        dc.SetBackground(wx.Brush(self.conf.get_color('menu')))
        dc.SetTextForeground(self.conf.get_color('text'))
        dc.SetFont(self.font)
        dc.Clear()

        dc.SetPen(wx.Pen(self.conf.get_color('border'), width=2))
        dc.SetBrush(wx.Brush(self.conf.get_color('select')
                             if self.value else self.conf.get_color('inactive')))

        width, height = self.GetClientSize()
        textWidth, textHeight = dc.GetTextExtent(self.label)
        if self.label.find('//') != -1:
            nl = self.label.find('//')
            text1 = self.label[:nl]
            text2 = self.label[nl + 2:]
            text1Width, text1Height = dc.GetTextExtent(text1)
            text2Width, text2Height = dc.GetTextExtent(text2)
            newHeight = text1Height + text2Height
            newWidth = (text1Width if text1Width > text2Width else text2Width) \
                     + newHeight
            self.SetMinSize((newWidth, newHeight))
            width, height = self.GetClientSize()
            text1X, text1Y = (width - height - text1Width) / 2, 0
            text2X, text2Y = (width - height - text2Width) / 2, height / 2
            dc.DrawText(text1, text1X, text1Y)
            dc.DrawText(text2, text2X, text2Y)
            longest = text1Width if text1Width > text2Width else text2Width
            rect_start = (text1X if longest == text1Width else text2X) + longest
            

        else:
            self.SetMinSize((textWidth + height + self.rectSize, textHeight))
            width, height = self.GetClientSize()
            textX, textY = (width - height - textWidth) / \
                2, (height - textHeight) / 2
            dc.DrawText(self.label, textX, textY)
            rect_start = width - height + padding

        padding = (height - self.rectSize) / 2
        dc.DrawRectangle(rect_start + padding, padding,
                         self.rectSize, self.rectSize)
        
