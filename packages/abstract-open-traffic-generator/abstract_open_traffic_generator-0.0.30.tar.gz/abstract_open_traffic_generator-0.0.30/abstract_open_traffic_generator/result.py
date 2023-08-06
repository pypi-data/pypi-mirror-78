

class Port(object):
    """Generated from OpenAPI #/components/schemas/Result.Port model

    TBD  

    Args
    ----
    - name (str): The name of a configured port
    - location (str): The state of the connection to the test port location
    - link (str): The state of the test port link
    - capture (str): The state of the test port capture infrastructure
    - frames_tx (int): The current total number of frames transmitted
    - frames_rx (int): The current total number of valid frames received
    - bytes_tx (int): The current total number of bytes transmitted
    - bytes_rx (int): The current total number of valid bytes received
    - frames_tx_rate (Union[float, int]): The current rate of frames transmitted
    - frames_rx_rate (Union[float, int]): The current rate of valid frames received
    - data_integrity_errors (int): The current total number of data integrity errors
    - counters (list[None]): A map of unique names of PortCounter objects added to Port objects and the corresponding count values
    """
    def __init__(self, name=None, location=None, link=None, capture=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, data_integrity_errors=None, counters=[]):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(location, (str, type(None))) is True:
            self.location = location
        else:
            raise TypeError('location must be an instance of (str, type(None))')
        if isinstance(link, (str, type(None))) is True:
            self.link = link
        else:
            raise TypeError('link must be an instance of (str, type(None))')
        if isinstance(capture, (str, type(None))) is True:
            self.capture = capture
        else:
            raise TypeError('capture must be an instance of (str, type(None))')
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


class Request(object):
    """Generated from OpenAPI #/components/schemas/Result.Request model

    The result request to the traffic generator   

    Args
    ----
    - category (list[Union[capability, port, flow]]): The results that are to be returned. More than one category of results can be returned in one call
    - names (list[str]): The names of objects to return results for. An empty list will return all results for each category specified
    """
    def __init__(self, category=[], names=[]):
        if isinstance(category, (list, type(None))) is True:
            self.category = category
        else:
            raise TypeError('category must be an instance of (list, type(None))')
        if isinstance(names, (list, type(None))) is True:
            self.names = names
        else:
            raise TypeError('names must be an instance of (list, type(None))')


class Response(object):
    """Generated from OpenAPI #/components/schemas/Result.Response model

    The result response from the traffic generator   

    Args
    ----
    - capabilities (list[Capability]): The capability results
    - ports (list[Port]): The port results
    - flows (list[Flow]): The flow results
    """
    def __init__(self, capabilities=[], ports=[], flows=[]):
        if isinstance(capabilities, (list, type(None))) is True:
            self.capabilities = capabilities
        else:
            raise TypeError('capabilities must be an instance of (list, type(None))')
        if isinstance(ports, (list, type(None))) is True:
            self.ports = ports
        else:
            raise TypeError('ports must be an instance of (list, type(None))')
        if isinstance(flows, (list, type(None))) is True:
            self.flows = flows
        else:
            raise TypeError('flows must be an instance of (list, type(None))')


class Errors(object):
    """Generated from OpenAPI #/components/schemas/Result.Errors model

    TBD  

    Args
    ----
    - errors (list[Error]): TBD
    """
    def __init__(self, errors=[]):
        if isinstance(errors, (list, type(None))) is True:
            self.errors = errors
        else:
            raise TypeError('errors must be an instance of (list, type(None))')


class Error(object):
    """Generated from OpenAPI #/components/schemas/Result.Error model

    TBD  

    Args
    ----
    - name (str): The unique name of an object in the configuration
    - message (str): Detailed error information
    """
    def __init__(self, name=None, message=None):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(message, (str, type(None))) is True:
            self.message = message
        else:
            raise TypeError('message must be an instance of (str, type(None))')


class Capability(object):
    """Generated from OpenAPI #/components/schemas/Result.Capability model

    TBD  

    Args
    ----
    - unsupported (list[str]): A list of #/components/schemas/... path that are not supported
    - formats (list[str]): A #/components/schemas/... path and specific format details regarding the path. Specific model format details can be additional objects and properties represented as a hashmap. For example layer1 models are defined as a hashmap key to object with each object consisting of a specific name/value property pairs. This list of items will detail any specific formats, properties, enums
    """
    def __init__(self, unsupported=[], formats=[]):
        if isinstance(unsupported, (list, type(None))) is True:
            self.unsupported = unsupported
        else:
            raise TypeError('unsupported must be an instance of (list, type(None))')
        if isinstance(formats, (list, type(None))) is True:
            self.formats = formats
        else:
            raise TypeError('formats must be an instance of (list, type(None))')


class Flow(object):
    """Generated from OpenAPI #/components/schemas/Result.Flow model

    TBD  

    Args
    ----
    - name (str): The name of a configured flow
    - port_tx (str): The name of a configured port
    - port_rx (str): The name of a configured port
    - frames_tx (int): The current total number of frames transmitted
    - frames_rx (int): The current total number of valid frames received
    - bytes_tx (int): The current total number of bytes transmitted
    - bytes_rx (int): The current total number of valid bytes received
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
