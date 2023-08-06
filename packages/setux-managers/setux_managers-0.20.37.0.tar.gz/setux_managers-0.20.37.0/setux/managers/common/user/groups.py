from setux.logger import debug
from setux.core.manage import ArgsChecker


class Groups(ArgsChecker):
    def get(self):
        ret, out, err = self.run(f'grep {self.key} /etc/group')
        groups = set()
        for line in out:
            name, x, gid, users = line.split(':')
            if self.key in users.split(','):
                groups.add(name)
        return groups

    def add(self, group):
        if group not in  self.get():
            debug(f'groups add {self.key} to {group}')
            self.distro.Group(group).set()
            self.run(f'usermod --append --groups {group} {self.key}')

    def rm(self, group):
        groups = self.get()
        if group in groups:
            groups.remove(group)
            debug(f'groups remove {self.key} from {group}')
            self.run(f'usermod --groups {",".join(groups)} {self.key}')

