

class DeviceGroup(object):
    """Generated from OpenAPI #/components/schemas/Device.DeviceGroup model

    An abstract container for emulated device containers  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - port_names (list[str]): One or more port names that the emulated device containers will share
    - devices (list[Device]): An unordered list of 0..n emulated device containers
    """
    def __init__(self, name=None, port_names=[], devices=[]):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(port_names, (list, type(None))) is True:
            self.port_names = port_names
        else:
            raise TypeError('port_names must be an instance of (list, type(None))')
        if isinstance(devices, (list, type(None))) is True:
            self.devices = devices
        else:
            raise TypeError('devices must be an instance of (list, type(None))')


class Device(object):
    """Generated from OpenAPI #/components/schemas/Device.Device model

    An abstract container for emulated devices  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - devices_per_port (int): The number of emulated devices that will be created on each port
    - ethernets (list[Ethernet]): An unordered list of 0..n emulated ethernet protocols
    - devices (list[Device]): An unordered list of 0..n emulated device containers
    - networks (list[Network]): An unordered list of 0..n emulated device containers
    """
    def __init__(self, name=None, devices_per_port=1, ethernets=[], devices=[], networks=[]):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(devices_per_port, (float, int, type(None))) is True:
            self.devices_per_port = devices_per_port
        else:
            raise TypeError('devices_per_port must be an instance of (float, int, type(None))')
        if isinstance(ethernets, (list, type(None))) is True:
            self.ethernets = ethernets
        else:
            raise TypeError('ethernets must be an instance of (list, type(None))')
        if isinstance(devices, (list, type(None))) is True:
            self.devices = devices
        else:
            raise TypeError('devices must be an instance of (list, type(None))')
        if isinstance(networks, (list, type(None))) is True:
            self.networks = networks
        else:
            raise TypeError('networks must be an instance of (list, type(None))')


class Ethernet(object):
    """Generated from OpenAPI #/components/schemas/Device.Ethernet model

    Emulated ethernet protocol  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - mac (Pattern): A container for emulated device property patterns
    - mtu (Pattern): A container for emulated device property patterns
    - vlans (list[Vlan]): List of vlans
    - ipv4 (Ipv4): Emulated ipv4 protocol
    - ipv6 (Ipv6): Emulated ipv6 protocol
    """
    def __init__(self, name=None, mac=None, mtu=None, vlans=[], ipv4=None, ipv6=None):
        from abstract_open_traffic_generator.device import Pattern
        from abstract_open_traffic_generator.device import Ipv4
        from abstract_open_traffic_generator.device import Ipv6
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(mac, (Pattern, type(None))) is True:
            self.mac = mac
        else:
            raise TypeError('mac must be an instance of (Pattern, type(None))')
        if isinstance(mtu, (Pattern, type(None))) is True:
            self.mtu = mtu
        else:
            raise TypeError('mtu must be an instance of (Pattern, type(None))')
        if isinstance(vlans, (list, type(None))) is True:
            self.vlans = vlans
        else:
            raise TypeError('vlans must be an instance of (list, type(None))')
        if isinstance(ipv4, (Ipv4, type(None))) is True:
            self.ipv4 = ipv4
        else:
            raise TypeError('ipv4 must be an instance of (Ipv4, type(None))')
        if isinstance(ipv6, (Ipv6, type(None))) is True:
            self.ipv6 = ipv6
        else:
            raise TypeError('ipv6 must be an instance of (Ipv6, type(None))')


class Pattern(object):
    """Generated from OpenAPI #/components/schemas/Device.Pattern model

    A container for emulated device property patterns  

    Args
    ----
    - choice (Union[str, list, Counter, Random]): TBD
    """
    _CHOICE_MAP = {
        'str': 'fixed',
        'list': 'list',
        'Counter': 'counter',
        'Random': 'random',
    }
    def __init__(self, choice=None):
        from abstract_open_traffic_generator.device import Counter
        from abstract_open_traffic_generator.device import Random
        if isinstance(choice, (str, list, Counter, Random)) is False:
            raise TypeError('choice must be of type: str, list, Counter, Random')
        self.__setattr__('choice', Pattern._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Pattern._CHOICE_MAP[type(choice).__name__], choice)


class Counter(object):
    """Generated from OpenAPI #/components/schemas/Device.Counter model

    An incrementing pattern  

    Args
    ----
    - start (str): TBD
    - step (str): TBD
    - up (Union[True, False]): TBD
    """
    def __init__(self, start=None, step=None, up=True):
        if isinstance(start, (str, type(None))) is True:
            self.start = start
        else:
            raise TypeError('start must be an instance of (str, type(None))')
        if isinstance(step, (str, type(None))) is True:
            self.step = step
        else:
            raise TypeError('step must be an instance of (str, type(None))')
        if isinstance(up, (bool, type(None))) is True:
            self.up = up
        else:
            raise TypeError('up must be an instance of (bool, type(None))')


class Decrement(object):
    """Generated from OpenAPI #/components/schemas/Device.Decrement model

    A decrementing pattern  

    Args
    ----
    - start (str): TBD
    - step (str): TBD
    """
    def __init__(self, start=None, step=None):
        if isinstance(start, (str, type(None))) is True:
            self.start = start
        else:
            raise TypeError('start must be an instance of (str, type(None))')
        if isinstance(step, (str, type(None))) is True:
            self.step = step
        else:
            raise TypeError('step must be an instance of (str, type(None))')


class Random(object):
    """Generated from OpenAPI #/components/schemas/Device.Random model

    A repeatable random range pattern  

    Args
    ----
    - min (str): TBD
    - max (str): TBD
    - step (Union[float, int]): TBD
    - seed (str): TBD
    """
    def __init__(self, min=None, max=None, step=None, seed=None):
        if isinstance(min, (str, type(None))) is True:
            self.min = min
        else:
            raise TypeError('min must be an instance of (str, type(None))')
        if isinstance(max, (str, type(None))) is True:
            self.max = max
        else:
            raise TypeError('max must be an instance of (str, type(None))')
        if isinstance(step, (float, int, type(None))) is True:
            self.step = step
        else:
            raise TypeError('step must be an instance of (float, int, type(None))')
        if isinstance(seed, (str, type(None))) is True:
            self.seed = seed
        else:
            raise TypeError('seed must be an instance of (str, type(None))')


class Vlan(object):
    """Generated from OpenAPI #/components/schemas/Device.Vlan model

    Emulated vlan protocol  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - tpid (Pattern): A container for emulated device property patterns
    - priority (Pattern): A container for emulated device property patterns
    - id (Pattern): A container for emulated device property patterns
    """
    
    TPID_8100 = '8100'
    TPID_88A8 = '88a8'
    TPID_9100 = '9100'
    TPID_9200 = '9200'
    TPID_9300 = '9300'
    
    def __init__(self, name=None, tpid=None, priority=None, id=None):
        from abstract_open_traffic_generator.device import Pattern
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(tpid, (Pattern, type(None))) is True:
            self.tpid = tpid
        else:
            raise TypeError('tpid must be an instance of (Pattern, type(None))')
        if isinstance(priority, (Pattern, type(None))) is True:
            self.priority = priority
        else:
            raise TypeError('priority must be an instance of (Pattern, type(None))')
        if isinstance(id, (Pattern, type(None))) is True:
            self.id = id
        else:
            raise TypeError('id must be an instance of (Pattern, type(None))')


class Ipv4(object):
    """Generated from OpenAPI #/components/schemas/Device.Ipv4 model

    Emulated ipv4 protocol  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - address (Pattern): A container for emulated device property patterns
    - gateway (Pattern): A container for emulated device property patterns
    - prefix (Pattern): A container for emulated device property patterns
    - bgpv4 (Bgpv4): Emulated bgpv4 protocol
    """
    def __init__(self, name=None, address=None, gateway=None, prefix=None, bgpv4=None):
        from abstract_open_traffic_generator.device import Pattern
        from abstract_open_traffic_generator.device import Bgpv4
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(address, (Pattern, type(None))) is True:
            self.address = address
        else:
            raise TypeError('address must be an instance of (Pattern, type(None))')
        if isinstance(gateway, (Pattern, type(None))) is True:
            self.gateway = gateway
        else:
            raise TypeError('gateway must be an instance of (Pattern, type(None))')
        if isinstance(prefix, (Pattern, type(None))) is True:
            self.prefix = prefix
        else:
            raise TypeError('prefix must be an instance of (Pattern, type(None))')
        if isinstance(bgpv4, (Bgpv4, type(None))) is True:
            self.bgpv4 = bgpv4
        else:
            raise TypeError('bgpv4 must be an instance of (Bgpv4, type(None))')


class Bgpv4(object):
    """Generated from OpenAPI #/components/schemas/Device.Bgpv4 model

    Emulated bgpv4 protocol  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - as_number_2_byte (Pattern): A container for emulated device property patterns
    - dut_as_number_2_byte (Pattern): A container for emulated device property patterns
    - as_number_4_byte (Pattern): A container for emulated device property patterns
    - as_number_set_mode (Pattern): A container for emulated device property patterns
    - as_type (Union[IBGP, EBGP]): The type of BGP autonomous system. External BGP (EBGP) is used for BGP links between two or more autonomous systems. Internal BGP (IBGP) is used within a single autonomous system
    - hold_time_interval (Pattern): A container for emulated device property patterns
    - keep_alive_interval (Pattern): A container for emulated device property patterns
    - graceful_restart (Pattern): A container for emulated device property patterns
    - authentication (Pattern): A container for emulated device property patterns
    - ttl (Pattern): A container for emulated device property patterns
    - dut_ipv4_address (Pattern): A container for emulated device property patterns
    """
    def __init__(self, name=None, as_number_2_byte=None, dut_as_number_2_byte=None, as_number_4_byte=None, as_number_set_mode=None, as_type=None, hold_time_interval=None, keep_alive_interval=None, graceful_restart=None, authentication=None, ttl=None, dut_ipv4_address=None):
        from abstract_open_traffic_generator.device import Pattern
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(as_number_2_byte, (Pattern, type(None))) is True:
            self.as_number_2_byte = as_number_2_byte
        else:
            raise TypeError('as_number_2_byte must be an instance of (Pattern, type(None))')
        if isinstance(dut_as_number_2_byte, (Pattern, type(None))) is True:
            self.dut_as_number_2_byte = dut_as_number_2_byte
        else:
            raise TypeError('dut_as_number_2_byte must be an instance of (Pattern, type(None))')
        if isinstance(as_number_4_byte, (Pattern, type(None))) is True:
            self.as_number_4_byte = as_number_4_byte
        else:
            raise TypeError('as_number_4_byte must be an instance of (Pattern, type(None))')
        if isinstance(as_number_set_mode, (Pattern, type(None))) is True:
            self.as_number_set_mode = as_number_set_mode
        else:
            raise TypeError('as_number_set_mode must be an instance of (Pattern, type(None))')
        if isinstance(as_type, (str, type(None))) is True:
            self.as_type = as_type
        else:
            raise TypeError('as_type must be an instance of (str, type(None))')
        if isinstance(hold_time_interval, (Pattern, type(None))) is True:
            self.hold_time_interval = hold_time_interval
        else:
            raise TypeError('hold_time_interval must be an instance of (Pattern, type(None))')
        if isinstance(keep_alive_interval, (Pattern, type(None))) is True:
            self.keep_alive_interval = keep_alive_interval
        else:
            raise TypeError('keep_alive_interval must be an instance of (Pattern, type(None))')
        if isinstance(graceful_restart, (Pattern, type(None))) is True:
            self.graceful_restart = graceful_restart
        else:
            raise TypeError('graceful_restart must be an instance of (Pattern, type(None))')
        if isinstance(authentication, (Pattern, type(None))) is True:
            self.authentication = authentication
        else:
            raise TypeError('authentication must be an instance of (Pattern, type(None))')
        if isinstance(ttl, (Pattern, type(None))) is True:
            self.ttl = ttl
        else:
            raise TypeError('ttl must be an instance of (Pattern, type(None))')
        if isinstance(dut_ipv4_address, (Pattern, type(None))) is True:
            self.dut_ipv4_address = dut_ipv4_address
        else:
            raise TypeError('dut_ipv4_address must be an instance of (Pattern, type(None))')


class Bgpv4RouteRange(object):
    """Generated from OpenAPI #/components/schemas/Device.Bgpv4RouteRange model

    Emulated bgpv4 route range  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - address (Pattern): A container for emulated device property patterns
    - prefix (Pattern): A container for emulated device property patterns
    - as_path (Pattern): A container for emulated device property patterns
    - next_hop_address (Pattern): A container for emulated device property patterns
    - aigp_metric (Pattern): A container for emulated device property patterns
    - atomic_aggregate (Pattern): A container for emulated device property patterns
    """
    def __init__(self, name=None, address=None, prefix=None, as_path=None, next_hop_address=None, aigp_metric=None, atomic_aggregate=None):
        from abstract_open_traffic_generator.device import Pattern
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(address, (Pattern, type(None))) is True:
            self.address = address
        else:
            raise TypeError('address must be an instance of (Pattern, type(None))')
        if isinstance(prefix, (Pattern, type(None))) is True:
            self.prefix = prefix
        else:
            raise TypeError('prefix must be an instance of (Pattern, type(None))')
        if isinstance(as_path, (Pattern, type(None))) is True:
            self.as_path = as_path
        else:
            raise TypeError('as_path must be an instance of (Pattern, type(None))')
        if isinstance(next_hop_address, (Pattern, type(None))) is True:
            self.next_hop_address = next_hop_address
        else:
            raise TypeError('next_hop_address must be an instance of (Pattern, type(None))')
        if isinstance(aigp_metric, (Pattern, type(None))) is True:
            self.aigp_metric = aigp_metric
        else:
            raise TypeError('aigp_metric must be an instance of (Pattern, type(None))')
        if isinstance(atomic_aggregate, (Pattern, type(None))) is True:
            self.atomic_aggregate = atomic_aggregate
        else:
            raise TypeError('atomic_aggregate must be an instance of (Pattern, type(None))')


class Ipv6(object):
    """Generated from OpenAPI #/components/schemas/Device.Ipv6 model

    Emulated ipv6 protocol  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - address (Pattern): A container for emulated device property patterns
    - gateway (Pattern): A container for emulated device property patterns
    - prefix (Pattern): A container for emulated device property patterns
    - manual_gateway_mac (Pattern): A container for emulated device property patterns
    """
    def __init__(self, name=None, address=None, gateway=None, prefix=None, manual_gateway_mac=None):
        from abstract_open_traffic_generator.device import Pattern
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(address, (Pattern, type(None))) is True:
            self.address = address
        else:
            raise TypeError('address must be an instance of (Pattern, type(None))')
        if isinstance(gateway, (Pattern, type(None))) is True:
            self.gateway = gateway
        else:
            raise TypeError('gateway must be an instance of (Pattern, type(None))')
        if isinstance(prefix, (Pattern, type(None))) is True:
            self.prefix = prefix
        else:
            raise TypeError('prefix must be an instance of (Pattern, type(None))')
        if isinstance(manual_gateway_mac, (Pattern, type(None))) is True:
            self.manual_gateway_mac = manual_gateway_mac
        else:
            raise TypeError('manual_gateway_mac must be an instance of (Pattern, type(None))')


class Network(object):
    """Generated from OpenAPI #/components/schemas/Device.Network model

    An abstract container for an emulated network devices  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - network_devices_per_port (int): The number of emulated network devices that will be created on each port
    - flow_link_name (str): Identifies which object in another container is the next hop from this container. The name cannot be one of the names in this networks container. An empty value indicates there is no flow link other than the default specified by the implementation
    - choice (Union[Bgpv4RouteRange]): The type of emulated network devices in the container
    """
    _CHOICE_MAP = {
        'Bgpv4RouteRange': 'bgpv4_route_range',
    }
    def __init__(self, name=None, network_devices_per_port=1, flow_link_name=None, choice=None):
        from abstract_open_traffic_generator.device import Bgpv4RouteRange
        if isinstance(choice, (Bgpv4RouteRange)) is False:
            raise TypeError('choice must be of type: Bgpv4RouteRange')
        self.__setattr__('choice', Network._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Network._CHOICE_MAP[type(choice).__name__], choice)
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(network_devices_per_port, (float, int, type(None))) is True:
            self.network_devices_per_port = network_devices_per_port
        else:
            raise TypeError('network_devices_per_port must be an instance of (float, int, type(None))')
        if isinstance(flow_link_name, (str, type(None))) is True:
            self.flow_link_name = flow_link_name
        else:
            raise TypeError('flow_link_name must be an instance of (str, type(None))')
