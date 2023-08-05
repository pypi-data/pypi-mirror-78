from tempfile import NamedTemporaryFile
from os.path import isdir, basename
import sys

from setux.core.target import Target
from . import logger, info
from . import remote_tpl


# pylint: disable=arguments-differ


class SSH(Target):
    def __init__(self, **kw):
        self.host = kw.pop('host', None)
        self.user = kw.pop('user', 'root')
        self.priv = kw.pop('priv', None)
        kw['name'] = kw.pop('name', self.host)
        super().__init__(**kw)

    def skip(self, line):
        if (
            line.startswith('Connection to')
            and line.endswith('closed.')
        ): return True
        return False

    def run(self, *arg, **kw):
        arg, kw = self.parse(*arg, **kw)
        cmd = ['ssh']
        if self.priv: cmd.extend(['-i', self.priv])
        cmd.append(f'{self.user}@{self.host}')
        cmd.append('-t')
        cmd.extend(arg)
        kw['skip'] = self.skip
        ret, out, err =  super().run(*cmd, **kw)
        self.trace(' '.join(arg), ret, out, err, **kw)
        return ret, out, err

    def __call__(self, command, **kw):
        ret, out, err = self.run(f'"{command}"', **kw)
        print('\n'.join(out))
        return ret

    def chk_cnx(self):
        ret, out, err = self.run('uname', report='quiet')
        if ret != 0:
            key = f'-i {self.priv} ' if self.priv else ''
            msg = [
                f' {self.name} ! connection error !',
                f'ssh {key}{self.user}@{self.host}\n',
            ]
            raise Exception('\n'.join(msg))

    def scp(self, *arg, **kw):
        arg, kw = self.parse(*arg, **kw)
        cmd = ['scp']
        if self.priv: cmd.extend(['-i', self.priv])
        cmd.extend(arg)
        ret, out, err =  super().run(*cmd, **kw)
        self.trace('scp '+' '.join(arg), ret, out, err, **kw)
        return ret, out, err

    def send(self, local, remote=None, quiet=False):
        if not remote: remote = local
        if not quiet: info(f'\tsend {local} -> {remote}')
        dest = remote[:remote.rfind('/')]
        self.run(f'mkdir -p {dest}', report='quiet')
        self.scp(f'{local} {self.user}@{self.host}:{remote}')

    def fetch(self, remote, local, quiet=False):
        if not quiet: info(f'\tfetch {local} <- {remote}')
        self.scp(f'{self.user}@{self.host}:{remote} {local}')

    def rsync_opt(self):
        if self.priv:
            return f'-e "ssh -i {self.priv}"'
        else:
            return '-e ssh'

    def sync(self, src, dst=None):
        assert isdir(src), f'\n ! sync reqires a dir ! {src} !\n'
        if not src.endswith('/'): src+='/'
        if not dst: dst = src
        self.Dir(dst[:-1]).set()
        info(f'\tsync {src} -> {dst}')
        return self.rsync(f'{src} {self.user}@{self.host}:{dst}')

    def read(self, path, mode='rt', critical=True, report='normal'):
        if report=='normal':
            info(f'\tread {path}')
        with NamedTemporaryFile(mode=mode) as tmp:
            self.fetch(path, tmp.name, quiet=True)
            content = tmp.read()
        return content

    def write(self, path, content, mode='wt', report='normal'):
        if report=='normal':
            info(f'\twrite {path}')
        dest = path[:path.rfind('/')]
        self.run(f'mkdir -p {dest}', report=report)
        with NamedTemporaryFile(mode=mode) as tmp:
            tmp.write(content)
            tmp.flush()
            self.send(tmp.name, path, quiet=True)
        return self.read(path, mode=mode.replace('w','r'), report='quiet') == content

    def export(self, name, root):
        info(f'\texport {name} -> {root}')
        cls = self.modules.items[name]
        mod = cls(self.distro)
        for module in mod.submodules:
            self.export(module, root)
        full = sys.modules[cls.__module__].__file__
        name = basename(full)
        self.send(
            full,
            f'{root}/setux/modules/{name}',
        )

    def remote(self, module, export_path=None, **kw):
        with logger.quiet():
            self.Pip.install('setux')
            path = export_path or '/tmp/setux/import'
            name = 'exported.py'
            self.export(module, path)
            kwargs = ', '+', '.join(f"{k}='{v}'" for k,v in kw.items()) if kw else ''
            self.write('/'.join((path, name)), remote_tpl.deploy.format(**locals()))
            ret, out, err = self.script(remote_tpl.script.format(**locals()))
        info('\t'+'\n\t'.join(out))
        return ret, out, err

    def __str__(self):
        return f'SSH({self.name} : {self.user}@{self.host})'
