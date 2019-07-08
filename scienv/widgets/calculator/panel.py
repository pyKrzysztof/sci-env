import wx
from wx.richtext import RichTextCtrl, RE_READONLY
from .expression_manager import evaluate
from decimal import *


class Panel(wx.Panel):

    def __init__(self, parent, appConf):
        super().__init__(parent, style=wx.NO_BORDER, size=(300, 150))

        self.config = appConf
        self.font = self.config.get_font('small')
        self.bigFont = self.config.get_font('medium')
        self.fontSize = self.font.GetPointSize()

        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)

        self.DefineStyles()
        self.Display()

    def DefineStyles(self):
        self.REGULAR_STYLE = wx.TextAttr(self.config.get_color(
            'text', 'widget'), self.config.get_color('color1', 'widget'))
        self.REGULAR_STYLE.SetFont(self.font)
        self.REGULAR_STYLE.SetFontSize(self.fontSize)
        self.KEYWORD_STYLE = wx.TextAttr('#ff7700')
        self.KEYWORD_STYLE.SetFont(self.font)
        self.KEYWORD_STYLE.SetFontWeight(wx.FONTWEIGHT_BOLD)
        self.KEYWORD_STYLE.SetFontStyle(wx.FONTSTYLE_ITALIC)
        self.KEYWORD_STYLE.SetFontSize(self.fontSize)
        self.NUMBER_STYLE = wx.TextAttr('#6600ff')
        self.NUMBER_STYLE.SetFont(self.font)
        self.NUMBER_STYLE.SetFontSize(self.fontSize)

    def Display(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.hist = History(self, style=wx.NO_BORDER |
                            wx.TE_RICH2 | wx.TE_READONLY, size=(100, 80))
        self.hist.SetFont(self.bigFont)
        self.hist.SetBackgroundColour(
            self.config.get_color('color1', 'widget'))
        self.hist.SetDefaultStyle(self.REGULAR_STYLE)

        self.inp = Input(self, self.config.get_color('color1', 'widget'))
        self.inp.SetFont(self.font)
        self.inp.SetForegroundColour(self.config.get_color('text', 'widget'))

        self.inp.Bind(wx.EVT_TEXT, self.ProcessInput)
        self.inp.Bind(wx.EVT_KEY_DOWN, self.ProcessKey)
        self.inp.Bind(wx.EVT_TEXT_ENTER, self.SubmitInput)
        self._lastKey = 999

        sizer.Add(self.hist, 1, flag=wx.EXPAND)
        sizer.Add((-1, 2))
        sizer.Add(self.inp, 0, flag=wx.EXPAND)

        self.SetSizer(sizer)
        self.Layout()

    def ProcessKey(self, e):
        value = self.inp.GetValue()
        length = len(value)
        key = e.GetUnicodeKey()
        if self._lastKey == 0:  # if shift/ctrl
            if key == 56 or key == 49 or key == 53 or key == 54 or key == 65 or key == 67 or key == 86:
                self._lastKey = 999
                e.Skip()
                return
            elif key == 0:
                e.Skip()
                return
        if key == 9:
            return
        elif 65 <= key <= 90:
            self.inp.SetDefaultStyle(self.KEYWORD_STYLE)
            self.inp.EmulateKeyPress(e)
            return
        elif 48 <= key <= 57:
            self.inp.SetDefaultStyle(self.NUMBER_STYLE)
            self.inp.EmulateKeyPress(e)
            return
        else:
            self._lastKey = key
            e.Skip()

    def ProcessInput(self, e):
        # allows combined keys, that couldn't be simulated by ProcessKey.
        pass

    def SubmitInput(self, e):
        value = self.inp.GetValue().strip()
        result = evaluate(value)
        self.hist.SetDefaultStyle(self.REGULAR_STYLE)
        if result[0] == None:
            self.hist.AppendText(result[1] + '\n')
        else:
            result = f'{result[0]}'
            self.hist.AppendText(f'{value} = {result}\n')
            self.inp.SetDefaultStyle(self.NUMBER_STYLE)
            self.inp.SetValue(f'{result}')

    def Draw(self, dc):
        dc.SetBackground(wx.Brush(self.config.get_color('frame', 'widget')))
        dc.Clear()

    def _OnEraseBackground(self, e):
        pass

    def _OnPaint(self, e):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)


class History(RichTextCtrl):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SetInsertionPoint(0)


class Input(wx.TextCtrl):

    def __init__(self, parent, bgcolor):
        super().__init__(parent,
                         style=wx.NO_BORDER | wx.TE_RICH | wx.TE_MULTILINE
                         | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB | wx.TE_RIGHT,
                         size=(100, 40))
        self.SetBackgroundColour(bgcolor)
        width, height = self.GetClientSize()
        self.SetMinSize((width, 3 * parent.fontSize + 5))
