import unittest


class project4tests(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super(project4tests, self).__init__(*args, **kwargs)

	def test_diagonal_left_match(self):
		self.last_input_index = 0
		inp = ''
		self.printed_stuff = ''
		def fake_input():
				ll = self.last_input_index
				self.last_input_index += 1
				ret = inp[ll]
				return ret
		def fake_print(*args):
			msg = ' '.join(args)
			self.printed_stuff+=msg+'\n' 
		import project4
		project4.input = fake_input
		project4.print = fake_print
		inp = [
			'6', '3', 'EMPTY',
			'F 1 Q W E', '', '', '', '', '', '',
			'F 2 A E S', '', '', '', '', '', '',
			'F 3 E Z X', '', '', '', '', '', '', 
			'', 'Q'
		]
		
		expected = '|         |\n|         |\n|         |\n|         |\n| Q  A  Z |\n| W  S  X |\n --------- \n'
		project4.run_program()
		self.assertEqual(self.printed_stuff[-1*len(expected):], expected)

	def test_diagonal_right_match(self):
		inp = ''
		self.printed_stuff1 = ''
		self.last_input_index1 = 0
		def fake_input():
				ll = self.last_input_index1
				self.last_input_index1 += 1
				ret = inp[ll]
				return ret
		def fake_print(*args):
			msg = ' '.join(args)
			self.printed_stuff1 += msg + '\n' 
		import project4
		project4.input = fake_input
		project4.print = fake_print
		inp = [
			'6', '3', 'EMPTY',
			'F 1 E W A', '', '', '', '', '', '',
			'F 2 A E S', '', '', '', '', '', '',
			'F 3 B Z E', '', '', '', '', '', '', 
			'', 'Q'
		]
		
		expected = '|         |\n|         |\n|         |\n|         |\n| W  A  B |\n| A  S  Z |\n --------- \n'
		project4.run_program()
		self.assertEqual(self.printed_stuff1[-1 * len(expected):], expected)

	def test_horizontal_match(self):
		inp = ''
		self.printed_stuff2 = ''
		self.last_input_index2 = 0
		def fake_input():
				ll = self.last_input_index2
				self.last_input_index2 += 1
				ret = inp[ll]
				return ret
		def fake_print(*args):
			msg = ' '.join(args)
			self.printed_stuff2 += msg + '\n' 
		import project4
		project4.input = fake_input
		project4.print = fake_print
		inp = [
			'6', '3', 'EMPTY',
			'F 1 A W F', '', '', '', '', '', '',
			'F 2 A E S', '', '', '', '', '', '',
			'F 3 A Z E', '', '', '', '', '', '',
			'', 'Q'
		]

		expected = '|         |\n|         |\n|         |\n|         |\n| W  E  Z |\n| F  S  E |\n --------- \n'
		project4.run_program()
		self.assertEqual(self.printed_stuff2[-1 * len(expected):], expected)

	def test_vertical_match(self):
		inp = ''
		self.printed_stuff3 = ''
		self.last_input_index3 = 0
		def fake_input():
				ll = self.last_input_index3
				self.last_input_index3 += 1
				ret = inp[ll]
				return ret
		def fake_print(*args):
			msg = ' '.join(args)
			self.printed_stuff3 += msg + '\n' 
		import project4
		project4.input = fake_input
		project4.print = fake_print
		inp = [
			'6', '3', 'EMPTY',
			'F 1 A A Q', '', '', '', '', '', '',
			'F 2 F E S', '', '', '', '', '', '',
			'F 3 F F F', '', '', '', '', '', '',
			'', 'Q'
		]

		expected = '|         |\n|         |\n|         |\n| A  F    |\n| A  E    |\n| Q  S    |\n --------- \n'
		project4.run_program()
		self.assertEqual(self.printed_stuff3[-1 * len(expected):], expected)

	def test_game_over(self):
		inp = ''
		self.printed_stuff4 = ''
		self.last_input_index4 = 0
		def fake_input():
				ll = self.last_input_index4
				self.last_input_index4 += 1
				ret = inp[ll]
				return ret
		def fake_print(*args):
			msg = ' '.join(args)
			self.printed_stuff4 += msg + '\n' 
		import project4
		project4.input = fake_input
		project4.print = fake_print
		inp = [
			'6', '3', 'EMPTY',
			'F 1 A A Q', '', '', '', '', '', '',
			'F 1 F E S', '', '', '',
			'F 1 J J K', '', '', '', '', '', '',
			'', 'Q'
		]

		expected = '| F       |\n| E       |\n| S       |\n| A       |\n| A       |\n| Q       |\n --------- \nGAME OVER\n'
		project4.run_program()
		self.assertEqual(self.printed_stuff4[-1 * len(expected):], expected)


if __name__=='__main__':
	unittest.main()
