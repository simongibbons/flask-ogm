from py2neo.ogm import GraphObject, Property

class WidgetCollection(object):
    def __init__(self, *args, **kwargs):
        self.data = list(*args, **kwargs)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def where(self, *args, **kwargs):
        """Mocks up py2neo's where
        """
        # should only ever have 1 kwarg
        assert len(kwargs) == 1
        k, v = list(kwargs.items())[0]
        self.data = [
            x
            for x in self.data
            if getattr(x, k) == v
        ]

        return self

    def __repr__(self):
        return repr(self.data)



class Widget(GraphObject):
    unique_id = Property()
    name = Property()
    colour = Property()
    __primarykey__ = 'unique_id'
    MOCK_DATA = [
        {
            'unique_id': 1,
            'name': 'Widget 1',
            'colour': 'red',
        },
        {
            'unique_id': 2,
            'name': 'Widget 2',
            'colour': 'red',
        },
        {
            'unique_id': 3,
            'name': 'Widget 3',
            'colour': 'blue',
        },
    ]

    selected_data = []

    @classmethod
    def mock_wrap(cls, d):
        w = cls()
        for k, v in d.items():
            setattr(w, k, v)
        return w

    @classmethod
    def custom_constructor(cls, graph, property):
        """Never runs, only used in tests that check this methos id
        present
        """
        pass

    @classmethod
    def return_non_iter(cls, *args, **kwargs):
        """Required for checking an excdeption is raised when a
        constructor returns a non-iterable
        """
        return None

    @classmethod
    def mock_select(cls, graph, primary_value = None):
        """Mock select method to return iterables for tests"""
        wc = WidgetCollection([cls.mock_wrap(w) for w in cls.MOCK_DATA])
        if primary_value is None:
            return wc

        return wc.where(cls, **{ cls.__primarykey__: primary_value})

    @classmethod
    def __iter__(cls):
        """When an iterable is required, we want the resultant data
        from the select query. In the real GraphObject, several objects
        exist here...
        """
        return iter(cls.selected_data)
