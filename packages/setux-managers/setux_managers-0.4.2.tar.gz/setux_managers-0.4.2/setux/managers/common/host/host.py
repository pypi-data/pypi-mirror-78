from setux.core.manage import Manager


class OS(Manager):
    @property
    def kernel(self):
        ret, out, err = self.run('uname -s')
        return out[0]

    @property
    def version(self):
        ret, out, err = self.run('uname -r')
        return out[0].split('-')[0]

    @property
    def arch(self):
        ret, out, err = self.run('uname -m')
        return out[0]


class Login(Manager):
    @property
    def name(self):
        ret, out, err = self.run('id -un')
        return out[0]

    @property
    def id(self):
        ret, out, err = self.run('id -u')
        return int(out[0])


class Host(Manager):
    @property
    def name(self):
        attr = '_host_name_'
        try:
            val = getattr(self, attr)
        except AttributeError:
            ret, out, err = self.run('hostname')
            val = out[0]
            setattr(self, attr,  val)
        return val

    @name.setter
    def name(self, val):
        attr = '_host_name_'
        delattr(self, attr)
        ret, out, err = self.run(
            'hostname', val.replace('_', '')
        )
        return ret

    @property
    def fqdn(self):
        ret, out, err = self.run('hostname -f')
        return out[0]

    @property
    def addr(self):
        ret, out, err = self.run('curl -s https://api.ipify.org')
        return ret==0 and out[0] or '!'

