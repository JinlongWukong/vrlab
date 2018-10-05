import os
import subprocess

# NOTE(toabctl): Don't use /sys/devices/virtual/net here because not all tap
# devices are listed here (i.e. when using Xen)
BRIDGE_FS = "/sys/class/net/"
BRIDGE_INTERFACE_FS = BRIDGE_FS + "%(bridge)s/brif/%(interface)s"
BRIDGE_INTERFACES_FS = BRIDGE_FS + "%s/brif/"
BRIDGE_PORT_FS_FOR_DEVICE = BRIDGE_FS + "%s/brport"
BRIDGE_PATH_FOR_DEVICE = BRIDGE_PORT_FS_FOR_DEVICE + '/bridge'

def to_string(cmd):
    command = ''
    for i in cmd:
        command = command + i + ' '
    return command

def is_bridged_interface(interface):
    if not interface:
        return False
    else:
        return os.path.exists(BRIDGE_PORT_FS_FOR_DEVICE % interface)

def get_bridge_names():
    return os.listdir(BRIDGE_FS)

class Bridge():
    def __init__(self, brname, namespace=None):
        self.name = brname
        self.namespace = namespace

    def _brctl(self, cmd):
        cmd = ['brctl'] + cmd
        command = to_string(cmd)
        print(command)
        return subprocess.call(command, shell=True)

    @classmethod
    def addbr(cls, name, namespace=None):
        bridge = cls(name, namespace)
        try:
            bridge._brctl(['addbr', bridge.name])
        except RuntimeError:
            print(RuntimeError.message)

        return bridge

    @staticmethod
    def is_existed(name):
        return os.path.exists(BRIDGE_FS + name)

    def delbr(self):
        return self._brctl(['delbr', self.name])

    def upbr(self):
        return self.set_interfaces_updown('up', self.name)

    def downbr(self):
        return self.set_interfaces_updown('down', self.name)

    def addif(self, interface):
        return self._brctl(['addif', self.name, interface])

    def delif(self, interface):
        return self._brctl(['delif', self.name, interface])

    def setfd(self, fd):
        return self._brctl(['setfd', self.name, str(fd)])

    def disable_stp(self):
        return self._brctl(['stp', self.name, 'off'])

    def owns_interface(self, interface):
        return os.path.exists(
            BRIDGE_INTERFACE_FS % {'bridge': self.name,
                                   'interface': interface})

    def get_interfaces(self):
        try:
            return os.listdir(BRIDGE_INTERFACES_FS % self.name)
        except OSError:
            return []

    def set_interfaces_updown(self, status, interface=None):
        if interface:
            cmd = ['ip link set ' + interface + ' ' + status]
            command = to_string(cmd)
            print(command)
            subprocess.call(command, shell=True)
        else:
            for i in self.get_interfaces():
                cmd = ['ip link set ' + i + ' ' + status]
                command = to_string(cmd)
                print(command)
                subprocess.call(command, shell=True)
        return