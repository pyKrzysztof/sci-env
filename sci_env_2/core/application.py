import wx

from .frame import SciFrame


class Application(wx.App):


	def start(self, debug_mode=False):
		if debug_mode:
			from wx.lib.inspection import InspectionTool
			InspectionTool().Show()

		frame = SciFrame(None, title='SciEnv', size=(1075, 650))
		frame.Show()