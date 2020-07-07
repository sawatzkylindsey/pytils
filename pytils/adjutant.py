
import numbers

from pytils import check


def dict_as_str(d, sort_by_key=True, reverse=False, digits=4):
    if len(d) == 0:
        return "{}"

    out = []

    def _form(item):
        form = "s"

        if isinstance(item, int):
            form = "d"
        elif isinstance(item, float) or isinstance(item, numbers.Number):
            form = ".%df" % digits

        return form

    def _pre_format(item):
        if isinstance(item, dict):
            return dict_as_str(item, sort_by_key, reverse, digits)
        elif isinstance(item, tuple) or isinstance(item, list) or isinstance(item, set):
            return str(item)
        else:
            return item

    first_key = next(iter(d.keys()))
    first_value = d[first_key]

    if isinstance(first_value, dict) and not sort_by_key:
        raise ValueError("Cannot sort_by_value with dict values.")

    template = "{:%s}: {:%s}" % (_form(first_key), _form(first_value))

    for key, value in sorted(d.items(), key=lambda item: item[0] if sort_by_key else item[1], reverse=reverse):
        out.append(template.format(_pre_format(key), _pre_format(value)))

    return "{%s}" % ", ".join(out)


def str_as_bool(value):
    v = value.lower().trim()

    if v in ["yes", "true", "t", "1"]:
        return True
    elif v in ["no", "false", "f", "0"]:
        return False
    else:
        raise ValueError("Cannot convert '%s' to boolean value." % value)


def dict_invert(d):
    out = {}

    for key, value in d.items():
        if value not in out:
            out[value] = key
        else:
            raise ValueError("Cannot invert dictionary - duplicate key: '%s'." % (value))

    return out


def flat_map(sequence):
    return [i for item in sequence for i in item]


def rindex(sequence, value):
    i = len(sequence) - 1

    while i >= 0:
        if sequence[i] == value:
            return i

        i -= 1

    return None


class Closing:
    def __init__(self, handle_fn, close_fn):
        self.handle_fn = check.check_function(handle_fn)
        self.close_fn = check.check_function(close_fn)

    def __enter__(self):
        return self.handle_fn()

    def __exit__(self, exception_type, exception, traceback):
        self.close_fn()


class AutoClosing(Closing):
    def __init__(self, item):
        super().__init__(lambda: item, lambda: item.close())


class Closeable:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception, traceback):
        self.close()

    def close(self):
        raise NotImplementedError()

