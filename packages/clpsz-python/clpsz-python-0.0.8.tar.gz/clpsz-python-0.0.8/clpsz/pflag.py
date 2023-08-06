import argparse


def main(args):
	number = args.number
	binary_str = "{0:b}".format(number)
	binary_str = binary_str[::-1]
	for i, c in enumerate(binary_str):
		print '{:02d}: {:s}'.format(i, c)


def pflag_main_helper():
	parser = argparse.ArgumentParser(prog='pflag')
	parser.add_argument('number', type=int, help='number to parse')
	args = parser.parse_args()

	main(args)


if __name__ == '__main__':
	# args = lambda: None
	# args.number = 4
	# main(args)
	pflag_main_helper()
