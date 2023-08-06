class LazyCachedAttribute(object):
    '''Computes attribute value and caches it in instance.

    Example:
        class MyClass(object):
            def myMethod(self):
                # ...
            myMethod = CachedAttribute(myMethod)
    Use "del inst.myMethod" to clear cache.'''

    def __init__(self, method, name: str = None, **method_args):
        self.method = method
        self.method_args=method_args
        self.name = name or method.__name__

    def __get__(self, inst, cls):
        if inst is None:
            return self
        result = self.method(inst, **self.method_args)
        setattr(inst, self.name, result)
        return result
