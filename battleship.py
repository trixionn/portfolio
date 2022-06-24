#---------BATTLESHIP
import pandas as pd
import copy
import time
from colorama import init, Fore, Back, Style
init()


ship_s = '#'
empty_s = '©'  # empty
none_s = '.'  # unknown
strike_s = 'X'
dict = {
	'А': 0, 
	'Б': 1, 
	'В': 2, 
	'Г': 3, 
	'Д': 4, 
	'Е': 5, 
	'Ж': 6, 
	'З': 7, 
	'И': 8, 
	'К': 9
}
directions = {
	'л': 1,
	'в': 2,
	'п': 3,
	'н': 4
}
move_delay = 1.2  # sec


def create_map(empty_line):
	map = [empty_line.copy() for _ in range(10)]
	return map
	
	
line = [_ for _ in none_s * 10]  # ~ * 10
# map of player 1 that player 2 will see
p1forp2 = create_map(line)
# map of player 2 that player 1 will see
p2forp1 = create_map(line)


def display(map, alphabet):
	m = pd.DataFrame(map, index=alphabet)
	print(Style.BRIGHT, Back.MAGENTA, m, Style.RESET_ALL, sep='')
	
	
def check_win(map, ships, strike_sign):
	strikes = 0
	for row in map:
		for cell in row:
			if cell == strike_sign:
				strikes += 1

	if strikes >= len(ships):
		return True
	return False
	
	
def put(map, place, length, direction, ship_sign):
	error_status = False
	
	
	def can_put(map, place, ship_sign):
		error_index_out_of_map = 'Корабль не может уходить за границы карты'
		error_already_placed = 'Место уже занято'
		map_width = len(map[0])
		map_height = len(map)
		# checking is the place in the field
		try:
			map[place[0]][place[1]] is True
		except IndexError:
			return error_index_out_of_map
		if place[0] < 0 or place[1] < 0:
			return error_index_out_of_map
		
		for row_check in range(-1, 2):
			for column_check in range(-1, 2):
				
				# if coordinates are negative (i shouldnt check the last element) or are too big
				if place[0]+row_check < 0 or place[1]+column_check < 0:
					continue
				elif place[0]+row_check >= map_height or place[1]+column_check >= map_width:
					continue

				if map[place[0]+row_check][place[1]+column_check] == ship_sign:
					return error_already_placed
		return True
	
	
	new_m = copy.deepcopy(map)
	spec_sym = '%'  # special symbol for temporary building of the ship
	for shift in range(length):
		if direction == 1:  # left
			# shifted place
			shift_plc = (place[0], place[1]-shift)
			result = can_put(new_m, shift_plc, ship_sign)
			if result is True:
				new_m[shift_plc[0]][shift_plc[1]] = spec_sym
			else:  # if it cant put ships part
				error_status = result
				
		elif direction == 2:  # up
			shift_plc = (place[0]-shift, place[1])
			result =  can_put(new_m, shift_plc, ship_sign)
			if result is True:
				new_m[shift_plc[0]][shift_plc[1]] = spec_sym
			else:
				error_status = result
			
		elif direction == 3:  # right
			shift_plc = (place[0], place[1]+shift)
			result = can_put(new_m, shift_plc, ship_sign)
			if result is True:
				new_m[shift_plc[0]][shift_plc[1]] = spec_sym
			else:
				error_status = result
			
		elif direction == 4:  # down
			shift_plc = (place[0]+shift, place[1])
			result = can_put(new_m, shift_plc, ship_sign)
			if result is True:
				new_m[shift_plc[0]][shift_plc[1]] = spec_sym
			else:
				error_status = result
				
		else:  # if direction != 1 or 2 or 3 or 4
			error_status = 'Указано неверное направление'
			
		if error_status is not False:
			return map, error_status
	
	# turning special syms into normal ship signs
	for row in range(len(map[0])):
		for cell in range(len(map)):
			if new_m[row][cell] == spec_sym:
				new_m[row][cell] = ship_sign
	
	return new_m, error_status
	

def ship_parts(cords, direction, length):
	output = []
	for shift in range(length):
		if direction == 1:  # left
			output.append((cords[0], cords[1]-shift))
		elif direction == 2:  # up
			output.append((cords[0]-shift, cords[1]))
		elif direction == 3:  # right
			output.append((cords[0], cords[1]+shift))
		elif direction == 4:  # down
			output.append((cords[0]+shift, cords[1]))
	return tuple(output)


def convert(input, dict, directions):
	"""input: 'Б4 п' output: ((1, 4), 3)"""
	cords, direction = input.split()
	cords = (dict[cords[0].upper()], int(cords[1]))
	direction = directions[direction.lower()]
	return cords, direction


def strike(map, strike_cords, ships, empty_sign, strike_sign):
	"""do an attack"""

	error = None
	new_m = copy.deepcopy(map)
	target = map[strike_cords[0]][strike_cords[1]]
	
	if target == empty_sign:
		error = 'Эта клетка пуста'
	elif target == strike_sign:
		error = 'Вы уже попали по этому кораблю'
	if error is not None:
	 	return map, error
	 
	 
	def check_ship(map, cords, ships, strike_sign, checked=None):
		"""checks is it a whole ship or just a part
		output: True if its the last part of a ship
		output: False if its not the last part of a ship
		"""
		new_m = copy.deepcopy(map)
		map_width = len(map[0])
		map_height = len(map)
		if checked is None:
			checked = []
		for row_shift in range(-1, 2):
			for column_shift in range(-1, 2):
				shft_crds = (cords[0]+row_shift, cords[1]+column_shift)
				
				# exceptions
				if shft_crds[0] < 0 or shft_crds[1] < 0:
					continue
				elif shft_crds[0] == cords[0] and shft_crds[1] == cords[1]:
					continue
				elif shft_crds[0] >= map_height or shft_crds[1] >= map_width:
					continue
				elif shft_crds in checked:
					continue
				if map[shft_crds[0]][shft_crds[1]] == strike_sign:
					checked.append(cords)
					if check_ship(map, shft_crds, ships,  strike_sign, checked):
						pass
					elif shft_crds in ships:
						return False
				elif shft_crds in ships:
					return False
		return True
		
		
	def destroy_ship(map, cords, strike_sign, empty_sign, checked=None):
		new_m = copy.deepcopy(map)
		map_width = len(map[0])
		map_height = len(map)
		if checked is None:
			checked = []
		for row_shift in range(-1, 2):
			for column_shift in range(-1, 2):
				
				shft_crds = (cords[0]+row_shift, cords[1]+column_shift)
				if shft_crds[0] < 0 or shft_crds[1] < 0:
					continue
				elif shft_crds[0] >= map_height or shft_crds[1] >= map_width:
					continue
				elif shft_crds in checked:
					continue
				
				if new_m[shft_crds[0]][shft_crds[1]] == strike_sign:
					checked.append(cords)
					new_m = destroy_ship(new_m, shft_crds, strike_sign, empty_sign, checked)
				else:
					new_m[shft_crds[0]][shft_crds[1]] = empty_sign
		return new_m


	# if cell is empty
	if strike_cords not in ships:
		new_m[strike_cords[0]][strike_cords[1]] = empty_sign
	# if its the last part of a ship
	elif check_ship(map, strike_cords, ships, strike_sign):
		new_m[strike_cords[0]][strike_cords[1]] = strike_sign
		new_m = destroy_ship(new_m, strike_cords, strike_sign, empty_sign)
		error = 'Hit'
	# if its a part of a ship
	else:
		new_m[strike_cords[0]][strike_cords[1]] = strike_sign
		error = 'Hit'
	return new_m, error


#test_map = [['', '', '', '', ''],
#						['', '', '', '', '×'],
#						['', '', '', '', '×'],
#						['', '', '', '', '×']]
#display(strike(test_map, (0, 4), [(0, 4), (1, 4), (2, 4), (3, 4)], '*', '×')[0], ['A', 'B', 'C', 'D'])
p1_ships = []  # will contain coordinates of
p2_ships = []  # ship parts, ex: (6, 3), (5, 2)
# contains lengths of every ship that will be used for the game
ships = (1, 1, 1, 1, 2, 2, 2, 3, 3, 4)  # default set
#ships = (2, 2, 3, 4)  # for tests and having fun
for player in range(1, 3):
	default_error = '=== Ошибка! Некорректный ввод'
	print(f'— Игрок {player}, расположите ваши корабли —\n')
	temp = create_map(line)
	for ship_len in ships:
		placed = False
		
		while not placed:
			error_output = default_error
			print('~' * 30 + '\n')
			display(temp, dict)
			print(f'\nДлина текущего корабля: {ship_len}')
			print('Введите сначала координаты, потом через пробел направление корабля')
			print('Пример: "ж5 в" (л - лево, в - верх, п - право, н - низ)')
			place = input('\n==> ')
			
			try:
				in_cords, in_dir = convert(place, dict, directions)
				temp, status_error = put(temp, in_cords, ship_len, in_dir, ship_s)
				if status_error is not False:
					error_output = status_error
					raise ValueError
				for cord in ship_parts(in_cords, in_dir, ship_len):
					if player == 1:
						p1_ships.append(cord)
					elif player == 2:
						p2_ships.append(cord)
				placed = True
				
			except (ValueError, KeyError, IndexError):
				print(Style.BRIGHT + Back.LIGHTRED_EX + error_output + Style.RESET_ALL)
				time.sleep(move_delay)

	print('~' * 30 + '\n')
	print('Ваше конечное поле:\n')
	display(temp, dict)
	time.sleep(4)
	print('\n' * 150 + 'ЭЙ, НЕ ПОДСМАТРИВАТЬ!!!')
	print('\n' * 30)


game = True
player = 1
while game:
	stroke = False
	if player == 1:
		print('\n———— Ход игрока 1 ————\n')
		time.sleep(move_delay)
		display(p2forp1, dict)
		
		while not stroke:
			inp_cords = input('Введите координаты для выстрела: ')
			try:
				coordinates = (dict[inp_cords[0].upper()], int(inp_cords[1]))
				result = strike(p2forp1, coordinates, p2_ships, empty_s, strike_s)
				
				if result[1] == 'Hit':
					player = 1
				elif result[1] is not None:
					print('\n' + result[1])
					raise ValueError
				else:
					player = 2
				
				p2forp1 = result[0]
				print('\n' + '\/' * 15 + '\n')
				print('~~~ Карта противника после выстрела ~~~\n')
				display(p2forp1, dict)
				time.sleep(3)
				stroke = True
			except (KeyError, ValueError, IndexError):
				print('=== Ошибка! Некорректный ввод')
				time.sleep(2)
				continue
			
			if check_win(p2forp1, p2_ships, strike_s):
				print(Back.LIGHTGREEN_EX + Style.BRIGHT + '\n== Игра окончена! Победа за игроком 1 ==' + Style.RESET_ALL)
				game = False
	
	elif player == 2:
		print('\n———— Ход игрока 2 ————\n')
		time.sleep(move_delay)
		display(p1forp2, dict)
		
		while not stroke:
			inp_cords = input('Введите координаты для выстрела: ')
			try:
				coordinates = (dict[inp_cords[0].upper()], int(inp_cords[1]))
				result = strike(p1forp2, coordinates, p1_ships, empty_s, strike_s)
				
				if result[1] == 'Hit':
					player = 2
				elif result[1] is not None:
					print('\n' + result[1])
					raise ValueError
				else:
					player = 1
					
				p1forp2 = result[0]
				print('\n' + '\/' * 15 + '\n')
				print('~~~ Карта противника после выстрела ~~~\n')
				display(p1forp2, dict)
				time.sleep(3)
				stroke = True
			except (KeyError, ValueError, IndexError):
				print('=== Ошибка! Некорректный ввод')
				time.sleep(2)
				continue
			
			if check_win(p1forp2, p1_ships, strike_s):
				print(Back.LIGHTGREEN_EX + Style.BRIGHT + '\n== Игра окончена! Победа за игроком 2 ==' + Style.RESET_ALL)
				game = False

input()