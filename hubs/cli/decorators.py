from functools import wraps
from argparse import ArgumentParser

def cli(*args, **kwargs):
    def decorator(func):
        class Parser(ArgumentParser):
            def handle(self, *args, **kwargs):
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    self.error(e.message)

            def handle_raw(self, *args, **kwargs):
                func(*args, **kwargs)

        return Parser(*args, **kwargs)
    return decorator
