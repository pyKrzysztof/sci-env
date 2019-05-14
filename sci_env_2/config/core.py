import configparser
import os




def read_theme(name):
	"""Used to read theme file."""

	theme = configparser.ConfigParser()
	path = os.path.abspath(__file__).replace('config/core.py', 'themes/')
	theme.read(f'{path}{name}.scienv_theme')
	return theme


def get_theme_dicts(theme):
	"""Used to return the dictionaries containing all the needed colors."""

	dict_app, dict_widget = {}, {}
	for key in theme['APP COLORS']:
		dict_app[key] = theme['APP COLORS'][key]
	for key in theme['WIDGET COLORS']:
		dict_widget[key] = theme['WIDGET COLORS'][key]
	return dict_app, dict_widget


def load_theme(name):
	"""Combines read_theme and get_theme_dicts to a single function."""

	theme = read_theme(name)
	dict_app, dict_widget = get_theme_dicts(theme)
	return dict_app, dict_widget


def get_defaults():
	"""Will return an confgparser with default values, 
	independantly from the config file."""

	config = configparser.ConfigParser()
	config['General'] = {'Path': f'{os.path.abspath(__file__).replace("core.py", "")}',
						 'SaveWidgetsOnExit': 'no',
						 'Theme': 'DefaultDark'}
	config['Small Font'] = {'Size': 13, 'Family': 'Modern', 'Weight': 'Normal'}
	config['Medium Font'] = {'Size': 17, 'Family': 'Modern', 'Weight': 'Normal'}
	config['Large Font'] = {'Size': 26, 'Family': 'Modern', 'Weight': 'Bold'}
	return config


def write_config(config):
	"""Writes contents of configparser to properties.conf"""

	with open(config['General']['path'] + 'properties.conf', 'w') as configfile:
		config.write(configfile)


def read_config():
	"""Reads the configuration file."""

	config = configparser.ConfigParser()
	path = os.path.abspath(__file__).replace('core.py', 'properties.conf')
	result = config.read(path)
	if not result:
		print('\'properties.conf\' file does not exist. Getting default values.')
		config = get_defaults()
		write_config(config)
	return config


def load_config():
	"""Processes configparser"""
	return read_config()