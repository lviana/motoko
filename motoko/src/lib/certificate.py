
import json
import os
import subprocess
import syslog

from Cheetah.Template import Template


class server(object):

    def __init__(self, ca, capriv, datadir, tmpdir='/tmp'):
        self.datadir = datadir
        self.tmpdir = tmpdir
        self.ca = ca
        self.capriv = capriv


    def _getlocal(self, hostname):
        try:
            cert = open('%s/%s/%s_server_certificate.pem' % (self.datadir, hostname, hostname), 'ro')
            key  = open('%s/%s/%s_server_certificate.key' % (self.datadir, hostname, hostname), 'ro')
        except IOError:
            syslog.syslog(syslog.LOG_INFO, '[warn] Certificate files not found. (%s)' % hostname)
            raise RuntimeError('Certificate does not exist')


        pack = {'certificate': cert.read(), 'key': key.read()}

        cert.close()
        key.close()

        return json.dumps(pack)

    def _getnew(self, hostname, template='/etc/motoko/server.tmpl'):
        templatefile = '%s/%s_server_certificate.info' % (self.tmpdir, hostname)
        serverkey    = '%s/%s/%s_server_certificate.key' % (self.datadir, hostname, hostname)
        servercert   = '%s/%s/%s_server_certificate.pem' % (self.datadir, hostname, hostname)

        try:
            os.makedirs('%s/%s' % (self.datadir, hostname))
        except OSError:
            pass

        render = Template(file = template, searchList = [{'hostname': hostname}])
        certTemplate = open(templatefile, 'a')
        certTemplate.write(str(render))
        certTemplate.close()

        try:
            subprocess.call(['/usr/bin/certtool', '--generate-privkey', '--outfile', serverkey])

            subprocess.call(['/usr/bin/certtool', '--generate-certificate',
                                                  '--template', templatefile ,
                                                  '--load-privkey', serverkey,
                                                  '--load-ca-certificate', self.ca,
                                                  '--load-ca-privkey', self.capriv,
                                                  '--outfile', servercert])
        except OSError:
            syslog.syslog(syslog.LOG_ERR, '[error] Problem executing /usr/bin/certtool. Certificate was not generated.')
            raise EnvironmentError('Check package dependencies, certtool not found')

        finally:
            os.remove(templatefile)

        if os.path.isfile(servercert):
            syslog.syslog(syslog.LOG_INFO, '[info] Certificate and private key created (%s)' % hostname)
        else:
            syslog.syslog(syslog.LOG_ERR, ('[error] Certificate could not be created. Command: certtool'
'--generate-certificate --template %s --load-privkey %s'
'--load-ca-certificate %s --load-ca-privkey %s --outfile %s')
% (templatefile,serverkey,self.ca,self.capriv,servercert))

    def get(self, hostname):
        try:
            certs = self._getlocal(hostname)
        except RuntimeError:
            self._getnew(hostname)
        
        certs = self._getlocal(hostname)

        return certs


class client(object):

    def __init__(self, ca, capriv, datadir, tmpdir='/tmp'):
        self.datadir = datadir
        self.tmpdir = tmpdir
        self.ca = ca
        self.capriv = capriv


    def _getlocal(self, hostname):
        try:
            cert = open('%s/%s/%s_client_certificate.pem' % (self.datadir, hostname, hostname), 'ro')
            key  = open('%s/%s/%s_client_certificate.key' % (self.datadir, hostname, hostname), 'ro')
        except IOError:
            syslog.syslog(syslog.LOG_INFO, '[warn] Certificate files not found. (%s)' % hostname)
            raise RuntimeError('Certificate does not exist')


        pack = {'certificate': cert.read(), 'key': key.read()}

        cert.close()
        key.close()

        return json.dumps(pack)

    def _getnew(self, hostname, template='/etc/motoko/client.tmpl'):
        templatefile = '%s/%s_client_certificate.info' % (self.tmpdir, hostname)
        clientkey    = '%s/%s/%s_client_certificate.key' % (self.datadir, hostname, hostname)
        clientcert   = '%s/%s/%s_client_certificate.pem' % (self.datadir, hostname, hostname)

        try:
            os.makedirs('%s/%s' % (self.datadir, hostname))
        except OSError:
            pass

        render = Template(file = template, searchList = [{'hostname': hostname}])
        certTemplate = open(templatefile, 'a')
        certTemplate.write(str(render))
        certTemplate.close()

        try:
            subprocess.call(['/usr/bin/certtool', '--generate-privkey', '--outfile', clientkey])

            subprocess.call(['/usr/bin/certtool', '--generate-certificate',
                                                  '--template', templatefile ,
                                                  '--load-privkey', clientkey,
                                                  '--load-ca-certificate', self.ca,
                                                  '--load-ca-privkey', self.capriv,
                                                  '--outfile', clientcert])
        except OSError:
            syslog.syslog(syslog.LOG_ERR,
                '[error] Problem executing /usr/bin/certtool. Certificate was not generated.')
            raise EnvironmentError('Check package dependencies, certtool not found')

        finally:
            os.remove(templatefile)

        if os.path.isfile(clientcert):
            syslog.syslog(syslog.LOG_INFO, '[info] Client certificate and private key created  (%s)' % hostname)
        else:
            syslog.syslog(syslog.LOG_ERR, ('[error] Client certificate could not be created. Command: certtool'
'--generate-certificate --template %s --load-privkey %s'
'--load-ca-certificate %s --load-ca-privkey %s --outfile %s')
% (templatefile,clientkey,self.ca,self.capriv,clientcert))

    def get(self, hostname):
        try:
            certs = self._getlocal(hostname)
        except RuntimeError:
            self._getnew(hostname)
        
        certs = self._getlocal(hostname)

        return certs
