from .. import NetQuery
import dns.resolver

class DNSQuery(NetQuery):
	"""Query configured or default DNS servers for a particular record."""
	def __init__(self):
		super(DNSQuery, self).__init__()
		# TODO: update this to use a global config file.
		self.__query = 'ford-web.net.'
		self.__resolver = dns.resolver.Resolver()
		self.__resolver.nameservers = ['216.40.47.26', '64.98.148.13']

	def query(self):
		"""Query the configured nameservers for the configured record.
		:return: True if the record can be retrieved; False on any error.
		"""
		try:
			response = self.__resolver.query(self.__query)
			return True
		except Exception as e:
			return False
