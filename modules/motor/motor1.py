import time
import argparse
import logging
from gpiozero import DigitalOutputDevice, Device
from pymodbus.client import ModbusTcpClient
# from w1thermsensor import W1ThermSensor
from collections import deque

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

# ログ設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# GPIOピン設定
IN1, IN2, IN3, IN4 = 17, 27, 22, 23
# # GPIO ピン番号を指定して DigitalOutputDevice を作成
# coil_pins = [
#     DigitalOutputDevice(IN1),
#     DigitalOutputDevice(IN2),
#     DigitalOutputDevice(IN3),
#     DigitalOutputDevice(IN4)
# ]
# 出力信号パターンのリストを作成
sig_1 = deque([0, 1, 0, 0])  # 1相励磁
sig_2 = deque([1, 1, 0, 0])  # 2相励磁

# 使用するピン番号
IN_1 = DigitalOutputDevice(IN1)
IN_2 = DigitalOutputDevice(IN2)
IN_3 = DigitalOutputDevice(IN3)
IN_4 = DigitalOutputDevice(IN4)


# 回転させる角度（度単位）
ang = 360

# 角度をパルス数に換算
#p_cnt = int(ang / (5.625 / 64))
p_cnt = int(ang / (5.625 / 32))

# 回転方向（-1: 時計回り, 1: 反時計回り）
dir = 1

# パルス幅（小さいほど速い、0.001以下は回転しない可能性あり）
p_wid = 0.002


# ステッピングモーターを制御する関数
def set_pins(pattern):
    IN_1.value = pattern[0]
    IN_2.value = pattern[1]
    IN_3.value = pattern[2]
    IN_4.value = pattern[3]



# 温度センサー設定
# sensor = W1ThermSensor()
# TEMP_THRESHOLD = 50

# Modbus TCP設定
PLC_IP = '127.0.0.1'
PLC_PORT = 502
client = ModbusTcpClient(PLC_IP, port=PLC_PORT)

# モータ動作関数
def step_motor():
    logging.debug('Stepping motor')
    # for step in sequence:
    #     logging.debug(f'Step: {step}')
    #     for pin, value in zip(coil_pins, step):
    #         logging.debug(f'Setting pin {pin} to {value}')
    #         pin.value = value
    #     time.sleep(0.01)  # 10ms delay

def test_mode(steps=512):
    # logging.info(f'Test mode started with {steps} steps')
    # for i in range(steps):
    #     #logging.info(f'Step {i+1}/{steps}')
    #     step_motor()
    # 時計回りに1回転、反時計回りに1回転する
    global dir, p_cnt, p_wid
    for i in range(2):
        for j in range(p_cnt):
            # if j % 2 == 0:
            #     set_pins(sig_2)
            #     time.sleep(p_wid)
            #     sig_2.rotate(dir)
            # else:
            #     set_pins(sig_1)
            #     time.sleep(p_wid)
            #     sig_1.rotate(dir)
            set_pins(sig_1)
            time.sleep(p_wid)
            sig_1.rotate(dir)
        
        # 回転方向を逆にする
        dir *= -1
        time.sleep(1.0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stepper Motor Control')
    parser.add_argument('--test', action='store_true', help='Enable test mode')
    args = parser.parse_args()

    try:
        if args.test:
            test_mode()
        else:
            while True:
                rr = client.read_coils(1, 1)
                motor_run = rr.bits[0]

                # temperature = sensor.get_temperature()
                # if temperature >= TEMP_THRESHOLD:
                #     client.write_register(40003, 1)
                #     motor_run = False
                # else:
                #     client.write_register(40003, 0)

                client.write_register(40003, 0)

                if motor_run:
                    step_motor()
                else:
                    for pin in coil_pins:
                        pin.off()
                    time.sleep(1)

    except KeyboardInterrupt:
        for pin in coil_pins:
            pin.off()
        client.close()
