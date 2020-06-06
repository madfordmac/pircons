from .. import NetQuery
import dns.resolver
import re

class DNSQuery(NetQuery):
	"""Query configured or default DNS servers for a particular record."""
	def __init__(self, cfg):
		super(DNSQuery, self).__init__()
		query, nameservers = None, None
		if cfg.has_section('DNSQuery'):
			if cfg.has_option('DNSQuery', 'record'):
				query = cfg.get('DNSQuery', 'record')
			if cfg.has_option('DNSQuery', 'nameservers'):
				nameservers = re.split(r'[, ;]+', cfg.get('DNSQuery', 'nameservers'))
		self.__query = query or 'www.google.com.'
		self.__resolver = dns.resolver.Resolver()
		self.__resolver.nameservers = namservers or ['1.1.1.1', '1.0.0.1']

	def query(self):
		"""Query the configured nameservers for the configured record.
		:return: True if the record can be retrieved; False on any error.
		"""
		try:
			response = self.__resolver.query(self.__query)
			return True
		except Exception as e:
			return False
