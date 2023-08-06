

class Config(object):
    """Generated from OpenAPI #/components/schemas/Config.Config model

    A container for all models that are part of the configuration  

    Args
    ----
    - ports (list[Port]): The ports that will be configured on the traffic generator
    - device_groups (list[DeviceGroup]): The device groups that will be configured on the traffic generator
    - flows (list[Flow]): The flows that will be configured on the traffic generator
    - layer1 (list[Layer1]): The layer1 settings that will be configured on the traffic generator
    - captures (list[Capture]): The captures that will be configured on the traffic generator
    """
    def __init__(self, ports=[], device_groups=[], flows=[], layer1=[], captures=[]):
        if isinstance(ports, (list, type(None))) is True:
            self.ports = ports
        else:
            raise TypeError('ports must be an instance of (list, type(None))')
        if isinstance(device_groups, (list, type(None))) is True:
            self.device_groups = device_groups
        else:
            raise TypeError('device_groups must be an instance of (list, type(None))')
        if isinstance(flows, (list, type(None))) is True:
            self.flows = flows
        else:
            raise TypeError('flows must be an instance of (list, type(None))')
        if isinstance(layer1, (list, type(None))) is True:
            self.layer1 = layer1
        else:
            raise TypeError('layer1 must be an instance of (list, type(None))')
        if isinstance(captures, (list, type(None))) is True:
            self.captures = captures
        else:
            raise TypeError('captures must be an instance of (list, type(None))')
