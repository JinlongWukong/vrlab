#!/usr/bin/python

import xml.etree.ElementTree as ET
import time
import subprocess
import os
import argparse

from vrlab import vriosxrv
from vrlab import bridge_lib
from vrlab import utils

class Node:
    def __init__(self, name, type, image):
        self.name = name
        self.type = type
        self.image = image
        self.interfaces = []

    def add_interface(self, id, nic):
        self.interfaces.append((id,nic))

    def __str__(self):
        return ('name:' + self.name + ', type:' + self.type + ', image:' + self.image)
'''
class Interface():
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
'''

class Link:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        self.linkName = src['name'][-7:] + dst['name'][-7:]

    def getLinkName(self):
        return self.linkName

    def __str__(self):
        return (self.src['desc'] + ' <------------> ' + self.dst['desc'])

def capture():
    cmd = "tcpdump -i "
    for link in Links:
        if link.src['desc'] in args.option:
            os.system(cmd + link.src['name'])
            return
        elif link.dst['desc'] in args.option:
            os.system(cmd + link.dst['name'])
            return

def loadVirlTopology(file):
    with open(file) as f:
        xml = f.read().replace(' xmlns=', " tobeingore=")
        root = ET.fromstring(xml)
        for child in root.findall('node'):
            #print(child.tag, child.attrib)
            node = Node(child.attrib.get('name'), child.attrib.get('subtype'), child.attrib.get('vmImage',''))
            for grandchild in child.findall('interface'):
                #print(grandchild.tag, grandchild.attrib)
                node.add_interface(grandchild.attrib.get('id'),grandchild.attrib.get('name'))
            Nodes.append(node)
        for child in root.findall('connection'):
            #print(child.tag, child.attrib.get('src'),child.attrib.get('dst'))
            nodeId = child.attrib.get('src').split('/')[2].split(':')[1][5]
            interId = child.attrib.get('src').split('/')[3].split(':')[1][10]
            src={}
            src['name'] = Nodes[int(nodeId)-1].name + "-" + Nodes[int(nodeId)-1].interfaces[int(interId)-1][0]
            src['desc'] = Nodes[int(nodeId)-1].name + "-" + Nodes[int(nodeId)-1].interfaces[int(interId)-1][1]
            nodeId = child.attrib.get('dst').split('/')[2].split(':')[1][5]
            interId = child.attrib.get('dst').split('/')[3].split(':')[1][10]
            dst={}
            dst['name'] = Nodes[int(nodeId)-1].name + "-" + Nodes[int(nodeId)-1].interfaces[int(interId)-1][0]
            dst['desc'] = Nodes[int(nodeId)-1].name + "-" + Nodes[int(nodeId)-1].interfaces[int(interId)-1][1]
            link = Link(src, dst)
            Links.append(link)

def show_topology():
    print("\n...Print all Nodes \n")
    cmd = "bash ./tools_lib.sh kvm"
    cmd = cmd + " '"
    for node in Nodes:
        cmd = cmd + node.name + '\|'
    cmd = cmd[:-2] + "'"
    print(subprocess.check_output(cmd, shell=True))

    print("\n...Print all links \n")
    for link in Links:
        print(link)
    print("\n...All done!")

def remove_topology():
    print("\n...Remove all Nodes \n")
    for node in Nodes:
        cmd = "bash ./tools_lib.sh kill name "
        cmd = cmd + node.name
        try:
            print(subprocess.check_output(cmd, shell=True))
        except:
            pass

    print("\n...Remove all bridges \n")
    for link in Links:
        br = bridge_lib.Bridge(link.getLinkName())
        try:
            br.downbr()
            br.delbr()
        except Exception as e:
           print(e.messages)

    print("\n...All done!")

def qemu_parameter():
    print("\nPrint nodes qemu startup parameters:")
    for i in Nodes:
        print(i.name + ':')
        vr = utils.factory_vr(i.name, i.type, i.image, i.interfaces, Nodes.index(i))
        print(vr)

def build_topology():
    print("...Will start building nodes:")
    for i in Nodes:
        print("\n-> starting node: %s " % i.name)
        vr = utils.factory_vr(i.name, i.type, i.image, i.interfaces, Nodes.index(i))
        if not vr: continue
        vr.start()
        # setup management interface after 2 seconds
        time.sleep(2)
        if bridge_lib.Bridge.is_existed(mgmt_br):
            br = bridge_lib.Bridge(mgmt_br)
            br.addif(vr.name + '-mgmt1')
            br.set_interfaces_updown('up', vr.name + '-mgmt1')

    print("\n...All Nodes build finished \n")
    print("...Will start building Links:")
    for i in Links:
        print("\n-> starting add link: %s" % i.getLinkName())
        br = bridge_lib.Bridge.addbr(i.getLinkName())
        br.addif(i.src['name'])
        br.addif(i.dst['name'])
        br.upbr()
        br.set_interfaces_updown('up')

    print("\n...All Links build finished \n")

## Main
parser = argparse.ArgumentParser(description="Topology tool")
parser.add_argument("-f", "--file",
                    required=True,
                    help="must specify a topology file which exported from VIRL")
parser.add_argument("-m", "--management",
                    help="specify a management bridge to connect nodes mgmt interface")
parser.add_argument('action',
                    choices=['show', 'build', 'remove', 'qemu', 'capture'],
                    help="specify action: build, show, remove, qemu, capture")
parser.add_argument('option', nargs='?',default='',
                    help="option parameters")

args = parser.parse_args()
Nodes = []
Links = []
mgmt_br = 'mgmt'
if args.management:
    mgmt_br = args.management

loadVirlTopology(args.file)

switch = {
    'build' : build_topology,
    'show' : show_topology,
    'remove' : remove_topology,
    'qemu' : qemu_parameter,
    'capture' : capture
}
switch[args.action]()