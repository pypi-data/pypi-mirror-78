class Event():
    '''Event class'''

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data


    def __init__(self, type, data):
        self._type = type
        self._data = data

    def __repr__(self):
        # <Event:event_type>
        return "<Event:{}".format(self.type)

    def __str__(self):
        # <Event:event_type>
        # {data}
        return "<Event:{}>\n{}".format(self.type, self.data)
