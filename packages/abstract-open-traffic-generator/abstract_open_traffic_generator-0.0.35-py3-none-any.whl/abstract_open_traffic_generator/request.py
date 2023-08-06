

class Port(object):
    """Generated from OpenAPI #/components/schemas/Request.Port model

    The flow result request to the traffic generator   

    Args
    ----
    - names (list[str]): The names of objects to return results for. An empty list will return all port row results
    - columns (list[Union[name, location, link, capture, frames_tx, frames_rx, frames_tx_rate, frames_rx_rate, bytes_tx, bytes_rx, bytes_tx_rate, bytes_rx_rate, pfc_class_0_frames_rx, pfc_class_1_frames_rx, pfc_class_2_frames_rx, pfc_class_3_frames_rx, pfc_class_4_frames_rx, pfc_class_5_frames_rx, pfc_class_6_frames_rx, pfc_class_7_frames_rx]]): The names of columns to return results for. An empty list will return all columns. The name column will always be included as it is the unique key
    """
    def __init__(self, names=[], columns=[]):
        if isinstance(names, (list, type(None))) is True:
            self.names = names
        else:
            raise TypeError('names must be an instance of (list, type(None))')
        if isinstance(columns, (list, type(None))) is True:
            self.columns = columns
        else:
            raise TypeError('columns must be an instance of (list, type(None))')


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
