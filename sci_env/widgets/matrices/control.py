import wx
from lib.buttons import ButtonBase




class Button(ButtonBase):


	def Draw(self, dc):
		dc.SetFont(self.config.Get('regFont', True))
		dc.SetTextForeground(self.config.Get('textColor'))
		dc.SetBackground(wx.Brush(self.config.Get('buttonColor')))
		if self._mouseIn:
			dc.SetBackground(wx.Brush(self.config.Get('highlightColor')))
		if self._mouseDown:
			dc.SetBackground(wx.Brush(self.config.Get('selectColor')))
		dc.Clear()

		width, height = self.GetClientSize()
		textWidth, textHeight = dc.GetTextExtent(self.label)
		textX, textY = (width - textWidth)/2, (height - textHeight)/2
		dc.DrawText(self.label, textX, textY)
		
		dc.SetPen(wx.Pen(self.config.Get('borderColor'), width=3))
		dc.SetBrush(wx.TRANSPARENT_BRUSH)
		dc.DrawRectangle(0, 0, width, height)



class ControlPanel(wx.Panel):


	def __init__(self, parent, appConf, widgetConf, matrix_a, matrix_b, matrix_c):
		super().__init__(parent)

		self.parent = parent
		self.appConf = appConf
		self.widgetConf = widgetConf

		self.in_matrices = [matrix_a, matrix_b]
		self.out_matrix = matrix_c

		self.Display()

		self.Bind(wx.EVT_PAINT, self._OnPaint)
		self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
		self.Bind(wx.EVT_BUTTON, self._OnButton)


	def Display(self):
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		butt1 = Button(self, self.appConf, 'Calculate', size=(100, 40))
		self.sizer.Add(butt1, 1, flag=wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, border=5)
		self.SetSizer(self.sizer)
		self.Layout()


	def Draw(self, dc):
		dc.SetBackground(wx.Brush(self.appConf.Get('widgetColor1')))
		dc.Clear()


	def _OnButton(self, e):
		e.Skip()


	def _OnEraseBackground(self, e):
		pass


	def _OnPaint(self, e):
		dc = wx.BufferedPaintDC(self)
		self.Draw(dc)