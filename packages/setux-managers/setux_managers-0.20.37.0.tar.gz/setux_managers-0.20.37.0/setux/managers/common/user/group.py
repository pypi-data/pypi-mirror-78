from setux.logger import debug
from setux.core.manage import SpecChecker


class Group(SpecChecker):
    def get(self):
        group = self.key if self.key else self.spec['gid']
        ret, out, err = self.run(f'grep ^{group}: /etc/group')
        for line in out:
            name, x, gid, users = line.split(':')
            if self.key:
                if name != self.key: continue
            else:
                if int(gid) != self.spec['gid']: continue
            return dict(
                name = name,
                gid = int(gid),
                users = users.split(','),
            )

    @property
    def name(self):
        return self.get()['name']

    @property
    def gid(self):
        return self.get()['gid']

    def cre(self):
        debug(f'group create {self.key}')
        self.run(f'groupadd {self.key}')

    def mod(self, key, val):
        debug(f'group {self.key} change {key} -> {val}')
        self.run(f'groupmod --{key} {val} {self.key}')

    def rm(self):
        debug(f'group delete {self.key}')
        self.run(f'groupdel {self.key}')

