import os
import logging
import logging.handlers

from functools import wraps
import inspect

class Logger(object):
    
    def _entry_exit_marker(self, func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            # self.my_logger.info((func.__name__ + "Entry").center(80,'-'))
            print ('<function: ' + func.__name__ + "> Entry").center(80,'*')

            to_return = func(*args, **kwargs)

            # self.my_logger.info((func.__name__ + "Exit").center(80,'-'))
            print ('<function: ' + func.__name__ + "> Exit").center(80,'*')
            return to_return
        return wrapper


    def mark_entry_exit(self, cls_or_func):
        '''Logs entry and exit of a function.
        Classes can be decored if and only if they are New-Style classes.
        '''
        if inspect.isclass(cls_or_func):
            cls = cls_or_func
            if not type(cls) is type:
                # self.my_logger.info('Failed to mark entry exit of %s, Not a new-style class' % cls).center(80,'%')
                print ('<Failed to mark entry exit of %s, Not a new-style class>' % cls).center(100,'%')
                return cls

            def attribute_getter(obj_or_cls, key):
                value = Logger.__getattribute__(obj_or_cls, key)
                if inspect.isroutine(value):
                    return self._entry_exit_marker(value)
                else:
                    return value
            cls.__getattribute__ = attribute_getter
            return cls

        elif inspect.isfunction(cls_or_func):
            func = cls_or_func
            return self._entry_exit_marker(func)
        else:
            raise TypeError('<mark_entry_exit> decorator inappropriately used')

