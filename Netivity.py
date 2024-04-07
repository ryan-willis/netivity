from threading import Thread
import rumps

from bandwidth import loop, ptr


class Netivity:
    def __init__(self):
        self.app = rumps.App("Netitivy", "👾")
        self.timer = rumps.Timer(self.tick, 1)

    def tick(self, *_):
        self.app.title = ptr[0]

    def run(self):
        self.stats_thread = Thread(target=loop)
        self.stats_thread.start()
        self.timer.start()
        self.app.run()


if __name__ == "__main__":
    Netivity().run()
