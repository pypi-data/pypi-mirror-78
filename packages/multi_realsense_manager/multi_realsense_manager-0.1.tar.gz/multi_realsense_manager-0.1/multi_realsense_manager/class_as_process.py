#!/usr/bin/env python3


def class_as_process(cls, init_args=None, init_kwargs=None, dummy=False):
    if dummy:
        from multiprocessing.dummy import Process, Pipe
    else:
        from multiprocessing import Process, Pipe

    class ClassAsProcess(Process):
        def __init__(self, cls, init_args=None, init_kwargs=None):
            if init_args is None:
                init_args = []
            if init_kwargs is None:
                init_kwargs = {}
            self._dirs = set(dir(self))
            self.conn, conn_child = Pipe()
            super().__init__(
                target=self.new_process, args=(cls, init_args, init_kwargs, conn_child)
            )
            self.start()

        @staticmethod
        def new_process(cls, init_args, init_kwargs, conn):
            instance = cls(*init_args, **init_kwargs)

            def listen():
                while True:
                    rev = conn.recv()
                    if rev is None:
                        break
                    if isinstance(rev, dict):
                        if "method" in rev:
                            func = getattr(instance, rev["method"])
                            re = func(*rev.get("args", []), **rev.get("kwargs", {}))
                            conn.send(re)

            if getattr(instance, "__enter__", None) and getattr(
                instance, "__exit__", None
            ):
                with instance:
                    listen()
            else:
                listen()

        def terminate(self):
            self.conn.send(None)

        def __getattr__(self, key):
            def func(*args, **kwargs):
                self.conn.send(dict(method=key, args=args, kwargs=kwargs))
                return self.conn.recv()

            return func

    return ClassAsProcess(cls, init_args, init_kwargs)


if __name__ == "__main__":
    # test
    class A:
        def __enter__(self):
            print("__enter__")
            return self

        def __exit__(self, *args):
            print("__exit__")

        def test(self, *args, **kwargs):
            return f"call args: {args} kwargs: {kwargs}"

    a = class_as_process(A, dummy=0)
    print(a.test(1, 2, a="a", b="b"))
    a.terminate()
    a.join()
