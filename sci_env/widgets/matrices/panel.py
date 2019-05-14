import wx
import numpy as np
from widgets.matrices.matrix import MainPanel
from widgets.matrices.control import ControlPanel


class Panel(wx.Panel):


	def __init__(self, parent, appConf, widgetConf):
		super().__init__(parent, size=(475, 300))

		self.Bind(wx.EVT_PAINT, self._OnPaint)
		self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
		self.Bind(wx.EVT_BUTTON, self.OnButton)


		self.appConf = appConf
		self.widgetConf = widgetConf

		self.Display()


	def Display(self):

		sizer = wx.BoxSizer(wx.VERTICAL)
		self.matrixPanel = MainPanel(self, self.appConf, self.widgetConf)
		self.controlPanel = ControlPanel(self, self.appConf, self.widgetConf, 
										 self.matrixPanel.matrix_a, 
										 self.matrixPanel.matrix_b, 
										 self.matrixPanel.matrix_c)

		sizer.Add(self.matrixPanel, 1, flag=wx.EXPAND)
		sizer.Add(self.controlPanel, 0, flag=wx.EXPAND)

		self.SetSizer(sizer)
		self.Layout()

	def OnButton(self, e):
		name = e.GetEventObject().label
		if name == 'Calculate':
			MultiplyMatrices(self.matrixPanel.matrix_a, 
							 self.matrixPanel.matrix_b, 
							 self.matrixPanel.matrix_c)



	def Draw(self, dc):
		dc.SetBackground(wx.Brush(self.appConf.Get('widgetColor1')))
		dc.Clear()


	def _OnEraseBackground(self, e):
		pass


	def _OnPaint(self, e):
		dc = wx.BufferedPaintDC(self)
		self.Draw(dc)


def MultiplyMatrices(matrix_a, matrix_b, out):
	A = np.array(matrix_a.ReadValues(), dtype=float)
	B = np.array(matrix_b.ReadValues(), dtype=float)
	C = A.dot(B)
	c_rows, c_cols = C.shape
	out.DisplayGrid(c_rows, c_cols)
	out.CalculateSize()
	out.WriteValues(C)