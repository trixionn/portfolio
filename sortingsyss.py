import random
import time


class Sorting:
	_decimal = 2  # nums in decimal
	_chance_repeat = 15 # chance of repeating of a num in mode 'repeats'
	
	
	@staticmethod
	def createRlist(len, type='regular',  float=False):
		new_rlist = []
		
		# if it shouldn't be random
		if type == 'regular':
			for n in range(len):
				num = n
				# if it should has float nums
				if float:
					num += round(random.random(), Sorting._decimal)
				# adding nums from x to y
				new_rlist.append(num)
			# randomizing
			random.shuffle(new_rlist)
			return new_rlist
		elif type == 'random':
			for i in range(len):
				# random int from -len to len
				num = random.randint(-len+1, len-1)
				if float:
					num += round(random.random(), Sorting._decimal)
				new_rlist.append(num)
			return new_rlist
		elif type == 'repeats':
			stop = len
			for n in range(len):
				if n == stop:
					break
				num = n
				if float:
					float = lambda: round(random.random(), Sorting._decimal)
					num += float()
				new_rlist.append(num)
				# repeating adds extra nums, therefore we need to stop earlier to total nums is len
				if chance(Sorting._chance_repeat):
					new_rlist.append(num + float())
					stop -= 1
			# final shuffling
			random.shuffle(new_rlist)
			return new_rlist
		
			
	def bubblesort(rlist):
		name = 'Bubble Sort'
		# take time of beginning
		start_time = time.time()
		
		sorted = rlist.copy()
		length = len(sorted)
		# go through list n times
		for i in range(length-1):
			for n in range(length-i-1):
				# if num in front is less then swap
				if sorted[n] > sorted[n + 1]:
					sorted[n], sorted[n + 1] = sorted[n + 1], sorted[n]
					
		# evelate difderence between start and now
		end_time = round(time.time() - start_time, 5)
		return sorted, end_time, name
	
	
	# counting sort doesnt work with float and rand
	def countingsort(rlist):
		name = 'Counting Sort'
		# preventing from accidental negative or float nums
		for n in rlist:
			# if num is less zero or its not int
			if n < 0 or not n % 1 == 0:
				return 'You shouldnt use counting sort', None, None
		
		start_time = time.time()
		
		sorted = rlist.copy()
		counting = []
		# adding much zeros as len of the list
		for i in range(len(sorted)):
			counting.append(0)
		for n in sorted:
			counting[n] += 1
		sorted.clear()
		index = 0
		for n in counting:
			for _i in range(n):
				sorted.append(index)
			index += 1
				
		end_time = round(time.time() - start_time, 5)
		return sorted, end_time, name
		
		
	# to know how radix works https://youtu.be/ujb2CIWE8zY
	def radixsort(rlist):
		name = 'Radix Sort'
		# preventing from accidental negative or float nums
		for n in rlist:
			# if num is less zero or its not int
			if n < 0 or not n % 1 == 0:
				return 'You shouldnt use radix sort', None, None

		start_time = time.time()
		unsorted = rlist.copy()
		output = [c * 0 for c in range(len(unsorted))]
		counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		digit = 1
		sort_len = len(unsorted)
		
		# finding the biggest digit
		for i in range(sort_len):
			unsorted[i] = str(unsorted[i])
			if len(unsorted[i]) > digit:
				digit = len(unsorted[i])
		
		# to get digits of nums we need to turn [1, 2, 3, 10] into [01, 02, 03, 10]
		for i in range(sort_len):
			if len(unsorted[i]) < digit:
				unsorted[i] = '0' * (digit - len(unsorted[i])) + unsorted[i]
		
		# the main cycle
		for d in range(1, digit+1):
			
			#counting digits
			for i in range(sort_len):
				counts[int(unsorted[i][-d])] += 1
			
			# prefix sum
			for n in range(1, 10):
				counts[n] = int(counts[n-1]) + int(counts[n])
			
			# putting nums from the unsorted array to output in correct order according to current digit
			for indx in range(1, len(unsorted)+1):
				counts[int(unsorted[-indx][-d])] -= 1
				output[counts[int(unsorted[-indx][-d])]] = unsorted[-indx]
			unsorted = output.copy()
			counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		
		# turning strings back into ints
		index = 0
		for i in output:
			output[index] = int(output[index])
			index += 1
			
		end_time = round(time.time() - start_time, 5)
		return output, end_time, name
		
		
	def pythonsort(rlist):			
		name = 'Python in-built sort'
		start_time = time.time()
		sorted_list = sorted(rlist)
		end_time = round(time.time() - start_time, 5)
		return sorted(rlist), end_time, name


def chance(perc):
	if random.random() < perc / 100:
		return True
	else:
		return False


rlist = Sorting.createRlist(10000, 'random')
print(f'Изначальный список: {rlist}')

sorted_list = Sorting.bubblesort(rlist)
print(f'Результат: {sorted_list[0]}\n\nВремени затрачено: {sorted_list[1]}\nНазвание сортировки: {sorted_list[2]}')

# сделай норм createRlist, сначала сгенерируй последовательность, потом ее подправляй
