from .. import NetActivate

class DummyActivate(NetActivate):
	"""Debugging activation module. Prints things to the console, but doesn't actually do anything"""
	def __init__(self):
		super(DummyActivate, self).__init__()

	def activate(self):
		"""Print a line to the console and return localhost
		:return: IPv4 localhost
		"""
		print("We would activate the secondary network interface here.")
		return '127.0.0.1'

	def deactivate(self):
		"""Print a line to the console and return.
		:return: True
		"""
		print("We would deactivate the secondary network interface here.")
		return True
