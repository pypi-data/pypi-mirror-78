

class Request(object):
    """Generated from OpenAPI #/components/schemas/Result.Request model

    The result request to the traffic generator   

    Args
    ----
    - result_type (Union[state, location, ports, flows]): TBD
    """
    def __init__(self, result_type=None):
        if isinstance(result_type, (str, type(None))) is True:
            self.result_type = result_type
        else:
            raise TypeError('result_type must be an instance of (str, type(None))')


class Response(object):
    """Generated from OpenAPI #/components/schemas/Result.Response model

    The result response from the traffic generator   

    Args
    ----
    - state (State): TBD
    - location (Location): Location result. Used to find out the possible types of location formats supported by an implementation. Implementations will return a description of the location format along with the regex format that will be used to validate the location input on the port object
    - ports (Port): TBD
    - flows (Flow): TBD
    """
    def __init__(self, state=None, location=None, ports=None, flows=None):
        from abstract_open_traffic_generator.result import State
        from abstract_open_traffic_generator.result import Location
        from abstract_open_traffic_generator.result import Port
        from abstract_open_traffic_generator.result import Flow
        if isinstance(state, (State, type(None))) is True:
            self.state = state
        else:
            raise TypeError('state must be an instance of (State, type(None))')
        if isinstance(location, (Location, type(None))) is True:
            self.location = location
        else:
            raise TypeError('location must be an instance of (Location, type(None))')
        if isinstance(ports, (Port, type(None))) is True:
            self.ports = ports
        else:
            raise TypeError('ports must be an instance of (Port, type(None))')
        if isinstance(flows, (Flow, type(None))) is True:
            self.flows = flows
        else:
            raise TypeError('flows must be an instance of (Flow, type(None))')


class State(object):
    """Generated from OpenAPI #/components/schemas/Result.State model

    TBD  

    Args
    ----
    - state_transitions (Union[success, errored, transitioning]): TBD
    - transitions (Union[float, int]): Indicates the current total number of state transitions
    - errors (Union[float, int]): Indicates the current total number of state errors
    - details (list[StateDetail]): TBD
    """
    def __init__(self, state_transitions=None, transitions=None, errors=None, details=[]):
        if isinstance(state_transitions, (str, type(None))) is True:
            self.state_transitions = state_transitions
        else:
            raise TypeError('state_transitions must be an instance of (str, type(None))')
        if isinstance(transitions, (float, int, type(None))) is True:
            self.transitions = transitions
        else:
            raise TypeError('transitions must be an instance of (float, int, type(None))')
        if isinstance(errors, (float, int, type(None))) is True:
            self.errors = errors
        else:
            raise TypeError('errors must be an instance of (float, int, type(None))')
        if isinstance(details, (list, type(None))) is True:
            self.details = details
        else:
            raise TypeError('details must be an instance of (list, type(None))')


class StateDetail(object):
    """Generated from OpenAPI #/components/schemas/Result.StateDetail model

    TBD  

    Args
    ----
    - name (str): The unique name of an object in the configuration
    - configured (str): The configured state of the named object
    - current (str): The current state of the named object
    - message (str): Detailed transition or error information
    """
    def __init__(self, name=None, configured=None, current=None, message=None):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(configured, (str, type(None))) is True:
            self.configured = configured
        else:
            raise TypeError('configured must be an instance of (str, type(None))')
        if isinstance(current, (str, type(None))) is True:
            self.current = current
        else:
            raise TypeError('current must be an instance of (str, type(None))')
        if isinstance(message, (str, type(None))) is True:
            self.message = message
        else:
            raise TypeError('message must be an instance of (str, type(None))')


class Location(object):
    """Generated from OpenAPI #/components/schemas/Result.Location model

    Location result  
    Used to find out the possible types of location formats supported by an implementation  
    Implementations will return a description of the location format along with the regex format that will be used to validate the location input on the port object  

    Args
    ----
    - description (str): The description of the location format
    - format (str): The regex format of the location
    """
    def __init__(self, description=None, format=None):
        if isinstance(description, (str, type(None))) is True:
            self.description = description
        else:
            raise TypeError('description must be an instance of (str, type(None))')
        if isinstance(format, (str, type(None))) is True:
            self.format = format
        else:
            raise TypeError('format must be an instance of (str, type(None))')


class Port(object):
    """Generated from OpenAPI #/components/schemas/Result.Port model

    TBD  

    Args
    ----
    - name (str): The name of a configured port
    - frames_tx (Union[float, int]): The current total number of frames transmitted
    - frames_rx (Union[float, int]): The current total number of valid frames received
    - bytes_tx (Union[float, int]): The current total number of bytes transmitted
    - bytes_rx (Union[float, int]): The current total number of valid bytes received
    - frames_tx_rate (Union[float, int]): The current rate of frames transmitted
    - frames_rx_rate (Union[float, int]): The current rate of valid frames received
    - data_integrity_errors (Union[float, int]): The current total number of data integrity errors
    - counters (list[None]): A map of unique names of PortCounter objects added to Port objects and the corresponding count values
    """
    def __init__(self, name=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, data_integrity_errors=None, counters=[]):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(frames_tx, (float, int, type(None))) is True:
            self.frames_tx = frames_tx
        else:
            raise TypeError('frames_tx must be an instance of (float, int, type(None))')
        if isinstance(frames_rx, (float, int, type(None))) is True:
            self.frames_rx = frames_rx
        else:
            raise TypeError('frames_rx must be an instance of (float, int, type(None))')
        if isinstance(bytes_tx, (float, int, type(None))) is True:
            self.bytes_tx = bytes_tx
        else:
            raise TypeError('bytes_tx must be an instance of (float, int, type(None))')
        if isinstance(bytes_rx, (float, int, type(None))) is True:
            self.bytes_rx = bytes_rx
        else:
            raise TypeError('bytes_rx must be an instance of (float, int, type(None))')
        if isinstance(frames_tx_rate, (float, int, type(None))) is True:
            self.frames_tx_rate = frames_tx_rate
        else:
            raise TypeError('frames_tx_rate must be an instance of (float, int, type(None))')
        if isinstance(frames_rx_rate, (float, int, type(None))) is True:
            self.frames_rx_rate = frames_rx_rate
        else:
            raise TypeError('frames_rx_rate must be an instance of (float, int, type(None))')
        if isinstance(data_integrity_errors, (float, int, type(None))) is True:
            self.data_integrity_errors = data_integrity_errors
        else:
            raise TypeError('data_integrity_errors must be an instance of (float, int, type(None))')
        if isinstance(counters, (list, type(None))) is True:
            self.counters = counters
        else:
            raise TypeError('counters must be an instance of (list, type(None))')


class Flow(object):
    """Generated from OpenAPI #/components/schemas/Result.Flow model

    TBD  

    Args
    ----
    - name (str): The name of a configured flow
    - port_tx (str): The name of a configured port
    - port_rx (str): The name of a configured port
    - frames_tx (Union[float, int]): The current total number of frames transmitted
    - frames_rx (Union[float, int]): The current total number of valid frames received
    - bytes_tx (Union[float, int]): The current total number of bytes transmitted
    - bytes_rx (Union[float, int]): The current total number of valid bytes received
    - frames_tx_rate (Union[float, int]): The current rate of frames transmitted
    - frames_rx_rate (Union[float, int]): The current rate of valid frames received
    - loss (Union[float, int]): The percentage of lost frames
    - group_by (None): A runtime map of field name to result value The name comes from the flow.packet.header.group_by property
    """
    def __init__(self, name=None, port_tx=None, port_rx=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, loss=None, group_by=None):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(port_tx, (str, type(None))) is True:
            self.port_tx = port_tx
        else:
            raise TypeError('port_tx must be an instance of (str, type(None))')
        if isinstance(port_rx, (str, type(None))) is True:
            self.port_rx = port_rx
        else:
            raise TypeError('port_rx must be an instance of (str, type(None))')
        if isinstance(frames_tx, (float, int, type(None))) is True:
            self.frames_tx = frames_tx
        else:
            raise TypeError('frames_tx must be an instance of (float, int, type(None))')
        if isinstance(frames_rx, (float, int, type(None))) is True:
            self.frames_rx = frames_rx
        else:
            raise TypeError('frames_rx must be an instance of (float, int, type(None))')
        if isinstance(bytes_tx, (float, int, type(None))) is True:
            self.bytes_tx = bytes_tx
        else:
            raise TypeError('bytes_tx must be an instance of (float, int, type(None))')
        if isinstance(bytes_rx, (float, int, type(None))) is True:
            self.bytes_rx = bytes_rx
        else:
            raise TypeError('bytes_rx must be an instance of (float, int, type(None))')
        if isinstance(frames_tx_rate, (float, int, type(None))) is True:
            self.frames_tx_rate = frames_tx_rate
        else:
            raise TypeError('frames_tx_rate must be an instance of (float, int, type(None))')
        if isinstance(frames_rx_rate, (float, int, type(None))) is True:
            self.frames_rx_rate = frames_rx_rate
        else:
            raise TypeError('frames_rx_rate must be an instance of (float, int, type(None))')
        if isinstance(loss, (float, int, type(None))) is True:
            self.loss = loss
        else:
            raise TypeError('loss must be an instance of (float, int, type(None))')
        if isinstance(group_by, None) is True:
            self.group_by = group_by
        else:
            raise TypeError('group_by must be an instance of None')
