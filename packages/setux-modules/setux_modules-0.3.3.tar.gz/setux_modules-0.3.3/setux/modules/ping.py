from setux.core.module import Module


def ping(target, pong='pong'):
    ret, out, err = target.run('echo', pong)
    response = out[0]
    return response==pong


class Distro(Module):
    '''Check Target Reachability
    '''
    def deploy(self, target, **kw):
        return ping(target, pong=kw.get('pong'))


class debian_9(Distro):
    def deploy(self, target, **kw):
        return super().deploy(target, pong='Debian 9')


class debian_10(Distro):
    def deploy(self, target, **kw):
        return super().deploy(target, pong='Debian 10')


class MX_19(Distro):
    def deploy(self, target, **kw):
        return super().deploy(target, pong='MX 19')


class fedora_32(Distro):
    def deploy(self, target, **kw):
        return super().deploy(target, pong='Fedora 32')


class manjaro(Distro):
    def deploy(self, target, **kw):
        return super().deploy(target, pong='Manjaro')

