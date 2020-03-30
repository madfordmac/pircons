#!/usr/bin/env python3
import argparse
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

class NetQuery(object):
	"""Non-functional base class for determining if the Internet is available."""
	def __init__(self):
		super(NetQuery, self).__init__()

	def query(self):
		"""Query if the Internet is available.
		:return: True if the Internet is reachable; False if the Internet is not reachable.
		"""
		raise NotImplementedError("This method needs to be overridden in subclasses.")

class NetNotify(object):
	"""Non-functional base class for notifying user that the Internet is down and the IP where the host can be reached."""
	def __init__(self):
		super(NetNotify, self).__init__()
		
	def notify(self, ip):
		"""Notify the user that the Internet is down.
		:param ip: The IP to send the user for accessing the host.
		:return: True on successful notification; False on failure to notify.
		"""
		raise NotImplementedError("This method needs to be overridden in subclasses.")

class NetActivate(object):
	"""Non-functional base class for (de)activating the secondary connection."""
	def __init__(self):
		super(NetActivate, self).__init__()
	
	def activate(self):
		"""Activate the secondary connection.
		:return: The public IP address of the activated connection.
		"""
		raise NotImplementedError("This method needs to be overridden in subclasses.")

	def deactivate(self):
		"""Deactivate the secondary connection.
		"""
		raise NotImplementedError("This method needs to be overridden in subclasses.")
