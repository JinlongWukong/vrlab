#!/usr/bin/python
import vr
import os

addr = [4.1, 4.2, 4.3, 4.4, 4.5, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5, 9.0, 9.1, 9.2, 9.3, 9.4, 9.5, 10.0, 10.1, 10.2, 10.3, 10.4, 10.5, 11.0, 11.1, 11.2, 11.3, 11.4, 11.5, 12.0, 12.1, 12.2, 12.3, 12.4, 12.5, 13.0, 13.1, 13.2, 13.3, 13.4, 13.5, 14.0, 14.1, 14.2, 14.3, 14.4, 14.5]

class n9kv(vr.vm):
    def __init__(self, vm_name, ram, image, nics, nic_type, num):
        self.nic_type = nic_type
        self.nics = nics
        self.name = vm_name
        self.qemu_args = ["qemu-system-x86_64", "-display", "none"]
        self.qemu_args.extend(["-bios", 'bios.bin'])
        self.qemu_args.extend(["-m", str(ram)])
        self.qemu_args.extend(["-name", self.name])
        if os.path.exists("/dev/kvm"):
            self.qemu_args.insert(1, '-enable-kvm')
        self.qemu_args.extend(["-daemonize"])
        self.qemu_args.extend(["-cpu", "host"])
        self.qemu_args.extend(["-smp", "cores=2,threads=1,sockets=1"])
        self.qemu_args.extend(["-device", "ahci,id=ahci0,bus=pci.0"])
        self.qemu_args.extend(["-drive", "if=none,file=%s,id=drive-sata-disk0,format=qcow2" % image])
        self.qemu_args.extend(["-device", "ide-drive,bus=ahci0.0,drive=drive-sata-disk0,id=drive-sata-disk0"])
        self.qemu_args.extend(["-monitor","telnet:0.0.0.0:6%02d0,nowait,server" % num])
        self.qemu_args.extend(["-serial", "telnet:0.0.0.0:6%02d1,nowait,server" % num])
        self.qemu_args.extend(["-netdev", "tap,ifname=%s,id=mgmt1,script=no,downscript=no" % (self.name + "-mgmt1")])
        self.qemu_args.extend(["-device", "vmxnet3,addr=4.0,romfile=,netdev=mgmt1,multifunction=on,mac=%s" % self.fetch_mac(self.name + "-mgmt1")])

    def gen_nics(self):
        res = []
        for i in range(len(self.nics)):
            res.append("-device")
            res.append("%(nic_type)s,addr=%(addr)s,romfile=,netdev=eth_1_%(i)d,multifunction=on,mac=%(mac)s"
                       % {'nic_type': self.nic_type, 'addr': addr[i], 'i': i+1, 'mac': self.fetch_mac(self.name + '-' + str(self.nics[i][0]))})
            res.append("-netdev")
            res.append("tap,id=eth_1_%(i)d,ifname=%(nic)s,script=no,downscript=no"
                       % {'i': i+1,'nic':self.name + '-' + str(self.nics[i][0])})
        return res