import functools


class CallCounter:
    """
    A simple class that contains a decorator to count method invocations
    """

    # def __init__(self, func):
    #     self.call_count = 0
    #     self.func = func
    #
    # def __call__(self, *args, **kwargs):
    #     self.call_count += 1
    #     return self.func(*args, **kwargs)
    #
    # def reset(self):
    #     self.call_count = 0

    @staticmethod
    def count_calls(func):
        """
        Decorates a function with a counter
        :param func: The function to count
        :return: Returns a wrapper that counts the number of times `func` is called
        """
        @functools.wraps(func)
        def counter(*args, **kwargs):
            counter.call_count += 1
            return func(*args, **kwargs)

        counter.call_count = 0
        counter.reset = lambda: setattr(counter, 'call_count', 0)
        return counter
