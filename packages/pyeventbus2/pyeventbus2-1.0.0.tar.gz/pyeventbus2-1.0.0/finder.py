import inspect
import tokenize
from typing import List, Optional, Callable


class BlockFinderDecorator(inspect.BlockFinder):

    def get_block_lines(self, lines):
        """Extract the block of code at the top of the given list of lines."""
        try:
            tokens = tokenize.generate_tokens(iter(lines).__next__)
            for _token in tokens:
                self.tokeneater(*_token)
        except (inspect.EndOfBlock, IndentationError):
            pass
        return lines[:self.last], self

    def get_block_finder(self):
        return self

    def get_token_line(self, lines: List):

        try:
            tokens = tokenize.generate_tokens(iter(lines).__next__)
            for _token in tokens:
                self.tokeneater(*_token)
                if self.indecorator: return _token.line.strip()
        except (inspect.EndOfBlock, IndentationError):
            pass

        return

    def is_decorated_by(self, token: str, clazz: type) -> List[Callable]:
        _decorated_function_list = []
        for func in dir(clazz):
            if not func.startswith("__"):
                _func = getattr(clazz, func)
                if callable(_func):
                    res = self.get_token_line(inspect.getsourcelines(_func)[0])
                    if bool(res) and token in res:
                        _decorated_function_list.append(_func)
        return _decorated_function_list

    def find_method(self, method: str, clazz: type) -> bool:
        lines = inspect.getsourcelines(clazz)[0]
        for line in lines:
            # _pattern = f"def {method}(self, msg:"
            # res = re.findall(r"def {method}(self, msg:*):".format(method=method), line)
            # if bool(res): return True
            if f"def {method}(self, msg:" in line:
                return True

        return False

    def get_args(self, func):
        # _args = inspect.getfullargspec(func).args
        # inspect.ArgInfo
        res = inspect.getfullargspec(func)
        return res

    # def do_execute(self, func_name, clazz: type):
    #     if self.is_decorated_by(func_name, clazz):
    #         pass
    # print(f"{_func.__name__} is decorated by {res}")
    # _args = inspect.getfullargspec(_func).args
    # result = _func(*_args)
    # print(result)
