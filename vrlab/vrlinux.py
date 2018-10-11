#!/usr/bin/python
import vr
import os

class linux(vr.vm):
    def __init__(self, vm_name, ram, image, nics, nic_type, num):
        self.nic_type = nic_type
        self.nics = nics
        self.name = vm_name
        self.qemu_args = ["qemu-system-x86_64"]
        self.qemu_args.extend(["-m", str(ram)])
        self.qemu_args.extend(["-name", self.name])
        if os.path.exists("/dev/kvm"):
            self.qemu_args.insert(1, '-enable-kvm')
        self.qemu_args.extend(["-daemonize"])
        self.qemu_args.extend(["-cpu", "host"])
        self.qemu_args.extend(["-smp", "cores=2,threads=1,sockets=1"])
        self.qemu_args.extend(["-drive", "if=virtio,media=disk,index=1,file=%s" % image])
        self.qemu_args.extend(["-boot", "once=c"])
        self.qemu_args.extend(["-vnc", "0.0.0.0:2%d" % num])
        self.qemu_args.extend(["-netdev", "tap,ifname=%s,id=host1,script=no,downscript=no" % (self.name + "-mgmt1")])
        self.qemu_args.extend(["-device", "virtio-net-pci,romfile=,netdev=host1,id=host1,mac=%s" % self.fetch_mac(self.name + "-mgmt1")])
