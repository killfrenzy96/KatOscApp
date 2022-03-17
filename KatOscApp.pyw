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


from tkinter import Tk, Text, Button
import math
import sys

import katosc

class KatOscApp:
	def __init__(self):
		self.kat = katosc.KatOsc()
		self.text_length = self.kat.text_length
		self.line_length = self.kat.line_length
		self.line_count = self.kat.line_count

		# --------------
		# GUI Setup
		# --------------
		self.window = window = Tk()
		window.title("KillFrenzy Avatar Text OSC")
		window.geometry("630x214")
		window.configure(bg = "#333")
		window.resizable(False, False)

		filepath = sys.argv[0]
		try:
			window.iconbitmap(filepath)
		except:
			print("Warning: Could not load icon from " + filepath)

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
		self.gui_text.bind_all('<Key>', self._limit_text_length)

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

		# Start App
		self.window.mainloop()

		# Stop App
		self.kat.stop()


	# Set the text to any value
	def set_text(self, text: str):
		self.kat.set_text(text)

		self.gui_text.delete(1.0, "end")
		self.gui_text.insert(1.0, text)
		self._limit_text_length()
		self.gui_text.focus_set()


	# Limits the text length of the text box
	def _limit_text_length(self, *args):
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
				length_padded += self._get_padded_length(text)

		# Delete text if it's too long
		if length_padded >= self.text_length:
			self.gui_text.delete("end-" + str(length_padded - self.text_length + 1) + "c", "end")

		# Send text
		self.kat.set_text(self.gui_text.get(1.0, "end"))


	# Gets the effective padded length of a line
	def _get_padded_length(self, text: str):
		lines = max(math.ceil(len(text) / self.line_length), 1)
		return self.line_length * lines


if __name__ == "__main__":
	kat_osc_app = KatOscApp()
