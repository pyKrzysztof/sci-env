import wx
from wx.lib.scrolledpanel import ScrolledPanel


class MyFrame(wx.Frame):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		bg_color = 'green'

		# changes the background of the scrollbars
		self.SetBackgroundColour(bg_color)

		sizer = wx.BoxSizer(wx.VERTICAL)

		panel = ScrolledPanel(self)
		panel.SetBackgroundColour(bg_color)
		panel.SetupScrolling(scroll_y=True)

		panelsizer = wx.BoxSizer(wx.VERTICAL)

		for _ in range(4):
			p = wx.Panel(panel, size=(400, 300))
			p.SetBackgroundColour(bg_color)
			panelsizer.Add(p, 0, flag=wx.EXPAND)
			panelsizer.Add((-1, 10))

		panel.SetSizer(panelsizer)

		for child in panel.GetChildren():
			print(type(child)) # there is no scrollbar

		sizer.Add(panel, 1, flag=wx.EXPAND)
		self.SetSizer(sizer)
		self.Layout()


app = wx.App()
frame = MyFrame(parent=None, title='ScrolledPanel', size=(400, 400))
frame.Show()
app.MainLoop()