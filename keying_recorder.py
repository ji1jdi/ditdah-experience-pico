from machine import Timer
from time import ticks_ms, ticks_diff

class KeyingRecorder:
    def __init__(self, emitter, timeout):
        self._emitter = emitter
        self._timeout = timeout

        self._keying = False
        self._timer = Timer()
        self._t0 = 0
        self._t1 = 0
        self._durations = []

    def on(self):
        if self._keying:
            return

        self._keying = True
        self._t0 = ticks_ms()
        print("key down")

        self._timer.deinit()

    def off(self):
        if not self._keying:
            return

        self._keying = False

        self._t1 = ticks_ms()

        d = ticks_diff(self._t1, self._t0)
        if d < 10:
            return

        print(f"key up {d}ms")

        self._durations.append(d)

        self._timer.init(mode=Timer.ONE_SHOT, period=self._timeout, callback=self.timeout)

    def timeout(self, timer):
        if self._keying:
            self._timer.init(mode=Timer.ONE_SHOT, period=self._timeout, callback=self.timeout)
            return

        self._emitter.emit("keyingTimeout", self._durations)

        self._durations.clear()
