#!/usr/bin/env python3
import argparse
import configparser
import importlib
import sys

class NetWatcher(object):
	"""docstring for NetWatcher"""
	def __init__(self, query, notify, activate):
		super(NetWatcher, self).__init__()
		if not isinstance(query, NetQuery):
			raise TypeError("The query parameter expects a NetQuery object but got a {t:s}.".format(t=type(query).__name__))
		self.query = query
		if not isinstance(notify, NetNotify):
			raise TypeError("The notify parameter expected a NetNotify object but got a {t:s}.".format(t=type(notify).__name__))
		self.notify = notify
		if not isinstance(activate, NetActivate):
			raise TypeError("The activate parameter expected a NetActivate object but got a {t:s}.".format(t=type(activate).__name__))
		self.activate = activate

class Config(object):
	"""Loads the config from file and deals with the messy stuff."""
	def __init__(self, config_file):
		super(Config, self).__init__()
		cfg = configparser.ConfigParser()
		cfg.read(config_file)
		query_name = cfg.get('setup', 'query plugin')
		try:
			self.query_class = getattr(importlib.import_module('plugins.NetQuery.%s' % query_name), query_name)
		except ModuleNotFoundError as e:
			logger.critical("Not able to find NetQuery plugin %s!" % query_name)
			sys.exit(1)
		notify_name = cfg.get('setup', 'notify plugin')
		try:
			self.notify_class = getattr(importlib.import_module('plugins.NetNotify.%s' % notify_name), notify_name)
		except ModuleNotFoundError as e:
			logger.critical("Not able to find NetNotify plugin %s!" % notify_name)
			sys.exit(1)
		activate_name = cfg.get('setup', 'activate plugin')
		try:
			self.activate_class = getattr(importlib.import_module('plugins.NetActivate.%s' % activate_name), activate_name)
		except ModuleNotFoundError as e:
			logger.critical("Not able to find NetActivate plugin %s!" % activate_name)
			sys.exit(1)
		self.cfg = cfg
