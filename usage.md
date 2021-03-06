# 本ソフトウェアの使い方

---
## wakeup 機能を使うための準備

### ホスト側の準備
1. `python` バージョン3 以上をインストールしておく
```shell:cmd
python -V   # hidapi の必要条件から、最低でも 3.5 が必要なはず
python3 -V  # ubuntu だとこの名前でインストールされている
```
3. python モジュールの [`hidapi`](https://pypi.org/project/hidapi/) をインストールする
```shell:cmd
pip install hidapi    # windows
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

### ホストからの wakeup のやりかた
1. 以下のコマンドを入力すると、USB に接続されていて最初に見つかった `PCF2129 RTC CONTROLLER` デバイスを制御して raspberrypi を wakeup させる
```shell:cmd
python mcp2221_ctrl.py --wakeup
```
2. オプションの詳しい使い方はヘルプを参照する
```shell:cmd
python mcp2221_ctrl.py -h
```
以下のようなヘルプが表示されるので、参考にする
```shell:cmd
usage: mcp2221_ctrl.py [-h] [--setup] [--no NO] [--wakeup] [--shutdown] [--vid [VID]] [--pid [PID]] [--name [NAME]]
                       [--gpio [GPIO]] [--hi | --lo]

hid controller for MCP2221a (c)Yachiyo.

optional arguments:
  -h, --help     show this help message and exit
  --setup        setup hid device for PCF2129 rtc module
  --no NO        specify target hid device's no. in the list
  --wakeup       wakeup target hid device
  --shutdown     shutdown target hid device
  --vid [VID]    specify target's VID
  --pid [PID]    specify target's PID
  --name [NAME]  specify target's product name
  --gpio [GPIO]  specify gpio no. to control
  --hi           specify gpio level to hi
  --lo           specify gpio level to lo

option example:
--setup --no 0  : device 0 in the list to be setup for PCF2129 rtc module
--wakeup        : wakeup first PCF2129 rtc module named 'PCF2129 RTC CONTROLLER'
--shutdown      : shutdown first PCF2129 rtc module named 'PCF2129 RTC CONTROLLER'
--wakeup --no 1 : wakeup PCF2129 rtc module named 'PCF2129 RTC CONTROLLER' and numbered '1' in the list
--wakeup --name hoge : wakeup first PCF2129 rtc module named 'hoge'
--wakeup --name hoge --no 1 : wakeup PCF2129 rtc module named 'hoge' and numbered '1' in the list
--setup --no 0 --name hoge : device 0 in the list to be setup for PCF2129 rtc module and name as 'hoge'
```
---
## shutdown 機能を使うための準備
### ホスト側の準備
[wakeup 機能を使うための準備](#wakeup-機能を使うための準備)と同じ

### ターゲット側の準備
1. [ハードウェアセットアップ](#ハードウェアセットアップ)を行っておく
2. RTC board For RaspberryPI Rev1.1 を使うのであれば、`/boot/firmware/syscfg.txt` を書き換え（ubuntu の場合）、**i2c1 (=i2c_arm) を無効にしておく**
3. `src/gpio2cmd` に移動し、設定ファイル `gpio2cmd.conf` を必要に応じて書き換える。gpio には検出対象の gpio 番号を、edge には 検出する gpio 信号のパターンを（`rising` / `falling` / `both` ）、command には gpio 信号を検出したときに実行するコマンドを記述する。command は、実行コマンド名のあとに4つまでオプションを指定することが出来る。スペースで区切って記述すること  
RTC board For RaspberryPI Rev1.1 及び epgrtc-tools とともに運用するときは、特に書き換える必要はない
```text:gpio2cmd.conf
gpio = 2
edge = falling
command = /usr/local/bin/shutdown_srv
```
4. サービスのビルドとインストールを行う
```shell:bash
make    # 実行ファイルをビルドする
sudo make install    # 実行ファイルをインストールする
sudo ./install_service.sh install    # サービスをインストールする
```
5. 再起動すると準備完了

### ホストからの shutdown のやり方
1. 以下のコマンドを入力すると、USB に接続されていて最初に見つかった `PCF2129 RTC CONTROLLER` デバイスを制御して raspberrypi を shutdown させる。（正確には、gpio2cmd.conf の command で指定したコマンドが実行される）
```shell:cmd
python mcp2221_ctrl.py --shutdown
```
2. オプションの詳しい使い方はヘルプを参照のこと
```shell:cmd
python mcp2221_ctrl.py -h
```

### ターゲット側のアンインストール方法
以下の操作のあと再起動するとアンインストールが完了する
```shell:bash
sudo ./install_service.sh uninstall
sudo make uninstall
```
---
以上
