def track_methods(obj):
    import types

    def make_wrapper(method, message):
        def wrapper(self, *args, **kwargs):
            print(message)
            return method(self, *args, **kwargs)

        return wrapper

    def get_var_name(obj):
        for gvar in globals():
            if id(obj) == id(globals()[gvar]):
                return gvar

    class TrackedClass(obj.__class__):
        def __init__(self):
            super().__init__()

    obj.__class__ = TrackedClass

    cls = obj.__class__

    tracked_methods = []
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if any(issubclass(type(attr), t) for t in [types.FunctionType]):
            wrapper = make_wrapper(attr, get_var_name(obj) + "." + attr_name)
            setattr(cls, attr_name, wrapper)
            tracked_methods.append(attr_name)


import pandas as pd
import numpy as np

CONTAINER = []
log = {}

df = pd.DataFrame({'a': [1, 2, 3], 'b': [1, 2, np.nan], 'c': [1, 2, 3]})
track_methods(df)

df.iloc[0, 0] = 100
log['iloc'] = CONTAINER.copy()
del CONTAINER[:]

df.dropna(inplace=True)
log['dropna'] = CONTAINER.copy()
del CONTAINER[:]

for key in log.keys():
    for item in log[key]:
        if all([item in x for x in log.values()]):
            print(item)
