

class Capture(object):
    """Generated from OpenAPI #/components/schemas/Capture.Capture model

    Capture model  

    Args
    ----
    - name (str): Unique name of an object that is the primary key for objects found in arrays
    - port_names (list[str]): A list of port names to configure capture settings on
    - filters (str): TBD
    """
    def __init__(self, name=None, port_names=[], filters=None):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(port_names, (list, type(None))) is True:
            self.port_names = port_names
        else:
            raise TypeError('port_names must be an instance of (list, type(None))')
        if isinstance(filters, (str, type(None))) is True:
            self.filters = filters
        else:
            raise TypeError('filters must be an instance of (str, type(None))')
