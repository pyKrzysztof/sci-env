import configparser
import datetime
import wx

# local imports
from . import core



class Config:

	"""
	Used as a common config manager thorought the application,
	it uses configparser functionality to load configuration files
	and theme files.
	"""


	def __init__(self):
		self.load_config()
	

	def load_config(self):
		"""Loading global config from ..properties.conf file."""
		
		self._config = core.load_config()
		self.load_theme(self._config['General']['Theme'])


	def load_theme(self, name):
		"""Loading theme from ..themes/ directory."""

		dict_app, dict_widget = core.load_theme(name)
		self._widgetColors = dict_widget
		self._appColors = dict_app
		self._fallback_color = '#ffffff'


	def get_key(self, key):
		"""Returns key from configs' general selection"""

		return self._config['General'][key] 


	def get_color(self, selection, name):
		"""
		Get the color from given selection, which
		can be 'app' or 'widget'. If the color name
		was not found, Config._fallback_color will be returned.
		"""

		try:
			if selection.lower() == 'app':
				color = self._appColors[name]
			elif selection.lower() == 'widget':
				color = self._widgudzetColors[name]
		except KeyError:
			print(datetime.datetime.now().time(), f'  Using fallback color, key {name} was not found.')
			color = self._fallback_color

		return color


	def get_font(self, name):
		"""
		Get the given font, if options are specified, will return
		a tuple of given attributes. Options can be: size, family, style, all.
		
		"""

		font_name = name.title() + ' Font'
		size = self._config[font_name]['Size']
		family = self._config[font_name]['Family']
		weight = self._config[font_name]['Weight']

		if family == 'Modern':
			family = wx.FONTFAMILY_MODERN
		elif family == 'Decorative':
			family = wx.FONTFAMILY_DECORATIVE
		elif family == 'Default':
			family = wx.FONTFAMILY_DEFAULT
		else:
			print(f'Invalid font family \'{family}\', using default family.')
			family = wx.FONTFAMILY_DEFAULT

		if weight == 'Bold':
			weight = wx.FONTWEIGHT_BOLD
		elif weight == 'Normal':
			weight = wx.FONTWEIGHT_NORMAL
		else:
			print(f'Invalid font weight \'{weight}\', using regular font weight.')
			weight = wx.FONTWEIGHT_NORMAL

		return wx.Font(int(size), family, wx.FONTSTYLE_NORMAL, weight)