from setux.logger import debug
from setux.core.manage import SpecChecker


class User(SpecChecker):
    def get(self):
        user = self.key if self.key else self.spec['uid']
        ret, out, err = self.run(f'grep ^{user}: /etc/passwd')
        for line in out:
            name, x, uid, gid, rem, home, shell = line.split(':')
            if self.key:
                if name != self.key: continue
            else:
                if int(uid) != self.spec['uid']: continue
            return dict(
                name = name,
                uid = int(uid),
                gid = int(gid),
                home = home,
                shell = shell,
            )

    @property
    def group(self):
        return self.target.Group(
            self.key,
            gid = self.spec.get('gid')
        )

    @property
    def home(self):
        spec = self.get()
        home = self.target.Dir(
            spec['home'],
            user = spec['name'],
            group = self.group.name,
        )
        return home

    def cre(self):
        debug(f'user create {self.key}')
        self.run(f'useradd {self.key}')
        self.home.set()

    def chk(self, name, value, spec):
        if name=='home':
            return self.home.check()
        return value == spec

    def mod(self, key, val):
        debug(f'user {self.key} change {key} -> {val}')
        if key=='gid':
            self.distro.Group(self.key, gid=val).set()
        if key=='home':
            self.home.set()
        self.run(f'usermod --{key} {val} {self.key}')

    def rm(self):
        debug(f'user delete {self.key}')
        self.run(f'userdel -r {self.key}')
