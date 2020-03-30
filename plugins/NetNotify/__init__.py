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
