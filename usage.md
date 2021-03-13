# 本ソフトウェアの使い方

### 使用準備
1. `python` バージョン3 以上をインストールしておく
```shell:cmd
python -V   # hidapi の必要条件から、最低でも 3.5 が必要なはず
python3 -V  # ubuntu だとこの名前でインストールされている
```
3. python モジュールの [`hidapi`](https://pypi.org/project/hidapi/) をインストールする
```shell:cmd
sudo pip install hidapi    # windows
sudo pip3 install hidapi   # ubuntu
```

### ハードウェアセットアップ
1. 用意した [RTC board For RaspberryPI Rev1.1](https://nekokohouse.sakura.ne.jp/raspi/#rasp_rtc) を raspberrypi の**ヘッダピンには接続せず**、
   usb のみホストに接続して、スクリプトを実行する
```shell:cmd
python mcp2221_ctrl.py
```
2. すると、接続している MCP2221a デバイスの一覧が表示される。以下は例
```shell:cmd
Hid device list VID/PID = 0x04d8/0x00dd
---------------------------------------
No.0 : TAP-RE34U SWITCHER
No.1 : PCF2129 RTC CONTROLLER

set option '-h' for usage
```
3. セットアップしたい RTC board For RaspberryPI Rev1.1 の No を確認して、以下のコマンドを入力する
```shell:cmd
python mcp2221_ctrl.py --setup --no 1   # ここでは、No.1 のデバイスをセットアップする
```
4. 本当にセットアップするか確認されるので、`y` を入力すると、MCP2221a のフラッシュメモリを書き換えてセットアップが行われる。
   セットアップを行ったデバイスは、`PCF2129 RTC CONTROLLER` という製品名で表示されるようになる（オプションで変更可能）
5. セットアップの終わったデバイスは、一度 USB 端子を抜き差ししておく（書き換えたフラッシュメモリの内容を反映させるため）
6. セットアップできた RTC board を raspberrypi のヘッダピンに刺し、USB はホストに繋ぐと使用準備完了

### wakeup のやりかた
1. 以下のコマンドを入力すると、USB に接続されていて最初に見つかった `F2129 RTC CONTROLLER` デバイスを制御して raspberrypi を wakeup させる
```shell:cmd
python mcp2221_ctrl.py --wakeup
```
2. オプションの詳しい使い方はヘルプを参照する
```shell:cmd
python mcp2221_ctrl.py -h
```
以下のようなヘルプが表示されるので、参考にする
```shell:cmd
usage: mcp2221_ctrl.py [-h] [--setup] [--no NO] [--wakeup] [--vid [VID]] [--pid [PID]] [--name [NAME]] [--gpio [GPIO]]
                       [--hi | --lo]

hid controller for MCP2221a (c)Yachiyo.

optional arguments:
  -h, --help     show this help message and exit
  --setup        setup hid device for PCF2129 rtc module
  --no NO        specify target hid device's no. in the list
  --wakeup       wakeup target hid device
  --vid [VID]    specify target's VID
  --pid [PID]    specify target's PID
  --name [NAME]  specify target's product name
  --gpio [GPIO]  specify gpio no. to control
  --hi           specify gpio level to hi
  --lo           specify gpio level to lo

option example:
--setup --no 0  : device 0 in the list to be setup for PCF2129 rtc module
--wakeup        : wakeup first PCF2129 rtc module named 'PCF2129 RTC CONTROLLER'
--wakeup --no 1 : wakeup PCF2129 rtc module named 'PCF2129 RTC CONTROLLER' and numbered '1' in the list
--wakeup --name hoge : wakeup first PCF2129 rtc module named 'hoge'
--wakeup --name hoge --no 1 : wakeup PCF2129 rtc module named 'hoge' and numbered '1' in the list
```
