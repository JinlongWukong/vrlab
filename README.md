## README
This tool is primaryly used for parsing VIRL topology file to build its topology using qemu + linux bridge

## How TO USE

usage: loadVIRL.py [-h] -f FILE [-m MANAGEMENT] {show,build,remove,qemu}

-f FILE, must specify the topology file exported from VIRL


-m MANAGEMENT, specify the management bridge to connect all nodes mgmt interfaces


positional arguments: 
	show -> show topology
	build -> build topology
	remove -> remove topolgy
	qemu -> check qemu startup parameter

Example1: build topology
 sudo ./loadVIRL.py -f topology.virl -m mgmt build

Example2: show topology
 sudo ./loadVIRL.py -f topology.virl -m mgmt show

Example3: remove topology
 sudo ./loadVIRL.py -f topology.virl -m mgmt remove
  

