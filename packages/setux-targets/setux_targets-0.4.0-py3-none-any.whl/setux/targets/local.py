from shutil import copy
from os.path import isdir

from setux.core.target import Target
from . import error, info


# pylint: disable=arguments-differ


class Local(Target):
    def __init__(self, **kw):
        kw['name'] = kw.get('name', 'local')
        super().__init__(**kw)

    def run(self, *arg, **kw):
        arg, kw = self.parse(*arg, **kw)
        ret, out, err =  super().run(*arg, **kw)
        self.trace(' '.join(arg), ret, out, err, **kw)
        return ret, out, err

    def __call__(self, command, **kw):
        ret, out, err = self.run(command, **kw)
        print('\n'.join(out))
        print('\n'.join(err))
        return ret

    def read(self, path, mode='rt', critical=True, report='normal'):
        if report=='normal':
            info(f'\tread {path}')
        return open(path, mode).read()

    def write(self, path, content, mode='wt', report='normal'):
        if report=='normal':
            info(f'\twrite {path}')
        dest = path[:path.rfind('/')]
        self.run(f'mkdir -p {dest}', report=report)
        with open(path, mode) as out:
            out.write(content)
        return open(path, mode=mode.replace('w','r')).read() == content

    def send(self, local, remote, quiet=False):
        info(f'\tsend {local} -> {remote}')
        copy(local, remote)

    def fetch(self, remote, local):
        info(f'\tfetch {local} <- {remote}')
        copy(remote, local)

    def sync(self, src, dst=None):
        assert isdir(src)
        if not src.endswith('/'): src+='/'
        assert dst
        self.Dir(dst).set()
        info(f'\tsync {src} -> {dst}')
        return self.rsync(f'{src} {dst}')

    def export(self, path):
        error("can't export on local")

    def remote(self, module, export_path=None, **kw):
        error("can't remote on local")

    def __str__(self):
        return f'Local({self.name})'
