
class Timer:
    def __init__(self, duration:float, callback) -> None:
        self.duration = duration
        self.callback = callback
        self.time = 0.0
        self.is_finished = False

    def update(self, dt:float):
        if (self.is_finished): return
        self.time += dt
        if (self.time >= self.duration):
            self.callback()
            self.is_finished = True

class TimerManager:
    def __init__(self) -> None:
        self.timers:list[Timer] = []
    
    def add_timer(self, delay:float, callback):
        self.timers.append(
            Timer(duration=delay, callback=callback)
        )
        print(f"Timer ajouté {delay}s")

    def update(self, delta_time:float):
        for timer in self.timers:
            timer.update(delta_time)
        self.timers = [t for t in self.timers if not t.is_finished]