from ctypes import CDLL, POINTER, Structure, c_uint64, c_char, byref


class Params(Structure):
    _fields_ = [
        ("last_out", c_uint64),
        ("last_in", c_uint64),
        ("net_in", c_uint64),
        ("net_out", c_uint64),
        ("ifa_name", c_char * 16),
    ]


dylib = CDLL("bandwidth.dylib")
get_bandwidth = dylib.get_bandwidth
get_bandwidth.argtypes = [POINTER(Params)]


def human_rate(bytes):
    i = 0
    suffixes = ["B", "K", "M"]
    while bytes >= 1024 and i < len(suffixes) - 1:
        bytes /= 1024.0
        i += 1
    return "%d%s" % (bytes, suffixes[i])


def format_human(p: Params):
    iface = p.ifa_name.decode()
    net_in = human_rate(p.net_in)
    net_out = human_rate(p.net_out)
    return f"{iface}⬆{net_out}⬇{net_in}"


def retrieve(p: Params):
    get_bandwidth(byref(p))
    return format_human(p)
