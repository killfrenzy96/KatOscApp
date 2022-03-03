# Avatar Text OSC App for VRChat
# Copyright (C) 2022 KillFrenzy / Evan Tran

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


from threading import Timer
from pythonosc import udp_client
from tkinter import *
import math
import sys

class KatOscApp:
	def __init__(self):
		self.osc_ip = "127.0.0.1" # OSC network IP
		self.osc_port = 9000 # OSC network port
		self.osc_delay = 0.3 # Delay between network updates in seconds. Setting this too low will cause issues.

		self.text_length = 128
		self.sync_params = 4
		self.pointer_count = int(self.text_length / self.sync_params)
		self.line_length = 32
		self.line_count = 4

		self.param_visible = "KAT_Visible"
		self.param_pointer = "KAT_Pointer"
		self.param_sync = "KAT_CharSync"

		self.osc_prefix = "/avatar/parameters/"
		self.osc_text = ""

		self.keys = {
			" ": 0,
			"!": 1,
			"\"": 2,
			"#": 3,
			"$": 4,
			"%": 5,
			"&": 6,
			"'": 7,
			"(": 8,
			")": 9,
			"*": 10,
			"+": 11,
			",": 12,
			"-": 13,
			".": 14,
			"/": 15,
			"0": 16,
			"1": 17,
			"2": 18,
			"3": 19,
			"4": 20,
			"5": 21,
			"6": 22,
			"7": 23,
			"8": 24,
			"9": 25,
			":": 26,
			";": 27,
			"<": 28,
			"=": 29,
			">": 30,
			"?": 31,
			"@": 32,
			"A": 33,
			"B": 34,
			"C": 35,
			"D": 36,
			"E": 37,
			"F": 38,
			"G": 39,
			"H": 40,
			"I": 41,
			"J": 42,
			"K": 43,
			"L": 44,
			"M": 45,
			"N": 46,
			"O": 47,
			"P": 48,
			"Q": 49,
			"R": 50,
			"S": 51,
			"T": 52,
			"U": 53,
			"V": 54,
			"W": 55,
			"X": 56,
			"Y": 57,
			"Z": 58,
			"[": 59,
			"\\": 60,
			"]": 61,
			"^": 62,
			"_": 63,
			"`": 64,
			"a": 65,
			"b": 66,
			"c": 67,
			"d": 68,
			"e": 69,
			"f": 70,
			"g": 71,
			"h": 72,
			"i": 73,
			"j": 74,
			"k": 75,
			"l": 76,
			"m": 77,
			"n": 78,
			"o": 79,
			"p": 80,
			"q": 81,
			"r": 82,
			"s": 83,
			"t": 84,
			"u": 85,
			"v": 86,
			"w": 87,
			"x": 88,
			"y": 89,
			"z": 90,
			"{": 91,
			"|": 92,
			"}": 93,
			"~": 94,
			"€": 95,
			"ぬ": 127,
			"ふ": 129,
			"あ": 130,
			"う": 131,
			"え": 132,
			"お": 133,
			"や": 134,
			"ゆ": 135,
			"よ": 136,
			"わ": 137,
			"を": 138,
			"ほ": 139,
			"へ": 140,
			"た": 141,
			"て": 142,
			"い": 143,
			"す": 144,
			"か": 145,
			"ん": 146,
			"な": 147,
			"に": 148,
			"ら": 149,
			"せ": 150,
			"ち": 151,
			"と": 152,
			"し": 153,
			"は": 154,
			"き": 155,
			"く": 156,
			"ま": 157,
			"の": 158,
			"り": 159,
			"れ": 160,
			"け": 161,
			"む": 162,
			"つ": 163,
			"さ": 164,
			"そ": 165,
			"ひ": 166,
			"こ": 167,
			"み": 168,
			"も": 169,
			"ね": 170,
			"る": 171,
			"め": 172,
			"ろ": 173,
			"。": 174,
			"ぶ": 175,
			"ぷ": 176,
			"ぼ": 177,
			"ぽ": 178,
			"べ": 179,
			"ぺ": 180,
			"だ": 181,
			"で": 182,
			"ず": 183,
			"が": 184,
			"ぜ": 185,
			"ぢ": 186,
			"ど": 187,
			"じ": 188,
			"ば": 189,
			"ぱ": 190,
			"ぎ": 191,
			"ぐ": 192,
			"げ": 193,
			"づ": 194,
			"ざ": 195,
			"ぞ": 196,
			"び": 197,
			"ぴ": 198,
			"ご": 199,
			"ぁ": 200,
			"ぃ": 201,
			"ぅ": 202,
			"ぇ": 203,
			"ぉ": 204,
			"ゃ": 205,
			"ゅ": 206,
			"ょ": 207,
			"ヌ": 208,
			"フ": 209,
			"ア": 210,
			"ウ": 211,
			"エ": 212,
			"オ": 213,
			"ヤ": 214,
			"ユ": 215,
			"ヨ": 216,
			"ワ": 217,
			"ヲ": 218,
			"ホ": 219,
			"ヘ": 220,
			"タ": 221,
			"テ": 222,
			"イ": 223,
			"ス": 224,
			"カ": 225,
			"ン": 226,
			"ナ": 227,
			"ニ": 228,
			"ラ": 229,
			"セ": 230,
			"チ": 231,
			"ト": 232,
			"シ": 233,
			"ハ": 234,
			"キ": 235,
			"ク": 236,
			"マ": 237,
			"ノ": 238,
			"リ": 239,
			"レ": 240,
			"ケ": 241,
			"ム": 242,
			"ツ": 243,
			"サ": 244,
			"ソ": 245,
			"ヒ": 246,
			"コ": 247,
			"ミ": 248,
			"モ": 249,
			"ネ": 250,
			"ル": 251,
			"メ": 252,
			"ロ": 253,
			"〝": 254,
			"°": 255
		}

		# --------------
		# GUI Setup
		# --------------
		self.window = window = Tk()
		window.title("KillFrenzy Avatar Text OSC")
		window.geometry("630x214")
		window.configure(bg = "#333")
		window.resizable(False, False)
		window.iconbitmap(sys.argv[0])

		# Create text box
		global full
		full = False

		self.gui_text = Text(window,
			font = ("Courier New", 24),
			width = self.line_length,
			height = 4,
			border = 0,
			wrap = "char",
			fg = "#fff",
			bg = "#222",
			insertbackground = "#fff"
		)
		self.gui_text.grid(column = 0, row = 1, padx = 10, pady = 10)
		self.gui_text.bind_all('<Key>', self.limit_text_length)

		# Create clear button
		self.gui_clear = Button(window,
			text = "Clear",
			command = lambda:self.set_text(""),
			border = 0,
			fg = "#ddd",
			bg = "#444",
			width = 16,
			height = 2
		)
		self.gui_clear.grid(column = 0, row = 2, padx = 10, pady = 0, sticky = "ne")

		# --------------
		# OSC Setup
		# --------------
		self.osc_client = udp_client.SimpleUDPClient(self.osc_ip, self.osc_port)
		self.osc_timer = RepeatedTimer(self.osc_delay, self.osc_timer_loop)

		self.osc_client.send_message(self.osc_prefix + self.param_visible, True) # Make KAT visible
		self.osc_client.send_message(self.osc_prefix + self.param_pointer, 255) # Clear KAT text
		for value in range(self.sync_params):
			self.osc_client.send_message(self.osc_prefix + self.param_sync + str(value), 0.0) # Reset KAT characters sync

		# Start App
		self.osc_timer.start()
		self.window.mainloop()

		# Stop App
		self.osc_timer.stop()
		self.osc_client.send_message(self.osc_prefix + self.param_visible, False) # Hide KAT


	# Set the text to any value
	def set_text(self, text: str):
		self.gui_text.delete(1.0, "end")
		self.gui_text.insert(1.0, text)
		self.limit_text_length()
		self.gui_text.focus_set()


	# Syncronisation loop
	def osc_timer_loop(self):
		gui_text = self.gui_text.get(1.0, "end")

		# Sends clear text message if all text is empty
		if gui_text.strip("\n").strip(" ") == "":
			self.osc_client.send_message(self.osc_prefix + self.param_pointer, 255) # 255 is the value to clear text
			self.osc_text = " ".ljust(self.text_length)
			return

		# Make sure KAT is visible even after avatar change
		self.osc_client.send_message(self.osc_prefix + self.param_visible, True)

		# Pad line feeds with spaces for OSC
		text_lines = gui_text.split("\n")
		for index, text in enumerate(text_lines):
			text_lines[index] = self.pad_line(text)
		gui_text = self.list_to_string(text_lines)

		# Pad text with spaces up to the text limit
		gui_text = gui_text.ljust(self.text_length)
		osc_text = self.osc_text.ljust(self.text_length)

		# Text syncing
		if gui_text != self.osc_text: # GUI text is different, needs sync
			osc_chars = list(osc_text)

			for pointer_index in range(self.pointer_count):
				# Check if characters within this pointer are different
				equal = True
				for char_index in range(self.sync_params):
					index = (pointer_index * self.sync_params) + char_index
					if gui_text[index] != osc_text[index]:
						equal = False
						break

				if equal == False: # Characters not equal, need to sync this pointer position
					self.osc_client.send_message(self.osc_prefix + self.param_pointer, pointer_index + 1) # Set pointer position

					# Loop through characters within this pointer and set them
					for char_index in range(self.sync_params):
						index = (pointer_index * self.sync_params) + char_index
						gui_char = gui_text[index]

						# Convert character to the key value
						key = 0
						if gui_char in self.keys.keys():
							key = self.keys[gui_char]
						else:
							key = self.keys[" "] # Invalid character, replace with a space

						# Calculate character float value for OSC
						value = float(key)
						if value > 127.5:
							value = value - 256.0
						value = value / 127.0

						self.osc_client.send_message(self.osc_prefix + self.param_sync + str(char_index), value)
						osc_chars[index] = gui_char # Apply changes to the networked value

					self.osc_text = self.list_to_string(osc_chars)
					return


	# Combines an array of strings into a single string
	def list_to_string(self, string: str):
		new_string = ""
		for x in string:
			new_string += x
		return new_string


	# Limits the text length of the text box
	def limit_text_length(self, *args):
		# Prevent too many line feeds
		self.gui_text.delete(5.0, "end")

		# Grab the text from the text box
		gui_text_original = self.gui_text.get(1.0, "end")
		text_lines = gui_text_original.split("\n")

		# Remove that empty line at the end
		if len(text_lines[len(text_lines) - 1]) == 0:
			text_lines = text_lines[:-1]

		# Calculate effective text length
		length_padded = 0
		for index, text in enumerate(text_lines):
			if index == len(text_lines) - 1: # Do not add padding to the last line
				length_padded += len(text)
			else:
				length_padded += self.get_padded_length(text)

		# Delete text if it's too long
		if length_padded >= self.text_length:
			self.gui_text.delete("end-" + str(length_padded - self.text_length + 1) + "c", "end")


	# Pads the text line to its effective length
	def pad_line(self, text: str):
		return text.ljust(self.get_padded_length(text))


	# Gets the effective padded length of a line
	def get_padded_length(self, text: str):
		lines = max(math.ceil(len(text) / self.line_length), 1)
		return self.line_length * lines


class RepeatedTimer(object):
	def __init__(self, interval, function, *args, **kwargs):
		self._timer     = None
		self.interval   = interval
		self.function   = function
		self.args       = args
		self.kwargs     = kwargs
		self.is_running = False
		self.start()

	def _run(self):
		self.is_running = False
		self.start()
		self.function(*self.args, **self.kwargs)

	def start(self):
		if not self.is_running:
			self._timer = Timer(self.interval, self._run)
			self._timer.start()
			self.is_running = True

	def stop(self):
		self._timer.cancel()
		self.is_running = False

if __name__ == "__main__":
	kat_osc_app = KatOscApp()
