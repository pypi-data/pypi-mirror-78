import sys, os
import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from bossman.logging import logger

py3 = sys.version_info[0] >= 3
if py3:
	from configparser import ConfigParser
	from urllib import parse
else:
	import ConfigParser
	# pylint: disable=import-error
	import urlparse as parse

class Session(requests.Session):
	def __init__(self, edgerc, section, **kwargs):
		super(Session, self).__init__(**kwargs)
		self.edgerc = EdgeRc(edgerc)
		self.section = section
		self.auth = EdgeGridAuth(
			client_token=self.edgerc.get(section, "client_token"),
			client_secret=self.edgerc.get(section, "client_secret"),
			access_token=self.edgerc.get(section, "access_token"),
		)

	def request(self, method, url, **kwargs):
		baseUrl = "https://{host}".format(host=self.edgerc.get(self.section, "host"))
		url = parse.urljoin(baseUrl, url)
		return super(Session, self).request(method, url, **kwargs)
