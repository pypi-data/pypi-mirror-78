import fabric
from . import commands

class Connection (fabric.Connection):
    def __init__ (self, *args, **kargs):
        super ().__init__ (*args, **kargs)
        self.identify_system ()

    def identify_system (self):
        r = self.run ('uname -a')
        if r.stdout.find ('Ubuntu') != -1:
            self.os = 'ubuntu'
        else:
            self.os = 'centos'

    def install (self, *apps):
        try:
            r = self.sudo ('apt install -y chkrootkit'.format (" ".join (apps)))
        except Exception as e:
            if e.result.return_code != 1:
                print ('  - error: ' + e.result.stderr)
            return False
        return True

    def run (self, cmd, *args, **kargs):
        x = super ().run (cmd, hide = True, *args, **kargs)
        pcmd = cmd.split ()[0]
        try:
            rclass = getattr (commands, pcmd)
        except AttributeError:
            rclass = commands.default

        r = rclass.Result (x.stdout, pcmd)
        x.command = cmd
        x.header = r.header
        x.meta = r.meta
        x.data = r.data
        return x

    def sudo (self, cmd):
        if 'password' in self.connect_kwargs:
            r = self.run ('echo "{}" | sudo -S {}'.format (self.connect_kwargs ['password'], cmd))
        else:
            r = self.run ('sudo {}'.format (cmd))
        return r

def connect (host, user = 'ubuntu', password = None, key_file = None, port = 22):
    if hasattr (host, 'public_dns_name'):
        host = host.public_dns_name
    if key_file:
        return Connection (host, user, port = port, connect_kwargs = dict (key_filename = key_file))
    return Connection (host, user, port = port, connect_kwargs = dict (password = password))
