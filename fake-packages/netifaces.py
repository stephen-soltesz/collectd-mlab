"""A fake minimal version of netifaces module."""

AF_INET = 2
AF_LINK = 17


def interfaces(self):  # pragma: no cover
    return ['lo', 'eth0']


def ifaddresses(self, iface):  # pragma: no cover
    return {AF_LINK: [{'addr': '00:11:22:33:44:55'}]}
