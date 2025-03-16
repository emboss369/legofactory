## LEGOミニ工場プロジェクト詳細設計書

### システム概要

Raspberry PiにOpenPLCを搭載し、LEGOベルトコンベアをステッピングモータ（28BYJ-48 & ULN2003）で駆動。ベルトコンベア上の物体を光センサーで検知し、検知後に一旦停止してカメラで撮影、AI画像認識で選別。NG判定された物品をFS90サーボモータで排出。温度センサーでモータの発熱状況を監視し、安全運転を確保。

### システム構成

- Raspberry Pi 5
- 28BYJ-48 ステッピングモータ & ULN2003 ドライバーボード
- FS90 サーボモータ
- カメラモジュール（Pi Camera）
- 温度センサー（DS18B20）
- 光センサー（フォトレジスタ：CdSセル）＆ 白色LED
- AD変換モジュール（MCP3008）
- LEGO Technic（ベルトコンベア機構）
- 電源（5V DC）

### システム全体のデータフロー

1. ベルトコンベアが28BYJ-48ステッピングモータで駆動。
2. 光センサー（CdSセル）が物体を検知するとベルトコンベアを一旦停止。
3. コンベア上の物体をカメラが撮影。
4. Raspberry Pi上のAIが画像認識で物体のOK/NGを判定。
5. AIが判定結果をOpenPLCへModbus TCP通信で送信。
6. AI判定結果がOpenPLCに送信されると、ベルトコンベアを再開。
7. 再開後、物体がFS90サーボの位置まで移動したら、OpenPLCがFS90サーボを制御し、NG品を排出。
8. 温度センサーがモータ温度を監視、異常温度時はモータを停止。

### 通信設計

- 通信プロトコル：Modbus TCP（ポート502）

#### レジスタ割当て

- 40001：AI判定結果（0=OK, 1=NG）
- 40002：画像処理完了フラグ（0=未処理, 1=処理完了）
- 40003：モータ温度異常フラグ（0=正常, 1=異常）
- 40004：物体検知フラグ（0=未検知, 1=検知）

### GPIO配線詳細（Raspberry Pi 5基準）

| Raspberry Pi 5 ピン    | 用途                                  |
| -------------------- | ----------------------------------- |
| 3.3V (1pin)          | MCP3008電源・基準電圧供給(Vdd,Vref 16,15pin) |
| GND (6pin)           | MCP3008接地(AGND,DGND 14,9pin)        |
| GPIO11 (23pin, SCLK) | SPIクロック信号 (CLK 13pin)               |
| GPIO9 (21pin, MISO)  | SPIデータ出力(MCP→RPi) (Dout 12pin)      |
| GPIO10 (19pin, MOSI) | SPIデータ入力(RPi→MCP) (Din 11pin)       |
| GPIO8 (24pin, CE0)   | SPIチップ選択信号 (CS 10pin)               |
| GPIO4                | 温度センサー（DS18B20）データ                  |
| GPIO17               | ULN2003 IN1                         |
| GPIO27               | ULN2003 IN2                         |
| GPIO22               | ULN2003 IN3                         |
| GPIO23                | ULN2003 IN4                         |
| GPIO13 (33pin, PWM1) | FS90サーボPWM信号                        |
| GPIO25               | 白色LED出力                             |
| 5V                   | ULN2003 VCC & FS90 VCC              |
| GND                  | 共通GND                               |

### OpenPLC ラダーロジック詳細

- モータ運転制御（10分運転・2分休止サイクル）をタイマーで管理
- 光センサーによる物体検知でベルトコンベアを一旦停止
- AI判定取得後にベルトコンベア再開し、適切なタイミングでサーボを制御（NG時のみ）
- モータ温度異常時の緊急停止処理（温度センサー異常フラグ40003でモータ停止）

### Raspberry Pi（AI側）処理フロー詳細

1. 光センサー（CdSセル）のアナログ値をMCP3008で取得し、物体検知を確認
2. ベルトコンベア停止後、カメラ画像取得（OpenCV, PiCamera）
3. TensorFlow LiteによるAI画像判定（事前学習済みモデル）
4. 判定結果（OK/NG）をOpenPLCへModbus TCP通信で送信

### Pythonプログラム詳細設計

#### 光センサー監視プログラム
- 使用ライブラリ：spidev, pymodbus
- MCP3008経由で光センサーの値をSPI通信で取得
- 閾値以下でModbus TCPでレジスタ40004へ検知フラグ送信

#### AI画像認識プログラム
- 使用ライブラリ：OpenCV, TensorFlow Lite, pymodbus
- PiCameraで画像取得
- TensorFlow Lite（MobileNetモデル）で画像判定
- 判定結果をModbus TCP経由でレジスタ40001,40002へ送信

#### ステッピングモータ制御プログラム
- 使用ライブラリ：RPi.GPIO, pymodbus, w1thermsensor
- OpenPLCから運転指示受信
- ULN2003を1-2相励磁方式（8ステップ/10ms）で駆動
- DS18B20で温度監視、50℃超でModbusレジスタ40003へ異常通知

#### サーボモータ制御プログラム
- 使用ライブラリ：RPi.GPIO, pymodbus
- OpenPLCからNG判定受信
- PWM信号でFS90サーボを90度位置へ0.5秒保持後、0°へ戻す

#### 温度センサー監視プログラム
- 使用ライブラリ：w1thermsensor, pymodbus
- DS18B20センサーで5秒ごとに温度計測
- 50℃以上でModbus TCPレジスタ40003へ異常フラグ送信

