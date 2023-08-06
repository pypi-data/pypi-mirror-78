

class PortLink(object):
    """Generated from OpenAPI #/components/schemas/Control.PortLink model

    Control link state  

    Args
    ----
    - names (list[str]): The names of port objects to control link state. An empty list will control all port objects
    - state (Union[up, down]): The state of the port link
    """
    def __init__(self, names=[], state=None):
        if isinstance(names, (list, type(None))) is True:
            self.names = names
        else:
            raise TypeError('names must be an instance of (list, type(None))')
        if isinstance(state, (str, type(None))) is True:
            self.state = state
        else:
            raise TypeError('state must be an instance of (str, type(None))')
