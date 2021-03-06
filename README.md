# MCP2221a controller for RASPI and PCF2129 rtc module

### 概要
Hid デバイスである MCP2221a の GPIO を制御する python3 スクリプト及び raspberrypi の gpio 入力を監視してコマンドを実行するサービスプログラム

### 目的
[MCP2221a](https://www.microchip.com/wwwproducts/en/MCP2221A) の GPIO と raspberrypi 4B の GPIO3 を接続し、ホストからリモートで raspberrypi を wakeup させる  
実際には [PCF2129](https://www.nxp.com/products/peripherals-and-logic/signal-chain/real-time-clocks/rtcs-with-spi/accurate-rtc-with-battery-backup-selectable-ic-bus-or-spi:PCF2129) と合わせて運用し、rtc アラームによる wakeup と MCP2221a を制御することによる wakeup を併用する  
また、ホストからリモートで raspberrypi に任意のコマンドを実行させる機能を raspberrypi のサービスとして実装する。主に [epgrtc-tools](https://github.com/nekokomaru/epgrtc-tools) のスクリプトを実行させることを想定しており、rasberrypi を shutdown しても問題ない状態（録画やエンコード処理を行っていない）かどうかを判断した上で shutdown させる。

### 動作環境
作者が動作させている環境は以下の通り

- ターゲット側ハードウェア
  - raspberrypi 4B
  - [RTC board For RaspberryPI Rev1.1](https://nekokohouse.sakura.ne.jp/raspi/#rasp_rtc)
- ターゲット側ソフトウェア
  - [Ubuntu Server 20.04.2 LTS](https://ubuntu.com/download/raspberry-pi)
  - [PCF2127 driver with alarm function for kernel 5.4](https://github.com/nekokomaru/pcf2127mod)
  - [Tools for EPGStation with RTC](https://github.com/nekokomaru/epgrtc-tools)
  - 本プロジェクトのサービス [gpio2cmd](https://github.com/nekokomaru/hidctrl/tree/main/src/gpio2cmd)
- ホスト側
  - Windows10 64bit PC
  - [Python v3.9.2](https://www.python.org/)
  - 本プロジェクトのスクリプト [mcp2221_ctrl.py](https://github.com/nekokomaru/hidctrl/tree/main/src/script)

### 免責事項
本ソフトウェアの動作は保証しない。著作者は一切の責任を負わない

### ライセンス
MIT ライセンスである。詳しくは LICENSE を参照のこと

### 著作者
Yachiyo <https://nekokohouse.sakura.ne.jp/>
