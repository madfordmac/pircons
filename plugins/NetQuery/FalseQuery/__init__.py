from .. import NetQuery

class FalseQuery(NetQuery):
	"""Always unsuccessful query."""
	def __init__(self, cfg):
		super(FalseQuery, self).__init__(cfg)

	def query(self):
		"""Always return offline. Intended for debugging.
		:return: False
		"""
		return False
