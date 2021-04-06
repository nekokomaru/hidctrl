#!/usr/bin/python3

# import -------------
# use hidapi
import hid

# system api
import time, argparse, sys

# const -------------
# MCP2221a's VID/PID
DEFAULT_VID = 0x04d8
DEFAULT_PID = 0x00dd

# default target name
DEFAULT_NAME = 'PCF2129 RTC CONTROLLER'

# report size
REPO_SIZE = 65

# argument function -----------------

def get_args():

	parser = argparse.ArgumentParser(description='hid controller for MCP2221a (c)Yachiyo.',
	formatter_class=argparse.RawDescriptionHelpFormatter,
	epilog='''option example:
--setup --no 0  : device 0 in the list to be setup for PCF2129 rtc module
--wakeup        : wakeup first PCF2129 rtc module named \'{0:s}\'
--shutdown      : shutdown first PCF2129 rtc module named \'{0:s}\'
--wakeup --no 1 : wakeup PCF2129 rtc module named \'{0:s}\' and numbered \'1\' in the list
--wakeup --name hoge : wakeup first PCF2129 rtc module named \'hoge\'
--wakeup --name hoge --no 1 : wakeup PCF2129 rtc module named \'hoge\' and numbered \'1\' in the list
--setup --no 0 --name hoge : device 0 in the list to be setup for PCF2129 rtc module and name as \'hoge\''''.format(DEFAULT_NAME))
	
	group = parser.add_mutually_exclusive_group()
	parser.add_argument('--setup', action='store_true', help='setup hid device for PCF2129 rtc module')
	parser.add_argument('--no', type=int, help='specify target hid device\'s no. in the list')
	parser.add_argument('--wakeup', action='store_true', help='wakeup target hid device')
	parser.add_argument('--shutdown', action='store_true', help='shutdown target hid device')
	parser.add_argument('--vid', type=int, nargs='?', default=DEFAULT_VID, help='specify target\'s VID')
	parser.add_argument('--pid', type=int, nargs='?', default=DEFAULT_PID, help='specify target\'s PID')
	parser.add_argument('--name', type=str, nargs='?', default=DEFAULT_NAME, help='specify target\'s product name')
	parser.add_argument('--gpio', type=int, nargs='?', default=0x00, help='specify gpio no. to control')
	group.add_argument('--hi', action='store_true', help='specify gpio level to hi')
	group.add_argument('--lo', action='store_true', help='specify gpio level to lo')

	args = parser.parse_args()

	return(args)

# setup func ------------------------
# write flash setting
def setup(path, p_name):

	# open device
	h = hid.device()
	h.open_path(path)

	# confirm
	print('**** warning ****')
	print('\'{0:s}\' to be setup for PCF2129 rtc module'.format(h.get_product_string()))
	val = input('[Y/n] ? ')

	if val.lower() != 'y':
		print('canceled')
		h.close()
		return 1

	# write product string

	# convert string to bytearray of utf16-le
	utf16_name = p_name.encode('utf-16-le')

	# write command
	# 1st byte is report id (= 0x00)
	# write flash : write USB product descriptor string
	cmd = bytearray([0x00, 0xb1, 0x03, len(utf16_name)+2, 0x03])
	cmd += utf16_name

	# write
	h.write(cmd)

	# wait
	time.sleep(0.05)

	# read response
	resp = h.read(REPO_SIZE)

	# check return code
	if resp[1] != 0x00:
		print('error to write product name')
		h.close()
		return 1

	print('new name is \'{0:s}\''.format(h.get_product_string()))


	# write gpio setting
	# 1st byte is report id (= 0x00)
	# write flash : write GP setting
	# GP0,1,2 = output, low, gpio mode. GP3 = input, gpio mode
	cmd = bytearray([0x00, 0xb1, 0x01, 0x00, 0x00, 0x00, 0x08] + [0x00] * (REPO_SIZE-7))

	# write
	h.write(cmd)

	# wait
	time.sleep(0.05)

	# read response
	resp = h.read(REPO_SIZE)

	# device close
	h.close()

	# check return code
	if resp[1] != 0x00:
		print('error to write gp setting')
		return 1

	print('gp setting is successed')
	return 0

# gpio func ------------------------
# control gpio 
def gpioctrl(path, no, val):

	# open device
	h = hid.device()
	h.open_path(path)

	# set gpio output value
	# 1st byte is report id (= 0x00)
	cmd = bytearray([0x00, 0x50, 0x00])

	if no == 0x00:  # GP0
		cmd += bytes([0x01, val, 0x00, 0x00])
	else:
		cmd += bytes([0x00, 0x00, 0x00, 0x00])

	if no == 0x01:  # GP1
		cmd += bytes([0x01, val, 0x00, 0x00])
	else:
		cmd += bytes([0x00, 0x00, 0x00, 0x00])

	if no == 0x02:  # GP2
		cmd += bytes([0x01, val, 0x00, 0x00])
	else:
		cmd += bytes([0x00, 0x00, 0x00, 0x00])

	cmd += bytes([0x00, 0x00, 0x00, 0x00])  # GP3

	cmd += bytes([0x00] * (REPO_SIZE-19))

	# write
	h.write(cmd)

	# wait
	time.sleep(0.05)

	# read response
	resp = h.read(REPO_SIZE)

	if resp[1] != 0x00:
		h.close()
		return 1

	# close device
	h.close()
	return 0


# main -----------------
def main():

	# for gpio
	gpio_val = 0x00

	args = get_args()

	v_id = args.vid
	p_id = args.pid
	p_name = args.name
	gpio_no = args.gpio

	if args.hi:
		gpio_val = 0x01
	elif args.lo:
		gpio_val = 0x00


	# search hid device
	print('Hid device list VID/PID = 0x{0:04x}/0x{1:04x}'.format(v_id, p_id))
	print('---------------------------------------')

	index = 0  # numbering devices
	target_dict = []  # target list
	for device_dict in hid.enumerate(vendor_id=v_id, product_id=p_id):
		if device_dict['interface_number'] >= 0:
			print("No.{0:d} : {1:s}".format(index, device_dict['product_string']))
			d = { 'no': index, 'product_string': device_dict['product_string'], 'path': device_dict['path'], 'vendor_id': device_dict['vendor_id'], 'product_id': device_dict['product_id'] }
			target_dict.append(d)
			index += 1
	print()

	if len(target_dict) == 0:
		print('no target device')
		sys.exit(0)

	# setup product string and gpio setting
	if args.setup:
		if args.no != None:
			ret = setup(target_dict[args.no]['path'], p_name=p_name)
			if ret == 0:
				print('setup successed')
			else:
				print('setup failed')
		else:
			print('use option \'--no\' to set device no.')

	else:
		# search target to control
		no = 0
		dic = dict()
		for d in target_dict:
			if args.no != None:
				if d['product_string'] == p_name and args.no == no:
					dic = d
					break
			else:
				if d['product_string'] == p_name:
					dic = d
					break
			no += 1

		if len(dic) == 0:
			if args.no != None:
				print('not found \'{0:s}\':No.{1:d}'.format(p_name, args.no))
			else:
				print('not found \'{0:s}\''.format(p_name))
			sys.exit(0)

		if args.wakeup:
			print('wakeup')
			ret = gpioctrl(path=dic['path'], no=0x00, val=0x01)
			if ret != 0:
				print('error wakeup')
				sys.exit(0)
			time.sleep(0.5)
			ret = gpioctrl(path=dic['path'], no=0x00, val=0x00)
			if ret != 0:
				print('error wakeup')
				sys.exit(0)

		elif args.shutdown:
			print('shutdown')
			ret = gpioctrl(path=dic['path'], no=0x01, val=0x01)
			if ret != 0:
				print('error shutdown')
				sys.exit(0)
			time.sleep(0.5)
			ret = gpioctrl(path=dic['path'], no=0x01, val=0x00)
			if ret != 0:
				print('error shutdown')
				sys.exit(0)

		elif args.hi or args.lo:
			print('gpio ctrl')
			ret = gpioctrl(path=dic['path'], no=gpio_no, val=gpio_val)
			if ret != 0:
				print('error control gpio')
		else:
			print('set option \'-h\' for usage')


# ----------------

if __name__ == '__main__':
	main()
