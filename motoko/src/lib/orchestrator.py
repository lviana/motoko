
import redis
import syslog
import virtinst.util


class server(object):

    def __init__(self):
        rserver = redis.Redis('localhost')

    def __generatemac(self):
        """ Generate new mac address (libvirt)
        """
        mac = virtinst.util.randomMAC()

        return mac

    def __generateuuid(self):
        """ Generate new uuid (libvirt)
        """
        uuid = virtinst.util.uuidToString(virtinst.util.randomUUID())

        return uuid

    def create(self, name, attributes):
        """ Create a new server object on redis
        """
        attributes['uuid'] = self.__generateuuid()
        rserver.hmset(name, attributes)

    def getinfo(self, name):
        """ Get server attribute
        """
        serverattrs = rserver.hgetall('pleskl0001')
        return serverattrs

    def list(self, pattern='*'):
        """ List all servers on redis
        """
        serverlist = rserver.keys(pattern)
        return serverlist