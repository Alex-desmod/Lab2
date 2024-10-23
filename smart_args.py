import inspect
import copy


class Evaluated:
    """
    The class is used to mark an 'evaluated' type of default arguments of functions.

    """

    def __init__(self, func_without_args):
        if isinstance(func_without_args, Isolated):
            raise ValueError("The Evaluated and Isolated types should not be mixed.")

        self.func = func_without_args

    def evaluate(self):
        """
        The method evaluates a value for the default argument using the function which has been passed to the instance.
        :return:
        A result of the function execution.
        """
        return self.func()


class Isolated:
    """
    The class is used to mark an 'isolated' type of default arguments of functions.
    Its instances have no arguments and serve as a fictive value.
    """

    def __init__(self):
        pass


def smart_args(func):
    """
    The decorator for analyzing the types 'evaluated/isolated' of default arguments of functions and processing the
    arguments.

    :param func:
    A function which should be processed.

    :return:
    The wrapped function
    """

    def wrapper(**kwargs):
        """
        The function serves as a wrapper for the original function.

        :param kwargs:
        Keyword-only arguments for the function.

        :return:
        The result of the original function executed with the modified arguments.
        """
        # we are going to use the 'inspect' module to handle arguments of a function
        sig = inspect.signature(func)

        # collecting all keyword-only arguments of the function into a dictionary and setting defaults values
        args = sig.bind(**kwargs)
        args.apply_defaults()
        args_dict = args.arguments

        # iterating through the arguments dictionary
        for name, value in args_dict.items():
            param = sig.parameters[name]

            # calculating a value for the defaults with 'evaluated' type
            if isinstance(param.default, Evaluated) and value == param.default:
                kwargs[name] = param.default.evaluate()

            # making a deep copy of an argument for the defaults with 'isolated' type
            elif isinstance(param.default, Isolated):
                kwargs[name] = copy.deepcopy(value)

        # returning the original function executed with the modified arguments
        return func(**kwargs)

    return wrapper
