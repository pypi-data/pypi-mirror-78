from setux.core.module import Module


# pylint: disable=arguments-differ


class Distro(Module):
    '''Add User to sudoers

    arg:
        user : user name
    '''

    def deploy(self, target, *, user):

        line = f'{user} ALL=(ALL) NOPASSWD: ALL\n'
        org = target.read('/etc/sudoers')

        if line in org: return True

        sudoers = [
            line
            for line in org.split('\n')
            if user not in line
        ]
        sudoers.append(line)
        target.write('/etc/sudoers', '\n'.join(sudoers))

        ok = line in target.read('/etc/sudoers')

        return ok
