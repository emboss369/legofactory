import time
import argparse
from gpiozero import DigitalOutputDevice
from pymodbus.client.sync import ModbusTcpClient
# from w1thermsensor import W1ThermSensor

# GPIOピン設定
IN1, IN2, IN3, IN4 = 17, 27, 22, 23
# GPIO ピン番号を指定して DigitalOutputDevice を作成
coil_pins = [
    DigitalOutputDevice(IN1),
    DigitalOutputDevice(IN2),
    DigitalOutputDevice(IN3),
    DigitalOutputDevice(IN4)
]

# ステッピングモータ制御用シーケンス（1-2相励磁方式）
sequence = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

# 温度センサー設定
# sensor = W1ThermSensor()
# TEMP_THRESHOLD = 50

# Modbus TCP設定
PLC_IP = '127.0.0.1'
PLC_PORT = 502
client = ModbusTcpClient(PLC_IP, port=PLC_PORT)

# モータ動作関数
def step_motor():
    for step in sequence:
        for pin, value in zip(coil_pins, step):
            pin.value = value
        time.sleep(0.01)  # 10ms delay

def test_mode(steps=512):
    for _ in range(steps):
        step_motor()

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
