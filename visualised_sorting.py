import random
import numpy as np
import time
import math


def graph(list):
	height = max(list)
	length = len(list)
	nums = []
	EMPTY = '.'
	FILLED = '#'
	for num in list:
		nums.append(EMPTY * (height - num) + FILLED * num)
	row = ''
	for r in range(length-1):
		for c in nums:
			row += ' ' + c[r] * 2
		row += '\n'
	row = row[:-1]
	return row


def genlist(length):
	new_list = []
	for i in range(length[0], length[1]):
		new_list.append(i)
	random.shuffle(new_list)
	return new_list
	

def bubble(rlist):
	sorted = np.array(rlist.copy())
	length = len(sorted)
	height = max(sorted)
	delay = 0.01
	for i in range(length-1):
		for n in range(length-i-1):
			print('\n' * 60)
		
			arrows = ' ' + '   ' * n + r'/\ /'+'\\' + '   ' * (length - n)
			print(graph(sorted))
			#print(sorted)
			print(arrows)
			
			if sorted[n] > sorted[n+1]:
				sorted[n], sorted[n+1] = sorted[n+1], sorted[n]
			
			time.sleep(delay)
	return sorted
	

def shaker(rlist):
	sorted = np.array(rlist.copy())
	length = len(rlist)
	delay = 0.01
	
	for i in range(math.trunc((length-2)/2)):
		for n in range(i, length - i - 1):
			arrows = ' ' + '   ' * n + r'/\ /'+'\\' + '   ' * (length - n)
			print(graph(sorted))
			#print(sorted)
			print(arrows)
			time.sleep(delay)
			
			if sorted[n] > sorted[n+1]:
				sorted[n], sorted[n+1] = sorted[n+1], sorted[n]
		
		for n in range(-(i+1), -(length - i), -1):
			arrows = ' ' + '   ' * (length + n) + r'/\ /'+'\\' + '   ' * -n
			print(graph(sorted))
			#print(sorted)
			print(arrows)
			time.sleep(delay)
			
			if sorted[n] < sorted[n-1]:
				sorted[n], sorted[n-1] = sorted[n-1], sorted[n]
	
	return sorted
	
	
new_list = genlist((0, 20))
print(shaker(new_list))
