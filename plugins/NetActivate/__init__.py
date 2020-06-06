class NetActivate(object):
	"""Non-functional base class for (de)activating the secondary connection."""
	def __init__(self, cfg):
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
