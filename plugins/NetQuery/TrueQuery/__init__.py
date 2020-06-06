from .. import NetQuery

class TrueQuery(NetQuery):
	"""Always successful query."""
	def __init__(self, cfg):
		super(TrueQuery, self).__init__()

	def query(self):
		"""Always return online. Intended for debugging.
		:return: True
		"""
		return True
