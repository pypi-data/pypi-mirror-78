from setux.core.module import Module
from setux.logger import error


class Distro(Module):
    '''Download File

    kw:
        url : File's URL
        dst : File's Dest (defaults to "downloaded"
    '''

    def deploy(self, target, **kw):
        url, dst = kw['url'], kw.get('dst')
        dst = dst or 'downloaded'
        try:
            ret, out, err = target.run(f'http --download {url} -o {dst}')
            if ret!=0:
                raise RuntimeError
        except:
            try:
                ret, out, err = target.run(f'curl -sfL {url} -o {dst}')
                if ret!=0:
                    raise RuntimeError
            except:
                try:
                    ret, out, err = target.run(f'wget -q {url} -O {dst}')
                    if ret!=0:
                        raise RuntimeError
                except:
                    target.Pip.install('httpie')
                    ret, out, err = target.run(f'http --download {url} -o {dst}')
                    if ret!=0:
                        msg = err[0]
                        error(msg)
                        raise RuntimeError(msg)
        target(f'ls -l {dst}')
        return True

