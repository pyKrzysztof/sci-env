import wx
from ...lib import ScaledStaticText
import numpy as np



class Matrix(wx.Panel):


	def __init__(self, parent, appConf, matrixFont, dimensions):
		super().__init__(parent)
		self.config = appConf
		self.parent = parent
		self.font = matrixFont
		self.fontSize = self.font.GetPointSize()

		rows, cols = [int(n) for n in dimensions.split('x')]
		
		self.DisplayGrid(rows, cols)
		self.CalculateSize()

		self.Bind(wx.EVT_PAINT, self._OnPaint)
		self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)


	def CalculateSize(self):
		width, height = (self.cols*(self.fontSize+20), self.rows*(self.fontSize+5))
		self.SetMinSize((width, height))


	def DisplayGrid(self, rows, cols):
		try:
			self.panel.Destroy()
		except:
			pass

		self.rows = rows
		self.cols = cols

		self.panel = wx.Panel(self)
		self.panel.SetBackgroundColour(self.config.get_color('color1', 'widget'))
		self.panel.sizer = wx.GridSizer(rows, cols, 0, 0)

		size = (self.fontSize+20, self.fontSize+5)
		fg = self.config.get_color('text', 'widget')
		bg = self.config.get_color('color1', 'widget')

		for row in range(0, rows):
			for col in range(0, cols):
				self.panel.sizer.Add(TextField(self.panel, self.font, fg, bg, size=size), 
									flag=wx.EXPAND)

		self.panel.SetSizer(self.panel.sizer)
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.panel, 1, flag=wx.EXPAND|wx.ALL, border=3)
		self.SetSizer(self.sizer)

		self.Layout()


	def ReadValues(self):
		array = []
		row = []
		nxt = self.cols - 1
		for index, child in enumerate(self.panel.GetChildren()):
			row.append(child.GetValue())

			if index == nxt:
				nxt = nxt + self.cols
				array.append(row)
				row = []

		return array


	def WriteValues(self, array):
		unpacked = []
		if self.rows == 1:
			unpacked = [str(num) for num in array]
		else:
			for subarray in array:
				for num in subarray:
					unpacked.append(str(num))
		print(unpacked)

		for index, child in enumerate(self.panel.GetChildren()):
			child.SetValue(unpacked[index])



	def Draw(self, dc):
		dc.SetBackground(wx.Brush(self.config.get_color('color1', 'widget')))
		dc.Clear()


		width, height = self.GetClientSize()
		dc.SetBrush(wx.TRANSPARENT_BRUSH)
		dc.SetPen(wx.Pen(self.config.get_color('color2', 'widget'), width=5))
		dc.DrawRectangle(0, 0, width, height)
		padding = self.fontSize
		dc.SetPen(wx.Pen(self.config.get_color('color1', 'widget'), width=10))
		dc.DrawLine(padding, 0, width-padding, 0)
		dc.DrawLine(padding, height, width-padding, height)
		#### draw 2 horizontal lines, one at the bottom, one at the top


	def _OnEraseBackground(self, e):
		pass


	def _OnPaint(self, e):
		dc = wx.BufferedPaintDC(self)
		self.Draw(dc)



class TextField(wx.TextCtrl):


	def __init__(self, parent, font, fgColor, bgColor, size, name=None):
		super().__init__(parent, value='0', style=wx.TE_CENTER|wx.NO_BORDER|wx.TE_PROCESS_ENTER, size=size)
		self.name = name
		self.SetFont(font)
		self.SetForegroundColour(fgColor)
		self.SetBackgroundColour(bgColor)
		self.HideNativeCaret()



class MainPanel(wx.Panel):


	def __init__(self, parent, appConf, widgetConf):
		super().__init__(parent)

		self.config = appConf
		self.widgetConf = widgetConf

		self.Bind(wx.EVT_PAINT, self._OnPaint)
		self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)

		self.Display()


	def Display(self):

		sizer = wx.GridBagSizer(0, 0)

		matrixFont = eval(self.widgetConf['matrixFont'])
		textFont = self.config.get_font('medium')

		dim_a = TextField(self, textFont, 
						  self.config.get_color('text', 'widget'),
						  self.config.get_color('color2', 'widget'),
						  size=(200, 30), name='a')
		dim_a.Bind(wx.EVT_TEXT_ENTER, self.ChangeDimensions)
		dim_a.SetValue('3x3')

		dim_b = TextField(self, textFont, 
						  self.config.get_color('text', 'widget'),
						  self.config.get_color('color2', 'widget'),
						  size=(200, 30), name='b')
		dim_b.Bind(wx.EVT_TEXT_ENTER, self.ChangeDimensions)
		dim_b.SetValue('3x3')

		x_text = ScaledStaticText(self, 'x', textFont, 
								  self.config.get_color('color1', 'widget'), self.config.get_color('text', 'widget'),
								  size=(20, 20))

		self.matrix_a = Matrix(self, self.config, matrixFont, dimensions='3x3')
		self.matrix_b = Matrix(self, self.config, matrixFont, dimensions='3x3')
		self.matrix_c = Matrix(self, self.config, matrixFont, dimensions='3x3')

		sizer.Add(dim_a, pos=(0, 0), span=(1, 2), flag=wx.EXPAND|wx.ALL, border=10)
		sizer.Add(dim_b, pos=(0, 3), span=(1, 2), flag=wx.EXPAND|wx.ALL, border=10)
		sizer.Add(x_text, pos=(1, 2), flag=wx.EXPAND)
		sizer.Add(self.matrix_a, pos=(1, 0), span=(1, 2), 
						flag=wx.EXPAND|wx.ALL, border=20)
		sizer.Add(self.matrix_b, pos=(1, 3), span=(1, 2), 
						flag=wx.EXPAND|wx.ALL, border=20)
		sizer.Add(self.matrix_c, pos=(3, 0), span=(1, 5), 
						flag=wx.EXPAND|wx.RIGHT|wx.LEFT|wx.BOTTOM, border=20)
		
		sizer.AddGrowableCol(0)
		sizer.AddGrowableCol(1)
		sizer.AddGrowableCol(3)
		sizer.AddGrowableCol(4)
		sizer.AddGrowableRow(1)
		sizer.AddGrowableRow(3)
		
		self.SetSizer(sizer)
		self.Layout()

	def ChangeDimensions(self, e):
		print('change dimensions')
		try:
			shape = e.GetEventObject().GetValue()
			matrix = e.GetEventObject().name
			rows, cols = [int(n) for n in shape.split('x')]
			if matrix == 'a':
				mx = self.matrix_a
			else:
				mx = self.matrix_b
			mx.DisplayGrid(rows, cols)
			mx.CalculateSize()

		except:
			raise


	def Draw(self, dc):
		dc.SetBackground(wx.Brush(self.config.get_color('color1', 'widget')))
		dc.Clear()


	def _OnEraseBackground(self, e):
		pass


	def _OnPaint(self, e):
		dc = wx.BufferedPaintDC(self)
		self.Draw(dc)