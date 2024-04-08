import bandwidth
import rumps
import subprocess
import re
import prefs

# import socket


class Netivity(prefs.Prefs):
    def __init__(self):
        self.app = rumps.App("Netitivy", "👾")
        self.timer = rumps.Timer(self.tick, 1)

        self.init_interfaces()
        self.init_menu()

        self.load_prefs()
        self.apply_prefs(self.app)

        self.params = bandwidth.Params(0, 0, 0, 0, self.interface.encode())

        self.timer.start()
        self.app.run()

    def init_interfaces(self):
        self.interface = None
        self.load_interfaces()

    def init_menu(self):
        items = ["Paused while open", None]
        items.append(
            (
                "Interfaces",
                [
                    rumps.MenuItem(
                        title=interface,
                    )
                    for interface in self.interfaces
                ],
            )
        )
        items.append(
            (
                "Settings",
                [
                    rumps.MenuItem(
                        "Shorten `utun` to `t` in the menu bar",
                        callback=self.shorten_utun,
                    ),
                    rumps.MenuItem(
                        "Shorten `en` to `e` in the menu bar",
                        callback=self.shorten_en,
                    ),
                ],
            )
        )
        self.app.menu = items
        self.set_interface_menu_items()

    def set_interface_menu_items(self):
        interfaces_menu = self.app.menu["Interfaces"]
        interfaces_menu.clear()
        for interface in self.interfaces:
            interfaces_menu.add(
                rumps.MenuItem(
                    title=interface,
                    callback=self.switch_interface,
                )
            )
        for item in interfaces_menu:
            if item == self.interface:
                interfaces_menu[item].state = True

    def load_interfaces(self):
        # interfaces = sorted([name for _, name in socket.if_nameindex()])
        self.active_interfaces = dict()

        # TOOD: python/C mechanism to get the interfaces with active routes
        # NOTE: this parsing is silly I know
        inet_routes = subprocess.check_output(["netstat", "-rnf", "inet"])
        lines = inet_routes.decode().splitlines()
        for line in lines:
            parts = re.split(r"\s+", line)
            if parts[0] == "Destination" or len(parts) < 4:
                continue
            iface = parts[3]
            # default route is always the first in the table
            if self.interface is None:
                self.interface = iface
            self.active_interfaces[iface] = True

        self.interfaces = sorted([iface for iface, _ in self.active_interfaces.items()])
        if self.interface not in self.interfaces:
            self.set_interface(self.interfaces[0])

    def shorten_utun(self, sender):
        sender.state = not sender.state
        self.write_pref("shorten_utun", sender.state)

    def shorten_en(self, sender):
        sender.state = not sender.state
        self.write_pref("shorten_en", sender.state)

    def switch_interface(self, sender):
        sender.state = True
        interfaces_menu = self.app.menu["Interfaces"]
        for item in interfaces_menu:
            if item != sender.title:
                interfaces_menu[item].state = False

        self.set_interface(sender.title)

    def set_interface(self, interface):
        self.interface = interface
        self.params.last_out = 0
        self.params.last_in = 0
        self.params.net_in = 0
        self.params.net_out = 0
        self.params.ifa_name = self.interface.encode()

    def tick(self, *_):
        self.load_interfaces()
        self.set_interface_menu_items()
        title = bandwidth.retrieve(self.params)
        if self.prefs["shorten_en"]:
            title = title.replace("en", "e")
        if self.prefs["shorten_utun"]:
            title = title.replace("utun", "t")
        self.app.title = title


def main():
    Netivity()


if __name__ == "__main__":
    main()
