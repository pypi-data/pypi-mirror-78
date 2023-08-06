from pybrary.ascii import oct_mod

from setux.logger import debug, error
from setux.core.manage import SpecChecker


class File(SpecChecker):
    def get(self):
        ret, out, err = self.run(f'ls -l --color=never {self.key}')
        try:
            mod, ln, usr, grp, size, month, day, time, path = out[0].split()
            typ, mod = mod[0], mod[1:10]
            assert typ=='-', f'FILE {self.key} : {typ} !'
            return dict(
                name = path,
                mod = oct_mod(mod),
                usr = usr,
                grp = grp,
                size = int(size),
            )
        except Exception as x:
            error('file %s !\n%s : %s', self.key, type(x), x)

    def __str__(self):
        data = self.get()
        if data:
            return f'File {self.key} {data["size"]} {data["mod"]} {data["usr"]}:{data["grp"]}'
        else:
            return f'File {self.key} not found'

    def cre(self):
        debug(f'file create {self.key}')
        self.run(f'touch {self.key}')

    def mod(self, key, val):
        debug(f'file {self.key} change {key} -> {val}')
        if key=='mod':
            self.run(f'chmod {val} {self.key}')
        elif key=='usr':
            self.run(f'chown {val} {self.key}')
        elif key=='grp':
            usr = self.spec["usr"]
            self.run(f'chown {usr}:{val} {self.key}')

    def rm(self):
        debug(f'file delete {self.key}')
        self.run(f'rm {self.key}')

    @property
    def size(self):
        return self.get().get('size')

    def read(self):
        content = self.target.read(self.key)
        assert self.size==len(content), f'\n size ! {self.size} ! {len(content)} !'
        return content

    def write(self, content):
        self.target.write(self.key, content)
        assert self.size==len(content), f'\n size ! {self.size} ! {len(content)} !'

    @property
    def hash(self):
        if self.get():
            debug(f'file hash {self.key}')
            ret, out, err = self.run(f'md5sum {self.key}')
            return out[0].split()[0]

