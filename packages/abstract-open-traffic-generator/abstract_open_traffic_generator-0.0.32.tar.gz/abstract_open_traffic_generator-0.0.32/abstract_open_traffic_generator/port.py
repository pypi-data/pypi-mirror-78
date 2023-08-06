

class Port(object):
    """Generated from OpenAPI #/components/schemas/Port.Port model

    An abstract test port  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - location (str): The location of a test port. It is the endpoint where packets will emit from. Test port locations can be the following:
        physical appliance with multiple ports
        physical chassis with multiple cards and ports
        local interface
        virtual machine, docker container, kubernetes cluster The test port location format is implementation specific. Use the /results/capabilities API to determine what formats an implementation supports for the location property. Get the configured location state by using the /results/port API
    """
    def __init__(self, name=None, location=None):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(location, (str, type(None))) is True:
            self.location = location
        else:
            raise TypeError('location must be an instance of (str, type(None))')


class Layer1(object):
    """Generated from OpenAPI #/components/schemas/Port.Layer1 model

    A container for layer1 ports and settings  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - port_names (list[str]): A list of unique names of a port objects that will share the choice settings.
    - choice (Union[OneHundredGbe, Ethernet]): The type of layer1 characteristics
    """
    _CHOICE_MAP = {
        'OneHundredGbe': 'one_hundred_gbe',
        'Ethernet': 'ethernet',
    }
    def __init__(self, name=None, port_names=[], choice=None):
        from abstract_open_traffic_generator.port import OneHundredGbe
        from abstract_open_traffic_generator.port import Ethernet
        if isinstance(choice, (OneHundredGbe, Ethernet)) is False:
            raise TypeError('choice must be of type: OneHundredGbe, Ethernet')
        self.__setattr__('choice', Layer1._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Layer1._CHOICE_MAP[type(choice).__name__], choice)
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(port_names, (list, type(None))) is True:
            self.port_names = port_names
        else:
            raise TypeError('port_names must be an instance of (list, type(None))')


class OneHundredGbe(object):
    """Generated from OpenAPI #/components/schemas/Port.OneHundredGbe model

    100 gigabit ethernet settings  

    Args
    ----
    - ieee_media_defaults (Union[True, False]): Enable/disable ieee media default settings. True will override the speed, auto_negotiate, link_training, rs_fec settings
    - auto_negotiate (Union[True, False]): Enable/disable auto negotiation
    - link_training (Union[True, False]): Enable/disable link training
    - rs_fec (Union[True, False]): Enable/disable reed solomon forward error correction (RS FEC)
    - speed (Union[one_hundred_gbps, fifty_gbps, forty_gbps, twenty_five_gpbs, ten_gbps]): This is the speed that will be used if auto_negotiate is false
    """
    def __init__(self, ieee_media_defaults=True, auto_negotiate=False, link_training=False, rs_fec=False, speed='one_hundred_gbps'):
        if isinstance(ieee_media_defaults, (bool, type(None))) is True:
            self.ieee_media_defaults = ieee_media_defaults
        else:
            raise TypeError('ieee_media_defaults must be an instance of (bool, type(None))')
        if isinstance(auto_negotiate, (bool, type(None))) is True:
            self.auto_negotiate = auto_negotiate
        else:
            raise TypeError('auto_negotiate must be an instance of (bool, type(None))')
        if isinstance(link_training, (bool, type(None))) is True:
            self.link_training = link_training
        else:
            raise TypeError('link_training must be an instance of (bool, type(None))')
        if isinstance(rs_fec, (bool, type(None))) is True:
            self.rs_fec = rs_fec
        else:
            raise TypeError('rs_fec must be an instance of (bool, type(None))')
        if isinstance(speed, (str, type(None))) is True:
            self.speed = speed
        else:
            raise TypeError('speed must be an instance of (str, type(None))')


class Ethernet(object):
    """Generated from OpenAPI #/components/schemas/Port.Ethernet model

    10/100/1000 Ethernet settings  

    Args
    ----
    - media (Union[copper, fiber]): TBD
    - speed (Union[one_thousand_mbps, one_hundred_fd_mbps, one_hundred_hd_mbps, ten_fd_mbps, ten_hd_mbps]): This is the speed that will be used if auto_negotiate is false
    - auto_negotiate (Union[True, False]): Enable/disable auto negotiation
    - advertise_one_thousand_mbps (Union[True, False]): If auto_negotiate is true then this speed will be advertised
    - advertise_one_hundred_fd_mbps (Union[True, False]): If auto_negotiate is true then this speed will be advertised
    - advertise_one_hundred_hd_mbps (Union[True, False]): If auto_negotiate is true then this speed will be advertised
    - advertise_ten_fd_mbps (Union[True, False]): If auto_negotiate is true then this speed will be advertised
    - advertise_ten_hd_mbps (Union[True, False]): If auto_negotiate is true then this speed will be advertised
    """
    def __init__(self, media='copper', speed='one_thousand_mbps', auto_negotiate=True, advertise_one_thousand_mbps=True, advertise_one_hundred_fd_mbps=True, advertise_one_hundred_hd_mbps=True, advertise_ten_fd_mbps=True, advertise_ten_hd_mbps=True):
        if isinstance(media, (str, type(None))) is True:
            self.media = media
        else:
            raise TypeError('media must be an instance of (str, type(None))')
        if isinstance(speed, (str, type(None))) is True:
            self.speed = speed
        else:
            raise TypeError('speed must be an instance of (str, type(None))')
        if isinstance(auto_negotiate, (bool, type(None))) is True:
            self.auto_negotiate = auto_negotiate
        else:
            raise TypeError('auto_negotiate must be an instance of (bool, type(None))')
        if isinstance(advertise_one_thousand_mbps, (bool, type(None))) is True:
            self.advertise_one_thousand_mbps = advertise_one_thousand_mbps
        else:
            raise TypeError('advertise_one_thousand_mbps must be an instance of (bool, type(None))')
        if isinstance(advertise_one_hundred_fd_mbps, (bool, type(None))) is True:
            self.advertise_one_hundred_fd_mbps = advertise_one_hundred_fd_mbps
        else:
            raise TypeError('advertise_one_hundred_fd_mbps must be an instance of (bool, type(None))')
        if isinstance(advertise_one_hundred_hd_mbps, (bool, type(None))) is True:
            self.advertise_one_hundred_hd_mbps = advertise_one_hundred_hd_mbps
        else:
            raise TypeError('advertise_one_hundred_hd_mbps must be an instance of (bool, type(None))')
        if isinstance(advertise_ten_fd_mbps, (bool, type(None))) is True:
            self.advertise_ten_fd_mbps = advertise_ten_fd_mbps
        else:
            raise TypeError('advertise_ten_fd_mbps must be an instance of (bool, type(None))')
        if isinstance(advertise_ten_hd_mbps, (bool, type(None))) is True:
            self.advertise_ten_hd_mbps = advertise_ten_hd_mbps
        else:
            raise TypeError('advertise_ten_hd_mbps must be an instance of (bool, type(None))')
