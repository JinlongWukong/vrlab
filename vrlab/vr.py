#!/usr/bin/python

import os
import subprocess
import bridge_lib

class vm(object):
    def __init__(self, vm_name, ram, image, nics, nic_type):
        self.nic_type = nic_type
        self.nics = nics
        self.name = vm_name
        self.qemu_args = ["qemu-system-x86_64", "-display", "none"]
        self.qemu_args.extend(["-m", str(ram)])
        self.qemu_args.extend(["-drive", "if=virtio,file=%s,media=disk,index=1" % image])
        self.qemu_args.extend(["-name", self.name])
        if os.path.exists("/dev/kvm"):
            self.qemu_args.insert(1, '-enable-kvm')
        self.qemu_args.extend(["-daemonize"])
        self.qemu_args.extend(["-cpu", "host"])

    def gen_nics(self):
        res = []
        for i in range(len(self.nics)):
            res.append("-device")
            res.append("%(nic_type)s,netdev=p%(i)02d,mac=%(mac)s"
                       % {'nic_type': self.nic_type, 'i': i, 'mac': self.fetch_mac(self.name + '-' + str(self.nics[i][0]))})
            res.append("-netdev")
            res.append("tap,id=p%(i)02d,ifname=%(nic)s,script=no,downscript=no"
                       % {'i': i, 'nic':self.name + '-' + str(self.nics[i][0])})
        return res

    def start(self):
        self.qemu_args.extend(self.gen_nics())
        cmd = self.qemu_args
        self.p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, universal_newlines=True)
        try:
            stdouts, stderrs = self.p.communicate()
            if stdouts or stderrs:
                print(stdouts + '\n' + stderrs)
        except:
            pass

    def stop(self):
        try:
            self.p.terminate()
        except:
            return

        try:
            self.p.communicate()
        except:
            try:
                self.p.kill()
                self.p.communicate()
            except:
                # just assume it's dead or will die?
                self.p.wait()

    def fetch_mac(self, src):
        cmd = "echo '%s'|md5sum|sed " % src + "'s/^\(..\)\(..\)\(..\)\(..\)\(..\).*$/02:\\1:\\2:\\3:\\4:\\5/'"
        return subprocess.check_output(cmd, shell=True).rstrip()

    def __str__(self):
        return bridge_lib.to_string(self.qemu_args)
