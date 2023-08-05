from setux.core.distro import Distro
from setux.managers.system.package.apt import Apt
from setux.managers.system.service.systemd import SystemD


class Debian(Distro):
    Package = Apt
    Service = SystemD
    pkgmap = dict(
        pip = 'python3-pip',
        sqlite = 'sqlite3',
        p7zip = 'p7zip-full',
        xz = 'xz-utils',
        ctag = 'exuberant-ctags',
    )
    svcmap = dict(
    )

    @classmethod
    def release_name(cls, infos):
        did = infos['ID'].strip()
        ver = infos['VERSION_ID'].strip('\r"')
        return f'{did}_{ver}'


class debian_9(Debian):
    pass


class debian_10(Debian):
    pass
