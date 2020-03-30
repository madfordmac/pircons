from .. import NetQuery

class FalseQuery(NetQuery):
	"""Always unsuccessful query."""
	def __init__(self):
		super(FalseQuery, self).__init__()

	def query(self):
		"""Always return offline. Intended for debugging.
		:return: False
		"""
		return False
