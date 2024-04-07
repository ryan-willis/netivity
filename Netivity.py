import rumps
import socket
import subprocess
import re
import bandwidth


class Netivity:
    def __init__(self):
        interfaces = sorted([name for _, name in socket.if_nameindex()])

        # TODO: python mechanism to get default interface name rather than system cli tool
        defroute = subprocess.check_output(["route", "get", "default"])
        match = re.search(r"interface: (.+)\n", defroute.decode(), re.MULTILINE)
        if match and match.group(1) in interfaces:
            self.interface = match.group(1)
        else:
            self.interface = interfaces[0]

        self.params = bandwidth.Params(0, 0, 0, 0, self.interface.encode())
        self.app = rumps.App("Netitivy", "👾")
        items = [
            rumps.MenuItem(
                title=self.interface_title(interface), callback=self.switch_interface
            )
            for interface in interfaces
        ]
        items.append(rumps.separator)
        self.app.menu = items

        self.timer = rumps.Timer(self.tick, 1)
        self.timer.start()
        self.app.run()

    def interface_title(self, interface):
        if interface == self.interface:
            return f"{interface} (default)"
        else:
            return interface

    def switch_interface(self, sender):
        self.interface = sender.title.rstrip(" (default)")
        self.params.last_out = 0
        self.params.last_in = 0
        self.params.net_in = 0
        self.params.net_out = 0
        self.params.ifa_name = self.interface.encode()

    def tick(self, *_):
        self.app.title = bandwidth.retrieve(self.params)


def main():
    Netivity()


if __name__ == "__main__":
    main()
