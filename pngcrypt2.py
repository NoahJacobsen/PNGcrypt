import argparse
import png
import math
import shutil

def get_args():
    desc = "A program"  #TODO
    parser = argparse.ArgumentParser(
        description=desc
    )
    parser.add_argument(
        'file',
        type=str,
        help="name of file to act on"
    )
    parser.add_argument(
        '-E',
        '--encrypt',
        action='store_true',
        default=False,
        help="encrypt mode"
    )
    parser.add_argument(
        '-D',
        '--decrypt',
        action='store_true',
        default=False,
        help="decrypt mode"
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
        help="print extra info"
    )
    parser.add_argument(
        '--out',
        type=str,
        default="",
        help="write to file OUT instead of default behaviour"
    )
    '''
    parser.add_argument(
        '-p',
        '--password-path',
        type=str,
        default="",
        help="point to file that conatins password instead of inputting upon prompt"
    )
    parser.add_argument(
        '-m',
        '--message-path',
        type=str,
        default="",
        help="point to file that conatins message instead of inputting upon prompt"
    )
    '''
    return parser.parse_args()
#-----------------
#   VERBOSE
#   takes: same as print()
#   returns:
#   does: Same as print, but for verbose/debugging
#   supports: multiple
#-----------------
def verbose(msg, end="\n"):
	# Put a conditional here: User can initiate verbose with a -v/--verbose switch
	print(msg, end=end)
#-----------------
#   TO_DEC
#   takes: a string representing a binary number; i.e '0b1000101' (must have '0b' prefix)
#   returns: an integer representing the decimal value of the input binary
#   does: Converts a binary number string (from the bin() function) into a decimal integer
#	future work: Could potentially use this in a custom "dynamic number" class that is able to freely shift between dec/bin/hex; could go even further and write "logic handlers" to allow user to avoid calling functions
#   supports: RUN_ENCRYPT
#-----------------
def to_dec(s_bin):
	s_bin = s_bin[2:]
	s_bin_temp = s_bin
	power = 1
	dec = 0
	while s_bin_temp:
		digit = s_bin_temp[-1]	# Get last digit
		dec += int(digit) * power	# Add power if digit is set
		power *= 2
		s_bin_temp = s_bin_temp[:-1]
	return dec
#-----------------
#   MAIN
#   takes:
#   returns:
#   does: Base program
#   supports: IS MAIN
#-----------------
def main():
    args = get_args()
    verbose(args)
    if(args.encrypt and args.decrypt):
        print("Cannot")
if __name__ == "__main__":
    main()
