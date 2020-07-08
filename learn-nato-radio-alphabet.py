#!/usr/bin/python
# -+- coding: utf-8 -+-

import random

words = {'a':("Alfa", "Alpha"), 'b':"Bravo", 'c':("Charlie", "Charly"), 'd':"Delta", 'e':"Echo", 'f':("Foxtrot", "Fox-trot", "Fox"), 'g':"Golf", 'h':"Hotel", 'i':"India",
         'j':("Juliett", "Juliet"), 'k':"Kilo", 'l':"Lima", 'm':"Mike", 'n':"November", 'o':"Oscar", 'p':"Papa", 'q':"Quebec", 'r':"Romeo",
         's':"Sierra", 't':"Tango", 'u':"Uniform", 'v':"Victor", 'w':("Whiskey", "Whisky"), 'x':"Xray", 'y':"Yankee", 'z':("Zulu", "Zoulou")}

randomletters = []
for i in range(4):
	while True:
		x = "%c" % (96+random.randint(1, len(words)))
		if not x in randomletters:
			break
	randomletters.append(x)

# ~ randomletters = ['a', 'b', 'c', 'z']

err = 1
while err:
	while True:
		print("Please type: "+("".join(randomletters).upper()))
		answers = raw_input("> ").replace(',', ' ').split()
		#answers = ['alpha', "Braxvo", "Charlie", "zoulou"]
		if len(answers) != len(randomletters):
			continue
		break

	err = 0
	for i in range(len(randomletters)):
		a = answers[i]
		s = words[randomletters[i]]
		if type(words[randomletters[i]]) is str:
			s = [s]

		ok = 0
		for w in s:
			if a.lower() == w.lower():
				#print(w+": OK!")
				ok = 1
				break
		if not ok:
			err+=1
			print(randomletters[i].upper()+": "+a+ " is incorrect.")

	if err > 0:
		print("do it again!")
	else:
		print("Good job!")
