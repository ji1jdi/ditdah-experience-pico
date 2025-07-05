import settings
import ssd1306
from machine import Pin, PWM, I2C
from time import sleep_ms
from emitter import Emitter
from buzzer import Buzzer
from manual_keyer import ManualKeyer
from keying_recorder import KeyingRecorder
from display import Display
from code_map import QOD1_MAP

dit_pin = Pin(settings.DIT_PIN, Pin.IN, Pin.PULL_UP)
dah_pin = Pin(settings.DAH_PIN, Pin.IN, Pin.PULL_UP)

emitter = Emitter()

keyer = ManualKeyer(emitter)

buzzer = Buzzer(PWM(Pin(settings.BUZZER_PIN)))
buzzer.frequency = settings.PITCH_DEFAULT
emitter.on("on", buzzer.on)
emitter.on("off", buzzer.off)

recorder = KeyingRecorder(emitter, settings.KEYING_TIMEOUT)
emitter.on("on", recorder.on)
emitter.on("off", recorder.off)
emitter.on("keyingTimeout", lambda e: keying_timeout(e))

i2c = I2C(0, sda=Pin(settings.OLED_SDA_PIN), scl=Pin(settings.OLED_SCL_PIN))
oled = ssd1306.SSD1306_I2C(settings.OLED_WIDTH, settings.OLED_HEIGHT, i2c)
display = Display(oled)

def keying_timeout(durations):
    def by_ratio(dmin, d):
        return "-" if d >= dmin * settings.DASH_RATIO else "."

    def by_duration(d):
        return "-" if d >= settings.DOT_DURATION else "."

    def analyze(durations):
        dmin = min(durations)

        marks = [by_ratio(dmin, d) for d in durations]

        if len(set(marks)) == 1:
            marks = [by_duration(d) for d in durations]

        return "".join(marks)

    def decode(code):
        return QOD1_MAP.get(code, " ")

    marks = analyze(durations)
    c = decode(marks)

    display.show(c)
    print(c)

def loop():
    keyer.handler(not dit_pin.value(), not dah_pin.value())

def main():
    while True:
        loop()
        sleep_ms(1)

if __name__ == "__main__":
    main()
