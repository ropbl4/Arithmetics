import flet
import asyncio


class Countdown(flet.Text):
    def __init__(self, seconds):
        super().__init__()

        self.seconds = seconds

    def did_mount(self):
        self.running = True
        self.page.run_task(self.timer)

    def will_unmount(self):
        self.running = False

