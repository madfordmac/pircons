#!/usr/bin/env python3
import socket
import argparse
import sys

class NetWatcher(object):
	"""docstring for NetWatcher"""
	def __init__(self, notify, activate):
		super(NetWatcher, self).__init__()
		if not isinstance(notify, NetNotify):
			raise TypeError("The notify parameter expected a NetNotify object but got a {t:s}.".format(t=type(notify).__name__))
		self.notify = notify
		if not isinstance(activate, NetActivate):
			raise TypeError("The activate parameter expected a NetActivate object but got a {t:s}.".format(t=type(activate).__name__))
		self.activate = activate

class NetNotify(object):
	"""docstring for NetNotify"""
	def __init__(self):
		super(NetNotify, self).__init__()
		
	def notify(self, ip):
		print("Network is down. Remote access via {ip:s}.".format(ip=ip), file=sys.stderr)

class NetActivate(object):
	"""docstring for NetActivate"""
	def __init__(self):
		super(NetActivate, self).__init__()
	
	def activate(self):
		return socket.gethostbyname('localhost')