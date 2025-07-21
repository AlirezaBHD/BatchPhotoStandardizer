from os import sep

def shorten_path(path, max_length):
    parts = path.split(sep)
    result = []

    while parts and len(sep.join(result)) + len(parts[-1]) + 1 <= max_length:
        result.insert(0, parts.pop())

    return sep + sep.join(result)


def column_to_int(value):
    if type(value) == str:
        return int(ord(value) - 65)
    return ""