from setux.core.module import Module


class Distro(Module):
    '''Write default SSH config
    '''

    def deploy(self, target):

        config = '''
            PermitRootLogin yes
            PasswordAuthentication yes
            ChallengeResponseAuthentication no
            UsePAM yes
            X11Forwarding no
            PrintMotd no
            AcceptEnv LANG LC_*
            ClientAliveInterval 120
        '''

        dst = '/etc/ssh/sshd_config'
        ok = target.write(dst, config)

        return ok
