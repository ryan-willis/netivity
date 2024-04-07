from ctypes import CDLL, POINTER, Structure, c_uint64, c_char, byref
from time import sleep


class Params(Structure):
    _fields_ = [
        ("last_out", c_uint64),
        ("last_in", c_uint64),
        ("net_in", c_uint64),
        ("net_out", c_uint64),
        ("ifa_name", c_char * 16),
    ]


def human_rate(bytes):
    i = 0
    suffixes = ["B", "K", "M"]
    while bytes >= 1024 and i < len(suffixes) - 1:
        bytes /= 1024.0
        i += 1
    return "%d%s" % (bytes, suffixes[i])


ptr = [""]


def print_human(p: Params):
    iface = params.ifa_name.decode()
    net_in = human_rate(p.net_in)
    net_out = human_rate(p.net_out)
    ptr[0] = f"{iface}⬇{net_in}⬆{net_out}"


get_bandwidth = CDLL("bandwidth.dylib").get_bandwidth
get_bandwidth.argtypes = [POINTER(Params)]

params = Params(0, 0, 0, 0, b"en0")


def loop():
    while True:
        get_bandwidth(byref(params))
        print_human(params)
        sleep(1)