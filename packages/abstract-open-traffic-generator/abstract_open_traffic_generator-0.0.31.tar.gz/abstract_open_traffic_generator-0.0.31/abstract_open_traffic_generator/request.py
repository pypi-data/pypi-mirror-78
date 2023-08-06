

class Port(object):
    """Generated from OpenAPI #/components/schemas/Request.Port model

    The flow result request to the traffic generator   

    Args
    ----
    - names (list[str]): The names of objects to return results for. An empty list will return all port results
    """
    def __init__(self, names=[]):
        if isinstance(names, (list, type(None))) is True:
            self.names = names
        else:
            raise TypeError('names must be an instance of (list, type(None))')


class Flow(object):
    """Generated from OpenAPI #/components/schemas/Request.Flow model

    The flow result request to the traffic generator   

    Args
    ----
    - names (list[str]): The names of objects to return results for. An empty list will return all flow results
    - group_by (list[str]): Unique names of fields to group results by
    """
    def __init__(self, names=[], group_by=[]):
        if isinstance(names, (list, type(None))) is True:
            self.names = names
        else:
            raise TypeError('names must be an instance of (list, type(None))')
        if isinstance(group_by, (list, type(None))) is True:
            self.group_by = group_by
        else:
            raise TypeError('group_by must be an instance of (list, type(None))')
