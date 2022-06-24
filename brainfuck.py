# -------------- BRAINFUCK

MEMORY_SIZE = 30_000
index = 0
memory = [0] * MEMORY_SIZE

your_code = '++++++[>++++++++++++<-]>.\
>++++++++++[>++++++++++<-]>+.\
+++++++.\
.\
+++.\
>++++[>+++++++++++<-]>.\
<+++[>----<-]>.\
<<<<<+++[>+++++<-]>.\
>>.\
+++.\
------.\
--------.\
>>+.'


def get_clear(code):
	brackets = 1
	for index, ch in enumerate(code[1:]):
		if ch == '[':
			brackets += 1
		elif ch == ']':
			brackets -= 1
		if brackets == 0:
			return code[1:index+1], index+1


def brain(code):
	global index, memory
	skip = 0
	code_length = len(code)
	
	for op in range(code_length):
		if op+skip == code_length:
			break
		
		if code[op+skip] == '.':
			print(chr(int(memory[index])), end='')
			
		elif code[op+skip] == ',':
			memory[index] = ord(input())
			
		elif code[op+skip] == '>':
			index += 1
			
		elif code[op+skip] == '<':
			index -= 1
			
		elif code[op+skip] == '+':
			memory[index] += 1
			
		elif code[op+skip] == '-':
			memory[index] -= 1
			
		elif code[op+skip] == '[':
			clear_code = get_clear(code[op+skip:])
			skip += clear_code[1]
			while memory[index] != 0:
				brain(clear_code[0])
				

brain(your_code)
