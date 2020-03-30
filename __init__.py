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
