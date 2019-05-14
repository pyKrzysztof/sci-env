from .scipanel import SciPanel


class WindowManager:


	def __init__(self, frame, config):
		self.frame = frame
		self.config = config


	def init_windows(self):
		"""Initializes the SciPanels, buttons panel, and displays them."""

		self.panels = [SciPanel(self.frame, idx, self.config) for idx in range(0, 6)]
		self.menu_open = False
		self.current = None