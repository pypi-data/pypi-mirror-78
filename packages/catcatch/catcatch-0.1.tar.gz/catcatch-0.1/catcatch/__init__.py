class ExceptionWithName:
    def __init__(self, name: str, text: str):
        self.name = name
        self.text = text

    def __repr__(self):
        return self.name + ": " + self.text


def catch(function):
    """This decorator catch exceptions and return it with exception name and text"""

    def decorator(*args, **kwargs):
        try:
            return function(*args, **kwargs)  # If there are no errors
        except Warning as e:
            return ExceptionWithName("Warning", str(e))

        except UnicodeTranslateError as e:
            return ExceptionWithName("UnicodeTranslateError", str(e))

        except UnicodeDecodeError as e:
            return ExceptionWithName("UnicodeDecodeError", str(e))

        except UnicodeEncodeError as e:
            return ExceptionWithName("UnicodeEncodeError", str(e))

        except UnicodeError as e:
            return ExceptionWithName("UnicodeError", str(e))

        except ValueError as e:
            return ExceptionWithName("ValueError", str(e))

        except TypeError as e:
            return ExceptionWithName("TypeError", str(e))

        except SystemError as e:
            return ExceptionWithName("SystemError", str(e))

        except TabError as e:
            return ExceptionWithName("TabError", str(e))

        except IndentationError as e:
            return ExceptionWithName("IndentationError", str(e))

        except SyntaxError as e:
            return ExceptionWithName("SyntaxError", str(e))

        except NotImplementedError as e:
            return ExceptionWithName("NotImplementedError", str(e))

        except RuntimeError as e:
            return ExceptionWithName("RuntimeError", str(e))

        except ReferenceError as e:
            return ExceptionWithName("ReferenceError", str(e))

        except TimeoutError as e:
            return ExceptionWithName("TimeoutError", str(e))

        except ProcessLookupError as e:
            return ExceptionWithName("ProcessLookupError", str(e))

        except PermissionError as e:
            return ExceptionWithName("PermissionError", str(e))

        except NotADirectoryError as e:
            return ExceptionWithName("NotADirectoryError", str(e))

        except InterruptedError as e:
            return ExceptionWithName("InterruptedError", str(e))

        except FileNotFoundError as e:
            return ExceptionWithName("FileNotFoundError", str(e))

        except FileExistsError as e:
            return ExceptionWithName("FileExistsError", str(e))

        except ConnectionResetError as e:
            return ExceptionWithName("ConnectionResetError", str(e))

        except ConnectionAbortedError as e:
            return ExceptionWithName("ConnectionAbortedError", str(e))

        except BrokenPipeError as e:
            return ExceptionWithName("BrokenPipeError", str(e))

        except ConnectionError as e:
            return ExceptionWithName("ConnectionError", str(e))

        except ChildProcessError as e:
            return ExceptionWithName("ChildProcessError", str(e))

        except BlockingIOError as e:
            return ExceptionWithName("BlockingIOError", str(e))

        except OSError as e:
            return ExceptionWithName("OSError", str(e))

        except UnboundLocalError as e:
            return ExceptionWithName("UnboundLocalError", str(e))

        except NameError as e:
            return ExceptionWithName("NameError", str(e))

        except MemoryError as e:
            return ExceptionWithName("MemoryError", str(e))

        except KeyError as e:
            return ExceptionWithName("KeyError", str(e))

        except IndexError as e:
            return ExceptionWithName("IndexError", str(e))

        except LookupError as e:
            return ExceptionWithName("LookupError", str(e))

        except ImportError as e:
            return ExceptionWithName("ImportError", str(e))

        except EOFError as e:
            return ExceptionWithName("EOFError", str(e))

        except BufferError as e:
            return ExceptionWithName("BufferError", str(e))

        except AttributeError as e:
            return ExceptionWithName("AttributeError", str(e))

        except AssertionError as e:
            return ExceptionWithName("AssertionError", str(e))

        except ZeroDivisionError as e:
            return ExceptionWithName("ZeroDivisionError", str(e))

        except OverflowError as e:
            return ExceptionWithName("OverflowError", str(e))

        except FloatingPointError as e:
            return ExceptionWithName("FloatingPointError", str(e))

        except ArithmeticError as e:
            return ExceptionWithName("ArithmeticError", str(e))

        except StopIteration as e:
            return ExceptionWithName("StopIteration", str(e))

        except Exception as e:
            return ExceptionWithName("Error", str(e))
    return decorator
