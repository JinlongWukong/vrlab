#!/usr/bin/python
import vr

class asav(vr.vm):
    def __init__(self, vm_name, ram, image, nics, nic_type, num):
        super(asav, self).__init__(vm_name, ram, image, nics, nic_type)
        self.qemu_args.extend(["-smp", "cores=2,threads=1,sockets=1"])
        self.qemu_args.extend(["-vnc", "0.0.0.0:2%d" % num])
        self.qemu_args.extend(["-monitor","telnet:0.0.0.0:6%02d0,nowait,server" % num])
        self.qemu_args.extend(["-serial", "telnet:0.0.0.0:6%02d1,nowait,server" % num])
        self.qemu_args.extend(["-netdev", "tap,ifname=%s,id=host1,script=no,downscript=no" % (self.name + "-mgmt1")])
        self.qemu_args.extend(["-device", "virtio-net-pci,romfile=,netdev=host1,id=host1,mac=%s" % self.fetch_mac(self.name + "-mgmt1")])
