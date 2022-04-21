import png
import math
import shutil
#import argparse	#FUTURE WORK: A lot of this program can be simplified with arg parsing; see below usage.
#	> python3 PNGcryp filename [--encrypt/-E] [--decrypt/-D] [--verbose/-v]
#		ON ENCRYPT:
#	> Please enter your message:
#	> [...]
#	> Encrypted.
#		ON DECRYPT:
#	> Please enter the name of an output file, or leave blank to only print to console
#	> [...]
#	> Decrypted. [File: ... / Decrypted text: \n ...]
#		ON ANY FAILURE (bad file name, no mode selected, keyboard interrupt, etc.):
#	> Error: [...]

class bin_list:

	# Not totally sure the logic behind this class, but it seems to work in this implementation (good job, past me)
	def __init__(self, dec_list):
		class bin_val:
			def __init__(self, dec):
				self.dec = dec
				self.bin = self.convert_to_bin()
			def convert_to_bin(self, length=8):
				remaining = self.dec
				bin = ""
				while remaining >= 1:
					if remaining % 2 == 1:
						remaining -= 1
						bin = f"1{bin}"
					else:
						bin = f"0{bin}"
					remaining /= 2
				while len(bin) < length:
					bin = f"0{bin}"
				return bin
			def get_insignificant(self):
				return self.bin[(len(self.bin)-2):]
			def place_insignificant(self, insig):
				if len(insig) != 2:
					print(f"Something went wrong, ${len(insig)} characters were passed to a bin_val")
					exit()
			def get_bin(self):
				return self.bin
		self.bins = []
		for dec in dec_list:
			self.bins.append(bin_val(dec))
	def get_bins(self):
		return [bin.get_bin() for bin in self.bins]
	# The following two functions are unused
	#	I probably had an idea how to progress but forgot about it
	def get_insig_series(self, start, end):
		return [bin.get_insignificant() for bin in self.bins[start:end]]
	def place_insig_series(self, series):
		insigs = []
		series = series.replace(" ","")
		while series:
			insigs.append(series[:2])
			series = series[2:]
		return insigs

#-----------------
#   MAIN
#   takes:
#   returns:
#   does: Base program
#   supports: IS MAIN
#-----------------
def main():
	print("\n--- W E L C O M E   T O   P N G C R i P ---\n")
	res = select_mode()
	if (res == "e"):
		print("... r u n n i n g   e n c r y p t   m o d e ...")
		run_encrypt()
	elif (res == "d"):
		print("... r u n n i n g   d e c r y p t   m o d e ...")
		run_decrypt()
	else:
		throw_err("No mode was selected; found ["+res+"]", 1)
	exit(0)
#-----------------
#   SELECT_MODE
#   takes:
#   returns: "e" or "d" for Encrypt or Decrypt
#   does: Gets run mode from user
#   supports: MAIN
#-----------------
def select_mode():
	print("Please select mode: Decryption [0]  |  Encrypt [1]")
	while True:
		try:
			res = int(input("> "))
		except ValueError:
			continue
		if res not in [0,1]:
			continue
		if res:
			return "e"
		return "d"


#-----------------
#   GET_PNG_DATA
#   takes:
#   returns: dict - list of bytes in first row of png data, and file name
#   does: Gets name of encrypting png from user, reads and returns relevant data
#   future work: Use an algorithm to almost randomly select pixels from the file instead of the predictable first row
#   supports: RUN_ENCRYPT, RUN_DECRYPT
#-----------------
def get_png_data():
	file_name = input("Please input the name of the .png:\n")
	r = png.Reader(file_name)
	data = r.read()
	rows = data[2]
	first_row = []
	for bytearray in rows:
		for bytes in bytearray:
			first_row.append(bytes)
		break
	return {
		"line_data": first_row,
		"file_name": file_name,
		"rows": rows,
		"full": data
	}
#-----------------
#   HASH_MESSAGE
#   takes:
#   returns: dict - message data
#   does: Gets message from user, converts message into number data
#   supports: RUN_ENCRYPT
#-----------------
def hash_message():
	message = input("Please input your message:\n")
	ords = []
	for char in message:
		ords.append(ord(char))
	msg_bins = bin_list(ords)
	return {
		"data": msg_bins.get_bins(),
		"char_len": len(ords),
		"sequence_len": len(ords)*8
	}
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
#   WRITE_MODIFIED_PNG
#   takes: array of new first line data, dict of full png data, string of file name
#   returns:
#   does: Writes the modified png content to a file called "pngcrip_[original file name]"
#   supports: RUN_ENCRYPT
#-----------------
def write_modified_png(new_line, png_data, png_name):
	#shutil.copy(png_name, "pngcrip_"+png_name) # Might create a new file?
	file_contents = []
	file_contents.append(new_line)
	skipped_first = False
	rows = png_data[2]
	for row in rows:
		#if(not skipped_first):
		#	verbose("Skipped first line")
		#	skipped_first = True
		#	continue
		row_content = []
		for byte in row:
			row_content.append(byte)
		file_contents.append(row_content)
	verbose("Finished copying file contents")
	w = png.Writer(png_data[0], png_data[1], greyscale=png_data[3]["greyscale"], bitdepth=png_data[3]["bitdepth"])
	f = open("pngcrip_"+png_name, "wb")
	w.write(f, file_contents)
	f.close()
	verbose("File written")
#-----------------
#   RUN_ENCRYPT
#   takes:
#   returns:
#   does: Runs the full encryption procedure
#   supports: MAIN
#-----------------
def run_encrypt():
	print("Now in encryption mode...")
	png_data = get_png_data()
	line_data = png_data["line_data"]
	bins = bin_list(line_data)
	message_data = hash_message()
	# Loop through png data and divide each character binary accross four pixel values' 2 least significant digits
	verbose(message_data["data"])
	verbose(message_data["sequence_len"])
	sequence_counter = 0
	encrypted_line_prefix = []
	for i in range(message_data["char_len"]):
		char_index = math.floor(sequence_counter/4)
		to_encrypt = message_data["data"][char_index]
		verbose(to_encrypt)
		for j in range(4):
			# Setup and get prefix
			to_edit = line_data[sequence_counter]
			verbose("["+str(sequence_counter)+"]"+str(to_edit),end=">>")
			data_bin_prefix = bin(to_edit)[:-2]
			# Get suffix
			bits_index = j*2
			suffix = to_encrypt[bits_index:bits_index+2]
			# Build new data and replace
			data_bin = to_dec(data_bin_prefix + suffix)
			encrypted_line_prefix.append(data_bin)
			sequence_counter += 1
			verbose(data_bin)
	# Update line data
	verbose(encrypted_line_prefix)
	new_line_data = encrypted_line_prefix + line_data[len(encrypted_line_prefix):]
	write_modified_png(new_line_data, png_data["full"], png_data["file_name"])
	print("|. e n c r y p t e d .|")
	print("|Thank you, come again|")
	print("|                     |")
	print("|       by runt       |")
	print("|---------------------|")

#-----------------
#   RUN_DECRYPT
#   takes:
#   returns:
#   does: Runs the full decryption procedure
#   supports: MAIN
#-----------------
def run_decrypt():
	print("Now in decryption mode...")
	# Get png data
	png_data = get_png_data()
	line_data = png_data["line_data"]
	# Get least significant bits of first row
	lsb_list = []
	for byte in line_data:
		b = bin(byte)[-2:]	# Get 2 least significant bits
		lsb_list.append(b)
	# Assemble lsbs into one long binary string
	char_counter = 0
	line_string = ""
	for lsb in lsb_list:
		if char_counter % 4 == 0:
			line_string += "0b"	# Needed prefix
		line_string += lsb
		if char_counter % 4 == 3:
			line_string += ":"	# Splitting char
		char_counter += 1
	line_chars = line_string.split(":")
	verbose(line_chars)
	message_string = r""
	for char in line_chars:
		if char:
			dec_char = to_dec(char)
			chr_char = chr(dec_char)
			message_string = f"{message_string}|{chr_char}"
		else:
			break
	print(message_string)
#-----------------
#   THROW_ERR
#   takes: string that represents error message, int error code (default 1)
#   returns:
#   does: Prints message, exits program with error code
#   supports: multiple
#-----------------
def throw_err(msg, code=1):
	print(">>ERR>> " + msg)
	exit(code)
#-----------------
#   VERBOSE
#   takes: same as print()
#   returns:
#   does: Same as print, but for verbose/debugging
#   supports: multiple
#-----------------
def verbose(msg, end="\n"):
	# Put a conditional here: User can initiate verbose with a -v/-V switch
	print(msg, end=end)

if __name__ == "__main__":
	main()
