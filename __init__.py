#!/usr/bin/env python3
from .plugins.NetQuery import NetQuery
from .plugins.NetNotify import NetNotify
from .plugins.NetActivate import NetActivate
import configparser
import importlib
import logging
import sys

class NetWatcher(object):
	"""NetWatcher coordinates a NetQuery, NetNotify, and NetActivate module to 
	monitor connectivity and activate a secondary connection.
	:param query: A NetQuery object to query connectivity
	:param notify: A NetNotify object to notify user of secondary connection's IP
	:param activate: A NetActivate object to activate the secondary connection
	"""

	# Constants
	PRIMARY = 1
	SECONDARY = 2

	def __init__(self, query, notify, activate):
		super(NetWatcher, self).__init__()
		self.__logger = logging.getLogger('pircons.NetWatcher')
		if not isinstance(query, NetQuery):
			raise TypeError("The query parameter expects a NetQuery object but got a {t:s}.".format(t=type(query).__name__))
		self.query = query
		if not isinstance(notify, NetNotify):
			raise TypeError("The notify parameter expected a NetNotify object but got a {t:s}.".format(t=type(notify).__name__))
		self.notify = notify
		if not isinstance(activate, NetActivate):
			raise TypeError("The activate parameter expected a NetActivate object but got a {t:s}.".format(t=type(activate).__name__))
		self.activate = activate
		self.mode = self.PRIMARY
		self.__logger.debug("Created NetWatcher with a %(q)s NetQuery, %(n)s NetNotify and %(a)s NetActivate." % {'q': type(self.query).__name__, 'n': type(self.notify).__name__, 'a': type(self.activate).__name__})

	def poll(self):
		"""Does 1 connection poll. If the connection is down, activate secondary and send alert.
		"""
		if self.mode == self.PRIMARY:
			self.__logger.debug('Mode is PRIMARY. Querying connectivity.')
			if not self.query.query():
				self.__logger.info('Connection is DOWN! Calling activate/notify.')
				self.trip()
		else:
			self.__logger.debug('Mode is SECONDARY. No query until reset.')

	def trip(self):
		self.notify.notify(self.activate.activate())
		self.mode = self.SECONDARY
		self.__logger.debug('Trip complete. Secondary active and notification sent.')

	def reset(self):
		"""Deactivates the secondary connection.
		"""
		self.activate.deactivate()
		self.mode = self.PRIMARY
		self.__logger.info('Reset complete. Back on primary connection.')

class NetConfig(object):
	"""Loads the config from file and deals with the messy stuff."""
	def __init__(self, config_file):
		super(NetConfig, self).__init__()
		self.__logger = logging.getLogger('pircons.NetConfig')
		cfg = configparser.ConfigParser()
		cfg.read(config_file)
		self.__logger.info('Read and parsed config file «%s».' % config_file)
		query_name = cfg.get('setup', 'query plugin')
		try:
			self.query_class = getattr(importlib.import_module('pircons.plugins.NetQuery.%s' % query_name), query_name)
		except ModuleNotFoundError as e:
			logger.critical("Not able to find NetQuery plugin %s!" % query_name)
			raise ValueError("Unable to find configured NetQuery plugin.")
		notify_name = cfg.get('setup', 'notify plugin')
		try:
			self.notify_class = getattr(importlib.import_module('pircons.plugins.NetNotify.%s' % notify_name), notify_name)
		except ModuleNotFoundError as e:
			logger.critical("Not able to find NetNotify plugin %s!" % notify_name)
			raise ValueError("Unable to find configured NetNotify plugin.")
		activate_name = cfg.get('setup', 'activate plugin')
		try:
			self.activate_class = getattr(importlib.import_module('pircons.plugins.NetActivate.%s' % activate_name), activate_name)
		except ModuleNotFoundError as e:
			logger.critical("Not able to find NetActivate plugin %s!" % activate_name)
			raise ValueError("Unable to find configured NetActivate plugin.")
		self.cfg = cfg
