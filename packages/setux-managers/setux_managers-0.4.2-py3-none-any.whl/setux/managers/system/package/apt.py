from pybrary.ascii import rm_ansi_codes

from setux.logger import error, debug
from setux.core.package import Packager


class Apt(Packager):

    def do_init(self):
        self.do_cleanup()
        self.do_update()

    def do_installed(self):
        ret, out, err = self.run('apt list --installed', report='quiet')
        decolor = rm_ansi_codes
        for line in out:
            name, ver, *_ = line.split()
            name = decolor(name.split('/')[0])
            yield name, ver

    def do_bigs(self):
        ret, out, err = self.target.script('''
            #!/bin/bash
            dpkg-query -Wf '${Installed-Size;9} ${Package}\n' | sort -n | tail -n 22
        ''', report='quiet')
        for line in out:
            yield line

    def do_upgradable(self):
        ret, out, err = self.run('''
            apt list --upgradable
        ''', report='quiet')
        decolor = rm_ansi_codes
        for line in out:
            if not line.strip(): continue
            try:
                line = decolor(line)
                name_ver = line.split()[0]
                name, ver = name_ver.split('/')
                yield name, ver
            except:
                debug(line)

    def do_available(self):
        ret, out, err = self.run('apt list', report='quiet')
        decolor = rm_ansi_codes
        for line in out:
            if '[install' not in line:
                name, ver, *_ = line.split()
                name = decolor(name.split('/')[0])
                yield name, ver

    def do_remove(self, pkg):
        self.run(f'apt-get -y purge {pkg}')

    def do_cleanup(self):
        self.run('apt autoremove -y')

    def do_update(self):
        self.run('apt-get update')

    def do_upgrade(self):
        self.run('apt-get upgrade -y')

    def do_install(self, pkg, ver=None):
        ret, out, err = self.run('apt-get -y install %s%s' % (pkg, '=%s'%ver if ver else ''))
        err = [
            x
            for x in err
            if (
                x.strip()
                and not x.startswith('Extracting templates')
                and x != 'Connection to xyz closed.'
            )
        ]
        if err: error('\n'.join(err))
