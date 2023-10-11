import new_game_mechanics
import pygame
import time

_frame_rate = 30
init_width = 400
init_height = 500
background_color = pygame.Color(128, 128, 128)
grid_square_color_black = pygame.Color(0, 0, 0)

def game_start_info():
    rows = 13
    columns = 6
    rows_list = None
    return new_game_mechanics.GameState(rows, columns, rows_list)


class Display:

	def __init__(self):
		self.running = True
		self.gem_list = {'Y':(255, 246, 137),
						 'G':(182, 255, 133),
						 'B':(52, 127, 196),
						 'R':(235, 81, 51),
						 'P':(184, 61, 169),
						 'T':(196, 162, 135),
						 'W':(255, 238, 219),
						 'grey':(100, 100, 100),
						 ' ': (0, 0, 0)}

	def _redraw(self):
		background = pygame.display.get_surface()
		background.fill(background_color)
		self.draw_grid(background)
		pygame.display.flip()

	def draw_grid(self, background):
		(window_width, window_height) = background.get_size()
		gridsquare_width = 0.075 * window_width
		gridsquare_height = 0.06 * window_height
		space_btwn_squares = 1
		topleft_pixel_y = (window_height - ((gridsquare_height * 13) + (space_btwn_squares * 12))) / 2
		for row in range(13):
			topleft_pixel_x = (window_width - ((gridsquare_width * 6) + (space_btwn_squares * 5))) / 2
			for col in range(6):
				color = self.convert_gem_to_color(self.game_state.field[col][row])
				is_faller_square = False
				if self.game_state.falling_tuple is not None:
					is_faller_square = (col, row) in self.game_state.falling_tuple[3]
				self.draw_square(	topleft_pixel_x, topleft_pixel_y, 
									gridsquare_width, gridsquare_height, 
									color, is_faller_square)
				
				topleft_pixel_x += (0.075 * window_width + 1)
			topleft_pixel_y += (0.06 * window_height + 1)

	def convert_gem_to_color(self, square_val):
		if square_val in self.gem_list:
			return pygame.Color(*self.gem_list[square_val])
		raise ValueError('unknown square_val:', square_val)

	def draw_square(self, topleft_pixel_x, topleft_pixel_y, gridsquare_width, gridsquare_height, grid_color, is_faller_square=False):
		surface = pygame.display.get_surface()
		grid_square = (topleft_pixel_x, topleft_pixel_y, gridsquare_width, gridsquare_height)
		if is_faller_square:
			pygame.draw.rect(surface, self.gem_list['grey'], grid_square)
			grid_square = (topleft_pixel_x - 1, topleft_pixel_y - 1, gridsquare_width - 5, gridsquare_height - 5)
			pygame.draw.rect(surface, grid_color, grid_square)
		else:
			pygame.draw.rect(surface, grid_color, grid_square)


	def _update_window(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.end_game()

		# self.handle_keys()

	def handle_keys(self, keys):
		# keys = pygame.key.get_pressed()
		for key in keys:
			if key == ' ':
				self.game_state.rotate()
			elif key == '<':
				self.game_state.move_faller_left()
			elif key == '>':
				self.game_state.move_faller_right()

	def get_key(self):
		keys = pygame.key.get_pressed()
		pressed_keys = []
		if keys[pygame.K_SPACE]:
			pressed_keys.append(' ')
		elif keys[pygame.K_LEFT]:
			pressed_keys.append('<')
		elif keys[pygame.K_RIGHT]:
			pressed_keys.append('>')
		return pressed_keys

	def end_game(self):
		self.running = False

	def display_game_window(self, size: (int, int)):
		pygame.display.set_mode(size, pygame.RESIZABLE)

	def run(self):
		pygame.init()
		self.game_state = game_start_info()
		try:
			clock = pygame.time.Clock()
			time_a = time.time()
			self.display_game_window((init_width, init_height))
			last_input = []
			while self.running:
				clock.tick(_frame_rate)
				time_b = time.time()
				temp_key = self.get_key()
				if len(temp_key) != 0:
					last_input = temp_key
				self._update_window()
				if (time_b - time_a) >= 1:
					self.handle_keys(last_input)
					self._redraw()
					if self.game_state.is_frozen():
						self.game_state.create_faller_list()
					elif not self.game_state.is_frozen():
						self.game_state.drop_faller_list()
					self._redraw()
					if self.game_state.game_is_over():
						break
					time_a = time.time()
					last_input = {}
		
		finally:
			pygame.quit()


if __name__=='__main__':
	Display().run()
