#import uuid

class Op():
    EQ = '='
    LT = '<'
    LE = '<='
    GT = '>'
    GE = '>='
    CHOICE = '?'
    SELECT = '[]'

class ConstraintGenerator():
    def __init__(self, name):
        self.name = name

    def __lt__(self, spec):
        return Constraint(self.name, value=spec, op=Op.LT)

    def __le__(self, spec):
        return Constraint(self.name, value=spec, op=Op.LE)

    def __eq__(self, spec):
        return Constraint(self.name, value=spec, op=Op.EQ)

    def __ne__(self, spec):
        return Constraint(self.name, value=spec, op=Op.NE)

    def __gt__(self, spec):
        return Constraint(self.name, value=spec, op=Op.GT)

    def __ge__(self, spec):
        return Constraint(self.name, value=spec, op=Op.GE)

class Constraint():
    def __init__(self, name, value=None, op=None):
        self.name = name
        self.value = value
        self.op = op

    def xir(self):
        return {
            'value__': self.value,
            'constraint__': self.op
        }

__xp = {}
def experiment(topo):
    global __xp
    __xp['topo'] = topo


class Topology():
    """A topology contains devices interconnected by networks. Topologies must
    be given a name.
    """
    def __init__(self, name, *args):
        self.name = name
        self.devices = []
        self.nets = []
        self.topos = []
        self.spec = args

    def connect(self, nodes, *args):

        endpoints = []
        for x in nodes:
            if isinstance(x, str):
                n = self.__getitem__(x)
                if n is None:
                    continue
                endpoints.append(EndpointRef(n.endpoint()))
            else:
                endpoints.append(EndpointRef(x.endpoint()))

        #endpoints = [x.endpoint() for x in nodes]
        net = Network(endpoints, *args)
        self.nets.append(net)
        return net

    def device(self, name, *args):
        d = Device(name, *args)
        self.devices.append(d)
        return d

    def xir(self):
        props = {}
        props['name'] = self.name
        for x in self.spec:
            props[x.name] = x.xir()
        return {
            'id': self.name,
            'nodes': list(map(lambda x: x.xir(), self.devices)),
            'links': list(map(lambda x: x.xir(), self.nets)),
            'props': props,
        }

    def __getitem__(self, key):

        if isinstance(key, str):
            for x in self.devices:
                if x.name == key:
                    return x
            return None

        if isinstance(key, tuple):
            res = []
            for x in self.devices:
                if x.name in key:
                    res.append(x)
            return res

        return None



class Device():
    def __init__(self, name, *args):
        self.name = name
        self.spec = args
        self.endpoints = []
        self.mounts = []
        self.props = {}

    def endpoint(self):
        e = Endpoint()
        e.device = self
        self.endpoints.append(e)
        return e

    def mount(self, path, ao):
        """
            mount adds a storage device to the Device
        """
        to_add = None
        if isinstance(ao, Storage):
            to_add = ao
        else:
            raise Exception("input to mount should be dict or Storage")
        self.mounts.append((path,to_add))
        return to_add

    def xir(self):
        for x in self.spec:
            self.props[x.name] = x.xir()
        return {
            'id': self.name,
            'endpoints': [x.xir() for x in self.endpoints],
            'props': self.props,
            'mounts': [{"path": x[0], "asset": x[1].xir()} for x in  self.mounts],
            #'props': {x.name: x.xir() for x in  self.spec},
        }

class IP():
    def __init__(self):
        self.addrs = []
        self.mtu = 1500

    def xir(self):
        return { 'addrs': self.addrs, 'mtu': self.mtu }

class EndpointRef():
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.ip = self.endpoint.ip

    def xir(self):
        x = {}
        x['node'] = self.endpoint.device.name
        x['index'] = self.endpoint.device.endpoints.index(self.endpoint)
        return x


class Endpoint():
    def __init__(self):
        #self.id = str(uuid.uuid4())
        self.props = {}
        self.ip = IP()
        self.device = None

    def xir(self):
        self.props['ip'] = self.ip.xir()
        return { 'props': self.props }

def link_id(endpoints):

    parts = []

    lid = ""
    for e in endpoints:
        parts.append(
            "%s.%d"%(
                e.endpoint.device.name, 
                e.endpoint.device.endpoints.index(e.endpoint)
            )
        )

    parts.sort()

    return "~".join(parts)

class Network():

    def __init__(self, endpoints, *args):
        #self.name = str(uuid.uuid4())
        self.name = link_id(endpoints)
        self.endpoints = endpoints
        self.spec = args
        self.props = {}

    def endpoint(self, x):
        return self[x]

    def __getitem__(self, x):

        if isinstance(x, Device):
            for e in self.endpoints:
                if e.endpoint.device == x:
                    return e.endpoint
            raise IndexError()

        raise TypeError()

    def xir(self):
        for x in self.spec:
            self.props[x.name] = x.xir()
        return {
            'id': link_id(self.endpoints),
            'endpoints': [ x.xir()  for x in self.endpoints],
            'props': self.props,
        }


class Storage():
    """
        Storage class is used to help users describe their experiment storage
        mount: is the name of the mount to show up on node (e.g. /mnt/mystorage, /dev/vdh)
        size: is the capacity or quota for the storage device
        name: is the reference to static allocations already preallocated
        kind: is the type of storage being requested
    """
    def __init__(self, kind=None, size=None, name=None):
        # the type of mount is required (cephfs, blockfs
        if not kind:
            raise Exception("type of mount is missing")
        self.type = kind

        # sizeacity is only required for block devices
        if size:
            self.size = size

        if name:
            self.name = name

    def xir(self):
        """
            special xir function to extract relevant information
        """
        return {
            'id': self.name,
            'size': self.size,
            'type': self.type,
        }
