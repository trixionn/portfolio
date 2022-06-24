#-----------WORDLE
from colorama import Fore, Back, Style, init
from random import choice

init()

# ————— Settings
# by default duplicate mode is disabled
# enabled: doesnt count duplicates before him
# ex: secret: WIDOW, guess: ROBOT
# out: (FALSE, RIGHT, FALSE, RIGHT, FALSE)
# if disabled: ex: secret: TOWEL, guess: WIDOW
# out: (RIGHT, FALSE, FALSE, RIGHT, FALSE)
DUPLICATE_MODE = False
PLAYERS = 1
WORD_LENGTH = 5
TRYS = 6 # amount of trys
# ———————————

RIGHT_POS = 'G'  # all's right
RIGHT = 'Y'  # there's same letter in secret word
FALSE = ' '  # completely wrong
# colors of spots
colors = {
	RIGHT_POS: Back.GREEN,
	RIGHT: Back.CYAN,
	FALSE: Back.LIGHTRED_EX
}

words = (
	'ОСЕНЬ', 'КАМЫШ', 'ВЫВОД', 'ХОЛОД',
	'ПУЛЬТ', 'МЫШКА', 'КЕПКА', 'ГРОЗА',
	'НОСОК', 'ЦИФРА', 'ШТАНЫ', 'ШАХТА',
	'ЛОЖКА', 'ФОТОН', 'БАНДА', 'КОВЁР',
	'ЦАПЛЯ', 'СПИРТ', 'МЯЧИК', 'СТЕНА',
	'СОПЛЯ', 'ТАНЕЦ', 'ШЛЯПА', 'ШКАЛА',
	'КАРТА', 'ДВЕРЬ', 'СЛАВА', 'ЭКРАН',
	'ЧАСТЬ', 'БЕЛЫЙ', 'ГЕРОЙ', 'БУРАН',
	'АРБУЗ', 'ЦВЕТЫ', 'ЧАШКА', 'ТУМАН',
	'КРЫЛО', 'ПРОЁМ', 'БИЛЕТ', 'ЖАБРЫ',
	'КОСТИ', 'ЖЕСТЬ', 'ПРАВО', 'НАЛОГ',
	'РАМКА', 'АКТЁР', 'ГЛАВА', 'ЗАРЯД',
	'КОШКА', 'АМЁБА', 'ПЛАТА', 'БИЛЕТ',
	'ЛОДКА', 'ВОКАЛ', 'ИЗГИБ', 'ДОЖДЬ',
	'ШАКАЛ', 'КАБАН', 'СЕРЫЙ', 'ШЁПОТ',
	'ГРУША', 'НАБОР', 'УЛИЦА', 'ЖОКЕЙ',
	'ВАГОН', 'СЛЕЗА', 'ВЕТЕР', 'ЖЕСТЬ',
	'ЯКОРЬ', 'СПОРТ', 'АКУЛА', 'АФИША',
	'БЛАГО', 'БЕТОН', 'ВАФЛЯ', 'ВЫВИХ',
	'ГАРАЖ', 'ГОЛОС', 'ДОБРО', 'ДЯТЕЛ',
	'АБОРТ', 'БАЛКА', 'БАНКА', 'РУЧКА'
)
wordle_help = 'Загадывается случайное\
 слово. Человеку необходимо при\
 помощи нескольких попыток\
 отгадать его. Если буква в слове,\
 которое написали для отгадки,\
 есть в секретном слове, то она\
 загорится голубым, если буква была\
 отгадана правильно, то она загорится\
 зеленым. Для больших подробностей\
 посмотрите в интернете'


def display(word: str, spots: tuple[str]) -> None:
	output = ''
	for letter in range(len(word)):
		output += colors[spots[letter]] + word[letter].upper()
	print(output + Style.RESET_ALL)
	

def get_spots(guess, secret) -> tuple[str]:
	output = ''
	
	secret_lets = {}
	for uniq in secret:
		if uniq in secret_lets:
			secret_lets[uniq] += 1
		else:
			secret_lets.update({uniq: 1})
			
	if DUPLICATE_MODE:
		for g, s in zip(guess, secret):
			if g not in secret:
				output += FALSE
			elif g == s:
				output += RIGHT_POS
			elif g in secret:
				output += RIGHT
	else:
		# we need to reserve places for RIGHT_POS letters
		for g, s in zip(guess, secret):
			if g == s:
				secret_lets[s] -= 1
		for g, s in zip(guess, secret):
			if g not in secret:
				output += FALSE
			elif g == s:
				secret_lets[g] -= 1
				output += RIGHT_POS
			elif g in secret:
				if secret_lets[g] > 0:
					secret_lets[g] -= 1
					output += RIGHT
				else:
					output += FALSE
	return tuple(output)


print(Fore.GREEN + 'Знаете как играть в Wordle?\n' + Style.RESET_ALL)
already_know_rules = bool(input('Введите ENTER если знаете\n\n==> '))

if already_know_rules:
	print(Back.GREEN + '\n' + wordle_help + '\n' + Style.RESET_ALL)
else:
	print()

config = None
print(Back.LIGHTBLUE_EX + 'Хотите изменить настройки?' + Style.RESET_ALL)
print(Fore.GREEN + f"""
Настройки:
Режим дупликатов: {int(DUPLICATE_MODE)}
Игроков: {PLAYERS}
Кол-во попыток: {TRYS}
Длина слова: {WORD_LENGTH}""" + Style.RESET_ALL)

while not (config is True or config is False):
	print(Back.LIGHTBLUE_EX + '\n1 - Да\n0 - Нет' + Style.RESET_ALL)
	config_input = input('\n==>  ')
	try:
		config = bool(int(config_input))
	except ValueError:
		print(Back.LIGHTRED_EX + 'Ошибка! Повторите ввод')

while config:
		try:
			print(Back.LIGHTBLUE_EX + '\nУстановите значение для режима дупликатов' + Style.RESET_ALL)
			print(Fore.GREEN + '\nПомощь:\nПри включенном режиме дупликатов повторения букв не учитываются при окрашивании')
			
			DUPLICATE_MODE = int(input(Style.RESET_ALL + '\n==> '))
			if DUPLICATE_MODE not in (0, 1):
				print(Back.LIGHTRED_EX + 'Ошибка! Режим дупликатов может принять только значаения 0 или 1\n')
				raise ValueError
		except ValueError:
			print(Back.LIGHTRED_EX + 'Ошибка! Повторите ввод\n')
			continue
		DUPLICATE_MODE = bool(DUPLICATE_MODE)
		
		try:
			print(Back.LIGHTBLUE_EX + '\nУстановите значение для кол-ва игроков' + Style.RESET_ALL)
			print(Fore.GREEN + '\nПомощь:\nПри одном игроке выбирается случайное слово, а вам его потребуется угадать\n')
			
			PLAYERS = int(input(Style.RESET_ALL + '\n==> '))
			if PLAYERS not in (1, 2):
				print(Back.LIGHTRED_EX + 'Ошибка! Количество игроков может быть только 1 или 2\n')
				raise ValueError
		except ValueError:
			print(Back.LIGHTRED_EX + 'Ошибка! Повторите ввод\n')
			continue
		
		try:
			print(Back.LIGHTBLUE_EX + '\nУстановите значение для кол-ва попыток' + Style.RESET_ALL)
			print(Fore.GREEN + '\nПомощь:\nКоличество попыток, которые даются игроку на то, чтобы угадать слово\n')
			
			TRYS = int(input(Style.RESET_ALL + '\n==> '))
			if TRYS < 1:
				print(Back.LIGHTRED_EX + 'Ошибка! Количество попыток не может быть меньше одной\n')
				raise ValueError
		except ValueError:
			print(Back.LIGHTRED_EX + 'Ошибка! Повторите ввод\n')
			continue
		
		try:
			print(Back.LIGHTBLUE_EX + '\nУстановите значение для длины загадываемого слова' + Style.RESET_ALL)
			print(Fore.GREEN + '\nПомощь:\nДлина слова, которое вам придется отгадывать (при одном игроке можно выбрать только длину в 5 букв)\n' + Style.RESET_ALL)
			
			if PLAYERS == 1:
				WORD_LENGTH = 5
				print(Back.LIGHTBLUE_EX + 'Длина слова выбрана автоматически' + Style.RESET_ALL)
			else:
				WORD_LENGTH = int(input(Style.RESET_ALL + '\n==> '))
				if WORD_LENGTH < 1:
					print(Back.LIGHTRED_EX + 'Ошибка! Длина слова не может быть меньше 1 буквы\n')
					raise ValueError
			config = False
		except ValueError:
			print(Back.LIGHTRED_EX + 'Ошибка! Повторите ввод\n')
			continue

secret_word = None
if PLAYERS == 1:
	secret_word = choice(words)
else:
	secret_word_chosen = False
	while not secret_word_chosen:
		print(Back.LIGHTBLUE_EX + f'\nЗагадайте слово длиной в {WORD_LENGTH} букв')
		secret_word = input(Style.RESET_ALL + '\n==> ').upper()
		if len(secret_word) != WORD_LENGTH:
			print(Back.LIGHTRED_EX + 'Длина вашего слова не соответствует правилам')
			continue
		secret_word_chosen = True

# ————— MAIN GAME
print('\n' * 200)
print(Fore.LIGHTYELLOW_EX + '\nИгра началась! (слева будет писаться номер попытки' + Style.RESET_ALL)

for num_try in range(1, TRYS+1):
	word_chosen = False
	while not word_chosen:
		guess_word = input(f'\n{num_try}/{TRYS}: ').upper()
		if len(guess_word) != WORD_LENGTH:
			print(Style.RESET_ALL + Back.LIGHTRED_EX + 'Ошибка! Длина слова не соответствует правилам' + Style.RESET_ALL)
			continue
		word_chosen = True
	
	print('Вывод: ', end='')
	spots = get_spots(guess_word, secret_word)
	display(guess_word, spots)
	
	if all(map(lambda x: x == RIGHT_POS, spots)):
		print(Back.GREEN + f'\nВы выйграли! Поздравляю!' + Style.RESET_ALL)
		break
else:
	print(Back.LIGHTRED_EX + f'\nВы програли! Загаданным словом было {secret_word} удачи в следущий раз!' + Style.RESET_ALL)
