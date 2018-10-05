from vriosxrv import iosxrv
from vrcsr1000v import csr1000v
from vrasav import asav
from vrnxos import n9kv
vrouters = {
    "IOS XRv" : iosxrv,
    "CSR1000v" : csr1000v,
    "ASAv" : asav,
    "NX-OSv" : n9kv
}

def factory_vr(name, type, image, interfaces, num):
    if type == "IOS XRv":
        return vrouters[type](name, 16384, image, interfaces, 'e1000', num)
    elif type == "CSR1000v":
        return vrouters[type](name, 4096, image, interfaces, 'e1000', num)
    elif type == "ASAv":
        return vrouters[type](name, 2048, image, interfaces, 'virtio-net-pci', num)
    elif type == "NX-OSv":
        return vrouters[type](name, 8192, image, interfaces, 'vmxnet3', num)
    else:
        print("Node type not support")
        return None
