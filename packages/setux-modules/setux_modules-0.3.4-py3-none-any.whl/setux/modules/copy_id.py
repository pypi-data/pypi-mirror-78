from setux.core.module import Module


class Distro(Module):
    '''Send Public Key to Target
    kw:
        usr : User name
        pub : Piblic key
    '''

    def deploy(self, target, **kw):

        usr = kw['usr']
        pub = kw['pub']

        user = target.User(usr)

        path = f'/home/{usr}/.ssh'
        name = f'authorized_keys'
        full = f'{path}/{name}'

        ok = target.Dir(
            path, mode='700', user=usr, group=user.group.name
        ).deploy()

        if not ok:
            return False

        target.send(pub, full)

        ok = target.File(
            full, mod='600', usr=usr, grp=user.group.name
        ).deploy()

        return ok
