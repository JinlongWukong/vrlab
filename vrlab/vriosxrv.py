#!/usr/bin/python

import vr

class iosxrv(vr.vm):
    def __init__(self, vm_name, ram, image, nics, nic_type, num):
        super(iosxrv, self).__init__(vm_name, ram, image, nics, nic_type)
        self.qemu_args.extend(["-smp", "cores=8,threads=1,sockets=1"])
        self.qemu_args.extend(["-rtc", "base=utc"])
        self.qemu_args.extend(["-monitor","telnet:0.0.0.0:6%02d0,nowait,server" % num])
        self.qemu_args.extend(["-serial", "telnet:0.0.0.0:6%02d1,nowait,server" % num])
        self.qemu_args.extend(["-serial", "telnet:0.0.0.0:6%02d2,nowait,server" % num])
        self.qemu_args.extend(["-serial", "telnet:0.0.0.0:6%02d3,nowait,server" % num])
        self.qemu_args.extend(["-netdev", "tap,ifname=%s,id=host1,script=no,downscript=no" % (self.name + "-mgmt1")])
        self.qemu_args.extend(["-device", "virtio-net-pci,romfile=,netdev=host1,id=host1,mac=%s" % self.fetch_mac(self.name + "-mgmt1")])
        self.qemu_args.extend(["-netdev", "tap,ifname=%s,id=host2,script=no,downscript=no" % (self.name + "-mgmt2")])
        self.qemu_args.extend(["-device", "virtio-net-pci,romfile=,netdev=host2,id=host2,mac=%s" % self.fetch_mac(self.name + "-mgmt2")])
        self.qemu_args.extend(["-netdev", "tap,ifname=%s,id=host3,script=no,downscript=no" % (self.name + "-mgmt3")])
        self.qemu_args.extend(["-device", "virtio-net-pci,romfile=,netdev=host3,id=host3,mac=%s" % self.fetch_mac(self.name + "-mgmt3")])
