# MCP2221a controller for RASPI and PCF2129 rtc module

### 概要
Hid デバイスである MCP2221a の GPIO を制御する python3 スクリプト  

### 目的
[MCP2221a](https://www.microchip.com/wwwproducts/en/MCP2221A) の GPIO と raspberrypi 4B の GPIO3 を接続し、ホストからリモートで raspberrypi を wakeup させる  
実際には [PCF2129](https://www.nxp.com/products/peripherals-and-logic/signal-chain/real-time-clocks/rtcs-with-spi/accurate-rtc-with-battery-backup-selectable-ic-bus-or-spi:PCF2129) と合わせて運用し、rtc アラームによる wakeup と MCP2221a を制御することによる wakeup を併用する

### 動作環境
作者が動作させている環境は以下の通り

- ターゲット側ハードウェア
  - raspberrypi 4B
  - [RTC board For RaspberryPI Rev1.1](https://nekokohouse.sakura.ne.jp/raspi/#rasp_rtc)
- ターゲット側ソフトウェア
  - [Ubuntu Server 20.04.2 LTS](https://ubuntu.com/download/raspberry-pi)
  - [PCF2127 driver with alarm function for kernel 5.4](https://github.com/nekokomaru/pcf2127mod)
- ホスト側
  - Windows10 64bit PC
  - [Python v3.9.2](https://www.python.org/)

### 免責事項
本ソフトウェアの動作は保証しない。著作者は一切の責任を負わない

### ライセンス
MIT ライセンスである。詳しくは LICENSE を参照のこと

### 著作者
Yachiyo <https://nekokohouse.sakura.ne.jp/>
