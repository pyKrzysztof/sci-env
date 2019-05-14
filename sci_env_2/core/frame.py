import wx

from .. import config

from .manager import WindowManager



class SciFrame(wx.Frame):


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.SetMinClientSize(self.GetClientSize())
		self.start()


	def set_config(self, config):
		self.config = config


	def start(self):
		self.set_config(config.Config())
		self.window_manager = WindowManager(self, self.config)

		sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(sizer)
		self.Layout()

		self.window_manager.init_windows()