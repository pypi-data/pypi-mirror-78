""" Reads and returns Unit Dictionary."""
import pkg_resources
from contextlib import closing
from io import StringIO

def read_dictionary(f):
    if isinstance(f, str):
        try:
            with closing(pkg_resources.resource_stream(__name__, f)) as fp:
                rbytes = fp.read()
                return read_dictionary(StringIO(rbytes.decode('utf-8')))
        except Exception as e:
            msg = getattr(e, 'message', '') or str(e)
            raise ValueError("While opening {}\n{}".format(f, msg))
    d = {}
    file_type = ""
    for line in f:
        if line[0] == "#":
            file_type = line.strip().strip('#')
        items = line.strip().split('=')
        if len(items) >= 2:
            d[items[0].strip()] = items[1:]
    return d, file_type
