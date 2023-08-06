

class PortLink(object):
    """Generated from OpenAPI #/components/schemas/Control.PortLink model

    Control port link state  

    Args
    ----
    - names (list[str]): The names of port objects to. An empty list will control all port objects
    - state (Union[up, down]): The link state
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


class FlowTransmit(object):
    """Generated from OpenAPI #/components/schemas/Control.FlowTransmit model

    Control flow transmit state  

    Args
    ----
    - names (list[str]): The names of flow objects to control. An empty list will control all flow objects
    - state (Union[start, stop, pause]): The transmit state
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
