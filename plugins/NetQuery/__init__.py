class NetQuery(object):
	"""Non-functional base class for determining if the Internet is available."""
	def __init__(self, cfg):
		super(NetQuery, self).__init__()

	def query(self):
		"""Query if the Internet is available.
		:return: True if the Internet is reachable; False if the Internet is not reachable.
		"""
		raise NotImplementedError("This method needs to be overridden in subclasses.")
