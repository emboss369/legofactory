#timeモジュールをインポート
import time

# gpiozeroモジュールからDigitalOutputDeviceとDeviceをインポート
from gpiozero import DigitalOutputDevice, Device
import gpiozero.pins.lgpio
import lgpio

# https://github.com/gpiozero/gpiozero/issues/1166
def __patched_init(self, chip=None):
    gpiozero.pins.lgpio.LGPIOFactory.__bases__[0].__init__(self)
    chip = 0
    self._handle = lgpio.gpiochip_open(chip)
    self._chip = chip
    self.pin_class = gpiozero.pins.lgpio.LGPIOPin

gpiozero.pins.lgpio.LGPIOFactory.__init__ = __patched_init

# MockFactoryを使用するように設定
#Device.pin_factory = MockFactory()

LED=18

# GPIO ピン番号を指定して DigitalOutputDevice を作成
led = DigitalOutputDevice(LED)

while True:
    # LEDの出力を1にして、LED点灯
    led.on()


    # 0.5秒待つ
    time.sleep(0.5)

    # LEDの出力を0にして、LED消灯
    led.off()

    # 0.5秒待つ
    time.sleep(0.5)

