from setux.core.module import Module


class Distro(Module):
    '''Write Prod SSH Config
    '''

    def deploy(self, target):

        config = '''
            PermitRootLogin no
            PasswordAuthentication no
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
