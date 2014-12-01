
import syslog
import virtinst.util
import yaml


class vmachine(object):

	def __init__(self):
		templates = self._gettemplates()

	def _gettemplates(self):
		""" Read templates from yaml
		"""
		try:
			stream = open("/etc/motoko/templates.yaml", 'r')
			templates = yaml.load(stream)
			stream.close()

		except IOError:
			syslog.syslog(syslog.LOG_ERR, 'Template file not found, check /etc/motoko/templates.yaml')
		
		return templates

	def generatemac(self):
		""" Generate new mac address for guest machine
		"""
		mac = virtinst.util.randomMAC()

		return mac

	def generateuuid(self):
		""" Generate new uuid for guest machine
		"""
		uuid = virtinst.util.uuidToString(virtinst.util.randomUUID())

		return uuid

	def render(self, template):
		""" Create new virtual machine based on template
		"""
		if type not in self.templates.keys():
			raise ValueError('Template not defined')
