import threading
from itertools import islice as _islice, count as _count
import time
import _thread
import sys as _sys
import _thread
from time import monotonic as _time
from traceback import format_exc as _format_exc
from _weakrefset import WeakSet
try:
    from _collections import deque as _deque
except ImportError:
    from collections import deque as _deque
# from app.ik_global import ik_global
_counter = _count().__next__
_start_new_thread = _thread.start_new_thread
_allocate_lock = _thread.allocate_lock
_set_sentinel = _thread._set_sentinel
get_ident = _thread.get_ident
ThreadError = _thread.error

# Active thread administration
_active_limbo_lock = _allocate_lock()
_active = {}    # maps thread id to Thread object
_limbo = {}
# _dangling = WeakSet()

# Support for profile and trace hooks

_profile_hook = None
_trace_hook = None


def settrace(func):
    """Set a trace function for all threads started from the threading module.

    The func will be passed to sys.settrace() for each thread, before its run()
    method is called.

    """
    global _trace_hook
    _trace_hook = func


def _newname(template="DaemonThreadTimer-%d"):
    return template % _counter()

# Global API functions


def current_thread():
    """Return the current Thread object, corresponding to the caller's thread of control.

    If the caller's thread of control was not created through the threading
    module, a dummy thread object with limited functionality is returned.

    """
    try:
        return _active[get_ident()]
    except KeyError:
        return _DummyThread()


class _DummyThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self, name=_newname("Dummy-%d"), daemon=True)

        self._started.set()
        self._set_ident()
        with _active_limbo_lock:
            _active[self._ident] = self

    def _stop(self):
        pass

    def is_alive(self):
        assert not self._is_stopped and self._started.is_set()
        return True

    def join(self, timeout=None):
        assert False, "cannot join a dummy thread"


class DaemonThreadTimer(threading.Thread):

    def __init__(self, interval, function, name=None, daemon=True, args=None, kwargs=None):
        threading.Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.finished = threading.Event()
        self.__result = None
        self._name = str(name or _newname())
        print("self._name: {}".format(self._name))
        # self.daemon = daemon
        if daemon is not None:
            self._daemonic = daemon
        else:
            self._daemonic = current_thread().daemon
        print("self._daemonic: {}".format(self._daemonic))
        self._initialized = True

    def cancel(self):
        """Stop the timer if it hasn't finished yet."""
        self.finished.set()

    def run(self):
        # 循环执行
        # while not self.finished.wait(self.interval):
        #     self.__result = self.function(*self.args)
        #     ik_global.Logger.warning("run result: {}".format(self.__result))

        # 单次执行
        # self.finished.wait(self.interval)
        # if not self.finished.is_set():
        #     self.__result = self.function(*self.args, **self.kwargs)
        #     # ik_global.Logger.warning("run result: {}".format(self.__result))
        # self.finished.set()
        """
        Method representing the thread's activity.

        You may override this method in a subclass. The standard run() method
        invokes the callable object passed to the object's constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.

        """
        try:
            print("self.__result: ", self.__result)
            print("self.function: ", self.function)
            # if self.function:
            self.__result = self.function(*self._args, **self._kwargs)
            # print("self.__result: ", self.__result)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self.function, self._args, self._kwargs

    @property
    def name(self):
        """A string used for identification purposes only.

        It has no semantics. Multiple threads may be given the same name. The
        initial name is set by the constructor.

        """
        assert self._initialized, "DaemonThreadTimer.__init__() not called"
        return self._name

    @name.setter
    def name(self, name):
        assert self._initialized, "DaemonThreadTimer.__init__() not called"
        self._name = str(name)

    @property
    def daemon(self):
        """A boolean value indicating whether this thread is a daemon thread.

        This must be set before start() is called, otherwise RuntimeError is
        raised. Its initial value is inherited from the creating thread; the
        main thread is not a daemon thread and therefore all threads created in
        the main thread default to daemon = False.

        The entire Python program exits when no alive non-daemon threads are
        left.

        """
        assert self._initialized, "Thread.__init__() not called"
        return self._daemonic

    @daemon.setter
    def daemon(self, daemonic):
        if not self._initialized:
            raise RuntimeError("Thread.__init__() not called")
        if self._started.is_set():
            raise RuntimeError("cannot set daemon status of active thread")
        self._daemonic = daemonic

    def isDaemon(self):
        return self.daemon

    def setDaemon(self, daemonic):
        self.daemon = daemonic

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    @property
    def result(self):
        return self.__result

    # def start(self):
    #     threading.Thread.start(self)
    def start(self):
        """Start the thread's activity.

        It must be called at most once per thread object. It arranges for the
        object's run() method to be invoked in a separate thread of control.

        This method will raise a RuntimeError if called more than once on the
        same thread object.

        """
        if not self._initialized:
            raise RuntimeError("thread.__init__() not called")

        if self._started.is_set():
            raise RuntimeError("threads can only be started once")
        with _active_limbo_lock:
            _limbo[self] = self
        try:
            print("----->")
            _start_new_thread(self._bootstrap, ())
        except Exception:
            with _active_limbo_lock:
                del _limbo[self]
            raise
        self._started.wait()

    def _bootstrap(self):
        # Wrapper around the real bootstrap code that ignores
        # exceptions during interpreter cleanup.  Those typically
        # happen when a daemon thread wakes up at an unfortunate
        # moment, finds the world around it destroyed, and raises some
        # random exception *** while trying to report the exception in
        # _bootstrap_inner() below ***.  Those random exceptions
        # don't help anybody, and they confuse users, so we suppress
        # them.  We suppress them only when it appears that the world
        # indeed has already been destroyed, so that exceptions in
        # _bootstrap_inner() during normal business hours are properly
        # reported.  Also, we only suppress them for daemonic threads;
        # if a non-daemonic encounters this, something else is wrong.
        try:
            print("----->")
            self._bootstrap_inner()
        except:
            if self._daemonic and _sys is None:
                return
            raise

    def _bootstrap_inner(self):
        try:
            self._set_ident()
            self._set_tstate_lock()
            self._started.set()
            with _active_limbo_lock:
                _active[self._ident] = self
                del _limbo[self]

            if _trace_hook:
                _sys.settrace(_trace_hook)
            if _profile_hook:
                _sys.setprofile(_profile_hook)

            try:
                print("----->")
                self.run()
            except SystemExit:
                pass
            except:
                # If sys.stderr is no more (most likely from interpreter
                # shutdown) use self._stderr.  Otherwise still use sys (as in
                # _sys) in case sys.stderr was redefined since the creation of
                # self.
                if _sys and _sys.stderr is not None:
                    print("Exception in thread %s:\n%s" %
                          (self.name, _format_exc()), file=_sys.stderr)
                elif self._stderr is not None:
                    # Do the best job possible w/o a huge amt. of code to
                    # approximate a traceback (code ideas from
                    # Lib/traceback.py)
                    exc_type, exc_value, exc_tb = self._exc_info()
                    try:
                        print((
                            "Exception in thread " + self.name +
                            " (most likely raised during interpreter shutdown):"), file=self._stderr)
                        print((
                            "Traceback (most recent call last):"), file=self._stderr)
                        while exc_tb:
                            print((
                                '  File "%s", line %s, in %s' %
                                (exc_tb.tb_frame.f_code.co_filename,
                                    exc_tb.tb_lineno,
                                    exc_tb.tb_frame.f_code.co_name)), file=self._stderr)
                            exc_tb = exc_tb.tb_next
                        print(("%s: %s" % (exc_type, exc_value)),
                              file=self._stderr)
                    # Make sure that exc_tb gets deleted since it is a memory
                    # hog; deleting everything else is just for thoroughness
                    finally:
                        del exc_type, exc_value, exc_tb
            finally:
                # Prevent a race in
                # test_threading.test_no_refcycle_through_target when
                # the exception keeps the target alive past when we
                # assert that it's dead.
                # XXX self._exc_clear()
                pass
        finally:
            with _active_limbo_lock:
                try:
                    # We don't call self._delete() because it also
                    # grabs _active_limbo_lock.
                    del _active[get_ident()]
                except:
                    pass


class DaemonThreadTimer2(threading.Timer):

    def __init__(self, interval, function, args=None, kwargs=None):
        threading.Timer.__init__(self, interval, function)
        self.interval = interval
        self.function = function
        self.args = args if args else ()
        self.kwargs = kwargs if kwargs else {}
        self.__result = None
        self.finished = threading.Event()

    def run(self):
        self.finished.wait(self.interval)
        # print("self.__result: {}".format(self.__result))
        if not self.finished.is_set():
            self.__result = self.function(*self.args, **self.kwargs)
        self.finished.set()

    @property
    def result(self):
        return self.__result

    @staticmethod
    def static_method():
        pass

    @classmethod
    def get_instance(cls, *args, **kwargs):
        pass


def pprint(arg):
    # print("{}: {}".format(arg, time.time()))
    return "{}: {}".format(arg, time.time())


def printf():
    return "printf called"


def set_interval(interval, func, args=()):
    # print(type(interval))
    # print(type(func))
    assert any([type(func) == type(C().sm), type(
        func) == type(C().m)]), "not any"
    t = DaemonThreadTimer2(
        interval=interval, function=func, args=args)
    t.daemon = True
    t.name = "test"
    # t.start()
    t.run()
    # ik_global.Logger.info("result: {}".format(t.result))
    set_interval(interval=interval, func=func, args=args)


def __func():
    pass


class C():

    @staticmethod
    def sm():
        pass

    def m(self):
        pass


if __name__ == '__main__':
    # crawler = Crawler(symbol='BTCUSD', output_file='BTCUSD.txt')
    # t = DaemonThreadTimer2(
    #     interval=2, function=pprint, args=("shiss",))
    # t.daemon = True
    # t.name = "test"
    # # t.start()
    # t.run()
    # print(t.result)
    # set_interval(interval=2, func=pprint, args=("sss",))
    set_interval(interval=2, func=printf)

    # assert any([type(set_interval) == type(C().sm), type(set_interval) == type(C().m)]), "not any"
    # assert type(set_interval) == type(C.m), "not "

    # assert (any([type(set_interval) == "<class 'function'>", type(t.run) == "<class 'method'>"])), "must be function or method"
    # print(type(set_interval))
    # print(type(t.run))
    # print(type(t.static_method))
    # print(type(t.get_instance))
    print(type(C.m))  # 实例化前世function
    print(type(C().m))  # 实例化后是method
