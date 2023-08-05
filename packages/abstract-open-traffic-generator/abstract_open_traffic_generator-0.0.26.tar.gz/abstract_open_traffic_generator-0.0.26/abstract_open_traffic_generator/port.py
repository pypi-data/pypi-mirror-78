

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
        virtual machine, docker container, kubernetes cluster The test port location format is implementation specific. Use the /results API to determine what formats the implementation supports for the location property
    - link_state (Union[up, down]): The configured link state of the port. Compare the actual state vs the configured state by using the /results API
    - capture_state (Union[start, stop]): The configured capture state of the port. Compare the actual state vs the configured state by using the /results API
    """
    def __init__(self, name=None, location=None, link_state='up', capture_state='stop'):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(location, (str, type(None))) is True:
            self.location = location
        else:
            raise TypeError('location must be an instance of (str, type(None))')
        if isinstance(link_state, (str, type(None))) is True:
            self.link_state = link_state
        else:
            raise TypeError('link_state must be an instance of (str, type(None))')
        if isinstance(capture_state, (str, type(None))) is True:
            self.capture_state = capture_state
        else:
            raise TypeError('capture_state must be an instance of (str, type(None))')
