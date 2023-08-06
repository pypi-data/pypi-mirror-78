from pybrary.ascii import oct_mod

from setux.logger import debug
from setux.core.manage import SpecChecker


class Dir(SpecChecker):
    def get(self):
        ret, out, err = self.run(f'ls -ld --color=never {self.key}')
        try:
            mod, ln, usr, grp, size, month, day, time, path = out[0].split()
            typ, mod = mod[0], mod[1:10]
            assert typ=='d', f'DIR {self.key} : {typ} !'
            return dict(
                name = path,
                mode = oct_mod(mod),
                user = usr,
                group = grp,
            )
        except Exception as x:
            debug('dir %s !\n%s : %s', self.key, type(x), x)

    def __str__(self):
        data = self.get()
        if data:
            return f'Dir {self.key} {data["mod"]} {data["usr"]}:{data["grp"]}'
        else:
            return f'Dir {self.key} not found'

    def cre(self):
        debug(f'dir create {self.key}')
        self.run(f'mkdir -pv {self.key}')

    def mod(self, key, val):
        debug(f'dir {self.key} change {key} -> {val}')
        if key=='mode':
            self.run(f'chmod -R {val} {self.key}')
        elif key=='user':
            self.run(f'chown -R {val} {self.key}')
        elif key=='group':
            user = self.spec["user"]
            self.run(f'chown -R {user}:{val} {self.key}')
        else:
            raise KeyError(f' ! {key} !')

    def rm(self):
        debug(f'dir delete {self.key}')
        self.run(f'rm -rf {self.key}')
