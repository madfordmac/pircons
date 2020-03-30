from .. import NetNotify

class ConsoleNotify(NetNotify):
	"""Print a line to stdout with the IP to access."""
	def __init__(self):
		super(ConsoleNotify, self).__init__()

	def notify(self, ip):
		"""Print the IP to the console. This is primarily intended for debugging.
		:return: Always returns True.
		"""
		print("Network is down. Access this host at {ip:s}.".format(ip=ip))
		return True