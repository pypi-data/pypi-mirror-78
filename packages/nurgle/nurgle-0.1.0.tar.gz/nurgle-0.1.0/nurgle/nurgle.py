"""Main module."""

from functools import wraps
from pathlib import Path
import inspect
import logging
from slack import WebClient
from slack.errors import SlackApiError


getargspec = None
if getattr(inspect, 'getfullargspec', None):
    getargspec = inspect.getfullargspec
else:
    # this one is deprecated in Python 3, but available in Python 2
    getargspec = inspect.getargspec


class _Namespace:
    pass

class Nurgle(object):
    def __init__(self, logger_name='nurgle', debug=False, slack_token=None, slack_channel=None, state_file=None):
        self.logger = logging.getLogger(logger_name)
        self.g = _Namespace()
        self.debug = debug
        self.except_ = {}
        self.force_debug = []
        self.force_handle = []
        self.else_ = None
        self.finally_ = None
        self.state_file = Path(state_file) if state_file is not None else None
        self.slack_channel=slack_channel
        self.slack_token=slack_token

    def _notify(self, message):
        if self.slack_channel is None or self.slack_token is None:
            return            
        slack = WebClient(token=self.slack_token)
        try:
            slack.chat_postMessage(channel=f"#{self.slack_channel}", text=message)
        except SlackApiError as e:
            pass
    
    def _update_state(self, e = None):        
        # no state and exception - always notify
        if self.state_file is None and e is not None:
            self._notify(message="ERR: " + str(e))
            return
        
        # no state and no exception - return
        if self.state_file is None:
            return

        # CHECK STATE
        # previous run - with was with error?
        had_error=False
        previous_error="<unknown>"
        if self.state_file.exists():
            had_error=True
            try:
                previous_error=self.state_file.read_text()
            except:
                pass

        # previous attempt was with exception, current is without
        # notify that we have recovered from an error
        if e is None and had_error:
            self._notify(message=f"RECOVERED from: {previous_error}")
            try:
                self.state_file.unlink()
            except:
                pass
            return

        # current attempt is with exception, previous was without or reason changed
        # notify that we have an error and save state        
        if e is not None and (had_error==False or previous_error!=str(e)):            
            self._notify(message="ERR=" +str(e))
            try:
                self.state_file.write_text(str(e))
            except:
                pass
            return

        
            
        
    
    def _try(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            ret = None
            try:
                ret = f(*args, **kwargs)

                # update state - at this stage, 
                # no exception occured, otherwise we would be in except clause
                self._update_state(e=None)

                # note that if the function returned something, the else clause
                # will be skipped. This is a similar behavior to a normal
                # try/except/else block.
                if ret is not None:
                    return ret

            except Exception as e:                                
                # update state - at this stage, we have an exception
                self._update_state(e=e)
                
                # find the best handler for this exception
                handler = None
                for c in self.except_.keys():
                    if isinstance(e, c):
                        if handler is None or issubclass(c, handler):
                            handler = c

                
                # if we don't have any handler, we let the exception bubble up
                if handler is None:
                    raise e
                                
                # log exception
                self.logger.exception('[nurgle] Exception caught')

                # if in debug mode, then bubble up to let a debugger handle
                debug = self.debug
                if handler in self.force_debug:
                    debug = True
                elif handler in self.force_handle:
                    debug = False
                if debug:
                    raise e

                # invoke handler
                if len(getargspec(self.except_[handler])[0]) == 0:
                    return self.except_[handler]()
                else:
                    return self.except_[handler](e)
            else:
                # if we have an else handler, call it now
                if self.else_ is not None:
                    return self.else_()
            finally:
                # if we have a finally handler, call it now
                if self.finally_ is not None:
                    alt_ret = self.finally_()
                    if alt_ret is not None:
                        ret = alt_ret
                    return ret
        return wrapper

    def _except(self, *args, **kwargs):
        def decorator(f):
            for e in args:
                self.except_[e] = f
            d = kwargs.get('debug', None)
            if d:
                self.force_debug.append(e)
            elif d is not None:
                self.force_handle.append(e)
            return f
        return decorator

    def _else(self, f):
        self.else_ = f
        return f

    def _finally(self, f):
        self.finally_ = f
        return f