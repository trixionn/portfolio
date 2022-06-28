import time
from colorama import init, Fore, Back, Style
import statistics as stcs
import math
import copy


if __name__ != '__main__':
	exit('THIS IS A SCRIPT, NOT A MODULE, BUCKAROO')


init()  # launching colorama

CELL_SIZE: tuple = (5, 3)  # width, height || only odd numbers!
MAP_SIZE: int = 8  # more than 6
half_of_map_size = math.trunc(MAP_SIZE / 2)
PLAYER1: str = '#'  # strings should consist of only 1 character
PLAYER2: str = '@'
PLAYER1_KING: str = '1'
PLAYER2_KING: str = '2'
EMPTY: str = ' '
if len({PLAYER1, PLAYER2, PLAYER1_KING, PLAYER2_KING, EMPTY}) != 5:
	print('WRONG SETTINGS')
	exit('bruh')
DEFAULT_MAP = [  # contains only playable cells
	[PLAYER1] * half_of_map_size,
	[PLAYER1] * half_of_map_size,
	[PLAYER1] * half_of_map_size,
	[PLAYER2] * half_of_map_size,
	[PLAYER2] * half_of_map_size,
	[PLAYER2] * half_of_map_size
]
_blank_lines = [[' '] * half_of_map_size] * (MAP_SIZE - 6)
for blank_line in _blank_lines:
	DEFAULT_MAP.insert(3, blank_line)


class Board:
	def __init__(self, size: int, cell_size: tuple, p1_figure, p2_figure, p1_king, p2_king, empty: str, default_map):
		"""p1, p2 figures and empty are characters that represents figures of 1st, 2nd player and empty spaces"""

		self.checker_to_move = None
		self.size = size
		self.cell_size = cell_size
		self.p1 = p1_figure
		self.p2 = p2_figure
		self.kings = {
			self.p1: p1_king,
			self.p2: p2_king
		}
		self.opponents = {
			self.p1: (self.p2, p2_king),
			p1_king: (self.p2, p2_king),
			self.p2: (self.p1, p1_king),
			p2_king: (self.p1, p1_king)
		}
		self.empty = empty
		self.valid_characters = p1_figure, p2_figure, p1_king, p2_king, empty
		self.center = stcs.median(range(cell_size[0])), stcs.median(range(cell_size[1]))
		self.field = Board.create_new_map(size, cell_size, empty, self.center, default_map)
		self.playable_field = self.clear_field()

	def make_move(self, from_cell, target_cell, player_turn):
		cords = Board.convert_cords(from_cell, self.size), Board.convert_cords(target_cell, self.size)

		if cords == (0, 0):  # exception
			return 'BC'  # bad coordinates
		if cords[0] != self.checker_to_move and self.checker_to_move is not None:
			return 'LM'  # last move
		if self.playable_field[cords[0][0]][cords[0][1]] not in (player_turn, self.kings[player_turn]):
			return 'WS'  # wrong side
		kill_moves = self.get_available_moves(player_turn)
		if len(kill_moves) != 0 and cords[0] not in kill_moves:
			return 'SK'  # should kill
		moves = self.get_moves(self.playable_field, cords[0])
		# print(moves)

		if cords[1] in moves[0]:
			# cords[0] is from
			# cords[1] is where
			if moves[1]:  # if player can kill someone
				try:
					killed_cords = moves[1][cords[1]]
					self.playable_field[killed_cords[0]][killed_cords[1]] = self.empty
				except KeyError:
					return 'KM'  # kill missed

			if player_turn == self.p1 and cords[1][0] == self.size-1:  # 1st player reaches the bottom
				self.playable_field[cords[1][0]][cords[1][1]] = self.kings[self.p1]
			elif player_turn == self.p2 and cords[1][0] == 0:  # 2nd player reaches the top
				self.playable_field[cords[1][0]][cords[1][1]] = self.kings[self.p2]
			else:  # nothing special
				self.playable_field[cords[1][0]][cords[1][1]] = self.playable_field[cords[0][0]][cords[0][1]]

			self.playable_field[cords[0][0]][cords[0][1]] = self.empty

			self.field = Board.create_new_map(self.size, self.cell_size, self.empty, self.center, self.playable_field)
			new_checker = self.get_moves(self.playable_field, cords[1])
			if new_checker[1] and moves[1]:  # if this checker still has killing moves
				self.checker_to_move = cords[1]
			else:
				self.checker_to_move = None

			win_check = self.check_win()
			if win_check == self.p1:
				return 'P1WIN'
			elif win_check == self.p2:
				return 'P2WIN'

			if moves[1]:
				if self.checker_to_move is None:
					return 'Killed'
				else:
					return 'One more'  # player must make one more move

			return 'Done'
		else:
			return 'NM'  # no moves

	def clear_field(self) -> list:
		"""returns map with only playble cells"""

		clear_field = []
		clear_rows = []
		playable_rows = []

		for row in range(self.center[1], self.size * self.cell_size[1], self.cell_size[1]):  # from second row every 3rd row
			playable_rows.append(self.field[row])

		for row in playable_rows:
			temp_clear_row = []

			for column in row:
				if column in self.valid_characters:
					temp_clear_row.append(column)
			clear_rows.append(temp_clear_row)

		white = True  # color that row starts with
		for clear_row in clear_rows:
			temp_clear_row = []
			step = self.cell_size[0] * 2
			start = self.center[0] + self.cell_size[0] * white

			for ch in range(start, self.size * self.cell_size[0], step):
				temp_clear_row.append(clear_row[ch])
			clear_field.append(temp_clear_row)
			white = not white

		return copy.deepcopy(clear_field)

	def get_available_moves(self, turn):
		"""returns list of checkers' cords that can kill someone"""

		total_moves = []
		for row in range(math.trunc(self.size)):
			for column in range(math.trunc(self.size/2)):
				checking = self.playable_field[row][column]

				if checking in self.opponents[self.opponents[turn][0]]:
					checker_result = self.get_moves(self.playable_field, (row, column))

					if len(checker_result[1]) > 0:
						total_moves.append((row, column))
		return total_moves

	def get_moves(self, clear_map: list, x: tuple):
		"""returns list of available moves
		also returns a dict of killed cells
		x is from_cell"""

		available_moves = []
		killed = dict()
		player_turn = clear_map[x[0]][x[1]]
		if player_turn in (self.p1, self.kings[self.p1]):
			self_king = self.kings[self.p1]
		else:
			self_king = self.kings[self.p2]

		if player_turn == self_king:
			rows = tuple(range(x[0]+1, len(clear_map))), tuple(range(x[0]-1, -1, -1))  # ((lower), (higher))

			if x[0] % 2 == 0:
				column_steps = ((0, -1), (1, 0))  # (left steps), (right steps)
			else:
				column_steps = ((-1, 0), (0, 1))  # (left steps), (right steps)

			left_column = []
			right_column = []
			left = True
			for step_direction in column_steps:
				total_shift = 0
				for _ in range(self.size):
					for step in step_direction:
						total_shift += step

						if x[1] + total_shift < 0 or x[1] + total_shift >= self.size / 2:
							break

						if left:
							left_column.append(x[1] + total_shift)
						else:
							right_column.append(x[1] + total_shift)
				left = not left

			for row_direction in rows:
				for column_direction in (left_column, right_column):
					enemy = False, (0, 0)  # (already met enemy in the line), (his cords)

					for row, column in zip(row_direction, column_direction):
						checking = clear_map[row][column]
						if enemy[0] is True and checking != self.empty:
							break
						elif checking in self.opponents[self.opponents[player_turn][0]]:  # enemy of my enemy is my friend
							break
						if checking == self.empty:
							if enemy[0] is False:
								available_moves.append((row, column))
							else:  # enemy is True
								available_moves.append((row, column))
								killed.update({(row, column): enemy[1]})
						elif checking in self.opponents[player_turn]:
							enemy = True, (row, column)

		else:
			rows = ((x[0]-1, x[0]-2), (x[0]+1, x[0]+2))

			if x[0] % 2 == 0:
				columns_shift = ((0, -1), (1, 1))  # (left(simple, behind opp), right(simple, behind opp))
			else:
				columns_shift = ((-1, -1), (0, 1))  # (left(simple, behind opp), right(simple, behind opp))

			for row in rows:
				for c_shift in columns_shift:
					if row[0] < 0 or x[1] + c_shift[0] < 0:
						continue

					try:
						checking_place = clear_map[row[0]][x[1] + c_shift[0]]
						if checking_place == self.empty:
							if player_turn == self.p1 and row[0] > x[0]:
								available_moves.append((row[0], x[1] + c_shift[0]))
							elif player_turn == self.p2 and row[0] < x[0]:
								available_moves.append((row[0], x[1] + c_shift[0]))
						elif checking_place in (player_turn, self_king):
							continue
						elif checking_place in self.opponents[player_turn]:
							# print(f'opponent approaching, checking {row[1]}, {x[1] + c_shift[1]}')
							if row[1] < 0 or x[1] + c_shift[1] < 0:
								continue

							checking_place = clear_map[row[1]][x[1] + c_shift[1]]  # checking behind an enemy
							if checking_place == self.empty:
								# print('and i can kill him')
								available_moves.append((row[1], x[1] + c_shift[1]))
								killed.update({(row[1], x[1] + c_shift[1]): (row[0], x[1] + c_shift[0])})
					except IndexError:
						# print('oh my, thats beyond my power')
						continue

		return available_moves, killed

	@staticmethod
	def convert_cords(cords, map_size: int) -> tuple:
		"""hard to explain, it converts user's input into a place in clear field"""

		try:  # some exceptions
			if int(cords[0]) > map_size or int(cords[1]) > map_size:
				return 0, 0
		except ValueError:
			return 0, 0

		even_nums = len(tuple(filter(lambda _: _ % 2 == 0 and _ != 0, map(int, cords))))
		if even_nums != 1:  # in cords one of nums should be even and another one should be odd
			return 0, 0

		output = [int(cords[0]) - 1]
		col = int(cords[1])
		if col % 2 == 0:
			output.append(int((col / 2) - 1))
		else:
			output.append(math.trunc(col / 2))
		return tuple(output)

	@staticmethod
	def create_new_map(size: int, cell_size: tuple, empty: str, center, layout):
		"""creates new map, to get a map - you need self.field"""

		if size < 7:
			return 'Size cant be smaller than 7 cells'

		new_map = []
		black = True  # second color

		for row in range(size):
			for cell_row in range(cell_size[1]):
				new_row = ''

				for column in range(size):
					playable = (column + int(black)) % 2 == 0

					for cell_column in range(cell_size[0]):
						if playable:
							new_row += Back.BLACK
							if (cell_column, cell_row) == center:
								converted_cords = Board.convert_cords((row+1, column+1), size)
								new_row += layout[converted_cords[0]][converted_cords[1]]
							else:
								new_row += empty + Style.RESET_ALL
						else:
							new_row += Back.WHITE
							new_row += empty + Style.RESET_ALL

				new_map.append(new_row)

			black = not black

		return new_map

	def check_win(self):
		"""returns the winner if there is else False"""

		player1_alive = False
		player2_alive = False

		for p_row in self.playable_field:
			for cell in p_row:
				if cell in (self.p1, self.kings[self.p1]):
					player1_alive = True
				elif cell in (self.p2, self.kings[self.p2]):
					player2_alive = True

		if player1_alive and player2_alive:
			return False
		else:
			if player1_alive is False:
				return self.p2
			elif player2_alive is False:
				return self.p1

	def display(self):
		"""displays the map"""

		# horizontal nums
		print(Fore.LIGHTGREEN_EX + ' ' * self.center[0], end='')
		for num_column in range(1, self.size + 1):
			print(str(num_column) + ' ' * (self.cell_size[0] - 1), end='')
		print(Style.RESET_ALL)

		output = ''
		for row in range(len(self.field)):
			output += self.field[row]
			if row < self.center[1]:
				pass
			elif row == self.center[1]:
				output += Fore.LIGHTGREEN_EX + '1'
			elif (row-self.center[1]) % self.cell_size[1] == 0:
				output += Fore.LIGHTGREEN_EX + str(int(row / self.cell_size[1] + 1))
			output += '\n'
		print(output, Style.RESET_ALL, sep='')


Map = Board(MAP_SIZE, CELL_SIZE, PLAYER1, PLAYER2, PLAYER1_KING, PLAYER2_KING, EMPTY, DEFAULT_MAP)
player = 1
players = {
	1: PLAYER1,
	2: PLAYER2,
	PLAYER1: 2,  # for player switch
	PLAYER2: 1  # same ^
}

Map.playable_field[1][2] = PLAYER1
Map.field = Board.create_new_map(MAP_SIZE, CELL_SIZE, EMPTY, Map.center, Map.playable_field)

game = True
while game:
	Map.display()
	print(Fore.LIGHTGREEN_EX, end='')
	if Map.checker_to_move is None:
		print(f'Ход игрока {player}')
	else:
		print(f'Эта шашка еще может рубить, игрок {player}, продолжите ход')

	move_done = False
	while not move_done:
		print(Style.RESET_ALL, end='')
		user_cord_x = input('\nВведите координаты шашки: ')
		user_cord_y = input('Введите куда хотите сходить: ')

		result = Map.make_move(user_cord_x, user_cord_y, players[player])
		match result:
			case 'Done':
				print(Fore.LIGHTGREEN_EX + 'Шашка успешно сходила!')
				move_done = True
			case 'Killed':
				print(Fore.LIGHTGREEN_EX + 'Вы успешно срубили чужую шашку!')
				move_done = True
			case 'One more':
				print(Fore.LIGHTGREEN_EX + 'Вы успешно срубили чужую шашку!')
				player = players[players[player]]  # switch the player 2 times
				move_done = True
			case 'SK':
				print(Back.LIGHTRED_EX + 'Вы обязаны рубить если есть такая возможность')
			case 'NM':
				print(Back.LIGHTRED_EX + 'Эта Шашка не может так ходить')
			case 'KM':
				print(Back.LIGHTRED_EX + 'Вы обязаны рубить, если есть такая возможность')
			case 'BC':
				print(Back.LIGHTRED_EX + 'Неверные координаты')
			case 'LM':
				print(Back.LIGHTRED_EX + 'Продолжите свой ход')
			case 'WS':
				print(Back.LIGHTRED_EX + f'Ваша фигура это {players[player]}, не путайте!')
			case 'P1WIN':
				print()
				Map.display()
				print(Fore.LIGHTGREEN_EX + 'Поздравляем! Игрок 1 выйграл! Спасибо за игру')
				move_done = True
				game = False
			case 'P2WIN':
				print()
				Map.display()
				print(Fore.LIGHTGREEN_EX + 'Поздравляем! Игрок 2 выйграл! Спасибо за игру')
				move_done = True
				game = False
		time.sleep(1)

	print(Style.RESET_ALL)

	if player == 1:
		player = 2
	elif player == 2:
		player = 1

input()
