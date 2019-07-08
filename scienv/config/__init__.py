import configparser
import datetime
import wx
import os

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
        """Loading global config from properties.conf file."""

        self._config = core.load_config()
        self.load_theme(self._config['General']['Theme'])

    def write_config(self):
        """Writes config to properties.conf file."""

        core.write_config(self._config)
        self.load_theme(self._config['General']['Theme'])

    def load_theme(self, name):
        """Loading theme from ..themes/ directory."""

        dict_app, dict_widget = core.load_theme(name)
        self._widget_colors = dict_widget
        self._app_colors = dict_app
        self._fallback_color = '#ffffff'

    def get_key(self, key):
        """Returns key from configs' general selection"""

        return self._config['General'][key]

    def get_color(self, name, selection='app'):
        """
        Get the color from given selection, which
        can be 'app' or 'widget'. If the color name
        was not found, Config._fallback_color will be returned.
        """

        try:
            if selection.lower() == 'app':
                color = self._app_colors[name]
            elif selection.lower() == 'widget':
                color = self._widget_colors[name]
        except KeyError:
            print(datetime.datetime.now().time(),
                  f'  Using fallback color, key {name} was not found.')
            color = self._fallback_color

        return color

    def get_font(self, name):
        """Get the given font, can be 'small', 'medium' or 'large'."""

        font_name = name.title() + ' Font'
        size = int(self._config[font_name]['Size'])
        family = int(self._config[font_name]['Family'])
        weight = int(self._config[font_name]['Weight'])
        return wx.Font(size, family=family, style=wx.FONTSTYLE_NORMAL, weight=weight)

    def set_font(self, font, size, family, style, weight):
        self._config[font]['Size'] = str(size)
        self._config[font]['Family'] = str(family)
        self._config[font]['Style'] = str(style)
        self._config[font]['Weight'] = str(weight)

    def get_current_theme(self):
        """Returns currently set theme."""

        return self._config['General']['Theme']

    def get_theme_list(self):
        """Returns a list of all avaible themes."""
        themes = [theme.replace('.scienv_theme', '') for theme in os.listdir(
            self._config['General']['themes_path'])]
        return themes

    def set_theme(self, theme):
        """Sets the theme."""

        self._config['General']['Theme'] = theme
        self.load_theme(theme)
        core.write_config(self)

    @property
    def save_widgets_on_exit(self):
    	return self._config.getboolean('General', 'savewidgetsonexit')

    @save_widgets_on_exit.setter
    def save_widgets_on_exit(self, value):
    	self._config.set('General', 'savewidgetsonexit', value)