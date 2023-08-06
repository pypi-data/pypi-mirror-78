from .exception import DetailedException

def make_tree(module_dict, **kwargs):
    for name, exception_injector in kwargs.items():
        exception_injector(name, DetailedException, module_dict)

def exception(*args, **kwargs):
    """
        Registers an exception. To be used inside of a `make_tree` call. All arguments
        will be treated as detail labels for the generated exception and all keyword
        arguments must be calls to this function to register the child exceptions.

        For examples see the `make_tree` documentation.
    """
    def exception_injector(name, parent, module_dict):
        class product_exception(parent, details=args):
            pass

        product_exception.__name__ = name
        product_exception.__module__ = module_dict["__name__"]
        module_dict[name] = product_exception

        for name, child_injector in kwargs.items():
            child_injector(name, product_exception, module_dict)

    return exception_injector
