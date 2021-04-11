'''
Documentatia se afla la link-ul de mai jos.

https://drive.google.com/drive/folders/19irNvx6XULiKS5X8TMK2zv2jzo6sklgo?usp=sharing
'''

# Pozitia (-10, -10) semnifica faptul ca un soarece a parasit tabla de joc
# Pozitia (-7, -7) semnifica faptul ca un soarece e ascuns
# Pozitia (-5, -5) semnifica faptul ca un soarece a fost mancat

import copy
import numpy as np
import math

# Functie ce va calcula distanta euclidiana dintre doua puncte
def compute_euclidian_distance(A_x, A_y, B_x, B_y):
	return math.sqrt((B_x - A_x) ** 2, (B_y - A_y) ** 2)

#informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
	def __init__(self, info, parinte, cost=0, h=0):
		self.info=info
		self.parinte=parinte #parintele din arborele de parcurgere
		self.g=cost #consider cost=1 pentru o mutare
		self.h=h
		self.f=self.g+self.h

	def obtineDrum(self):
		l=[self]
		nod=self
		while nod.parinte is not None:
			l.insert(0, nod.parinte)
			nod=nod.parinte
		return l
		
	def afisDrum(self, afisCost=False, afisLung=False): #returneaza si lungimea drumului
		l=self.obtineDrum()
		for nod in l:
			print(str(nod))
		if afisCost:
			print("Cost: ", self.g)
		if afisCost:
			print("Lungime: ", len(l))
		return len(l)


	def contineInDrum(self, infoNodNou):
		nodDrum = self
		while nodDrum is not None:
			areNotEqual = False
			for line_index in range(len(infoNodNou)):
				for column_index in range(len(infoNodNou[line_index])):
					if infoNodNou[line_index][column_index] != nodDrum.info[line_index][column_index]:
						areNotEqual = True
			
			if areNotEqual == False: # Va returna True daca sunt egale, asta inseamna ca areNotEqual va fi False
				return True

			nodDrum = nodDrum.parinte
		
		return False
		
	def __repr__(self):
		sir=""		
		sir+=str(self.info)
		return(sir)


	#euristica banală: daca nu e stare scop, returnez 1, altfel 0

	
	def __str__(self):
		sir=""
		maxInalt=max([len(stiva) for stiva in self.info])
		for inalt in range(maxInalt, 0, -1):
			for stiva in self.info:
				if len(stiva)< inalt:
					sir+="  "
				else:
					sir+=stiva[inalt-1]+" "
			sir+="\n"
		sir+="-"*(2*len(self.info)-1)
		return sir
	
	"""
	def __str__(self):
		sir=""
		for stiva in self.info:
			sir+=(str(stiva))+"\n"
		sir+="--------------\n"
		return sir
	"""
		

class Graph: #graful problemei
	def __init__(self, nume_fisier):
		self.no_of_sol = 0
		self.mice_positions = []
		self.mice_positions_hidden = []
		self.cats_positions = []
		self.n = 0
		self.m = 0

		def parseFile(file_content):
			lines_of_content = file_content.split('\n')

			n = len(lines_of_content) - 1
			m = len(lines_of_content[1].split(' ')) - 1
			self.n = n
			self.m = m
			# Minimum number of mices that have to get out of the map
			self.no_of_sol = int(lines_of_content[0])
			elements_list = []
			aux_list = []

			no_of_mice = 0
			no_of_cats = 0
			no_of_mice_hidden = 0

			for line_index in range(1, n + 1):
				elements = lines_of_content[line_index].split()
				elements_list.append(elements)
				for element in elements:
					aux_list.append(element)
					if 's' in element:
						no_of_mice += 1
					elif 'S' in element:
						no_of_mice_hidden += 1
					elif 'p' in element:
						no_of_cats += 1

			for index in range(no_of_mice):
				for line_index in range(n):
					for column_index in range(len(elements_list[line_index])):
						if elements_list[line_index][column_index] == ('s' + str(index)):
							self.mice_positions.append((line_index, column_index))
							self.mice_positions_hidden.append((-7, -7))
						elif elements_list[line_index][column_index] == ('S' + str(index)):
							self.mice_positions.append((-7, -7))
							self.mice_positions_hidden.append((line_index, column_index))
				
			for index in range(no_of_cats):
				for line_index in range(n):
					for column_index in range(len(elements_list[0])):
						if elements_list[line_index][column_index] == ('p' + str(index)):
							self.cats_positions.append((line_index, column_index))

			return elements_list, aux_list

		f = open(nume_fisier, 'r') 

		continutFisier = f.read()
		aux_list = []

		self.start, aux_list = parseFile(continutFisier)

		print("Stare Initiala: ", self.start)
		# input()

	# Scop este in momentul in care 3 soricei au iesit de pe harta sau nu mai sunt soricei
	def testeaza_scop(self, nodCurent):
		no_of_mice_out = 0

		for position in self.mice_positions:
			if position[0] == -10 and position[1] == -10:
				no_of_mice_out += 1

		if no_of_mice_out == self.no_of_sol:
			return True
		
		return False

	# Va muta toti soarecii din stare (care pot fi mutati) si va face o lista cu toate configuratiile posibile
	def move_mice(self, stare, n, m):
		possible_moves = []
		aux_stare = copy.deepcopy(stare)

		for position_x, position_y in self.mice_positions:
			for mouse_index in range(len(self.mice_positions)):
				if self.mice_positions[mouse_index] != (-10, -10):
					if self.mice_positions[mouse_index] != (-7, -7):
						positions = [(position_x - 1, position_y), (position_x, position_y + 1), (position_x + 1, position_y), (position_x, position_y - 1)]

						for position in positions:
							if position[0] in range(0, n) and position[1] in range(0, m):
								if position not in self.cats_positions and position not in self.mice_positions_hidden and stare[position[0]][position[1]] not in ['#', 'E', '@']:
									aux = aux_stare[position[0]][position[1]]
									aux_stare[position[0]][position[1]] = "s" + str(mouse_index)
									aux_stare[position_x][position_y] = aux
									self.mice_positions[mouse_index] = position
								elif stare[position[0]][position[1]] == 'E':
									self.mice_positions[mouse_index] = (-10, -10)
									self.mice_positions_hidden[mouse_index] = (-10, -10)
								elif stare[position[0]][position[1]] == '@':
									aux_stare[position[0]][position[1]] = "S" + str(mouse_index)
									self.mice_positions_hidden[mouse_index] = position
									self.mice_positions[mouse_index] = (-7, -7)
					else:
						positions = [(position_x - 1, position_y), (position_x, position_y + 1), (position_x + 1, position_y), (position_x, position_y - 1)]

						for position in positions:
							if position[0] in range(0, n) and position[1] in range(0, m):
								if position not in self.cats_positions and position not in self.mice_positions and stare[position[0]][position[1]] not in ['#', 'E', '@']:
									aux = aux_stare[position[0]][position[1]]
									aux_stare[position[0]][position[1]] = "s" + str(mouse_index)
									aux_stare[position_x][position_y] = aux
									self.mice_positions[mouse_index] = position
									self.mice_positions_hidden[mouse_index] = (-7, -7)
								elif stare[position[0]][position[1]] == 'E':
									self.mice_positions_hidden[mouse_index] = (-10, -10)
									self.mice_positions[mouse_index] = (-10, -10)

				possible_moves.append(aux_stare)

		return possible_moves

	# Va muta toate pisicile din stare (care pot fi mutate) si va face o lista cu toate configuratiile posibile
	# Functia se va apela DUPA mutarea soarecilor
	def move_cats(self, stare, n, m):
		possible_moves = []
		aux_stare = copy.deepcopy(stare)
		print(m)
		for cat_index in range(len(self.cats_positions)):
			for position_x, position_y in self.cats_positions:
				positions = [(position_x - 1, position_y), (position_x - 1, position_y + 1), (position_x, position_y + 1), (position_x + 1, position_y + 1), (position_x + 1, position_y), (position_x + 1, position_y - 1), (position_x, position_y - 1), (position_x - 1, position_y - 1)]

				for position in positions:
					if position[0] in range(n) and position[1] in range(m):
						print(position[0], position[1])
						if position not in self.cats_positions and position not in self.mice_positions_hidden and stare[position[0]][position[1]] not in ['#', 'E', '@']:
							if position in self.mice_positions:
								for mouse_index in range(len(self.mice_positions)):
									if self.mice_positions[mouse_index][0] == position[0] and self.mice_positions[mouse_index][1] == position[1]:
										self.mice_positions[mouse_index] = (-5, -5)
										self.mice_positions_hidden[mouse_index] = (-5, -5)
										aux_stare[position[0]][position[1]] = "p" + str(cat_index)
							else:
								aux = aux_stare[position[0]][position[1]]
								aux_stare[position[0]][position[1]] = "p" + str(cat_index)
								aux_stare[position_x][position_y] = aux
								self.cats_positions[cat_index] = position

				possible_moves.append(aux_stare)

		return possible_moves

	# va genera succesorii sub forma de noduri in arborele de parcurgere	
	def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
		listaSuccesori = []
		conf_curenta = nodCurent.info

		result_after_mice = self.move_mice(conf_curenta, self.n, len(conf_curenta[0]))

		for configuration_mice in result_after_mice:
			result_after_cats = self.move_cats(configuration_mice, self.n, len(conf_curenta[0]))

			for configuration_cats in result_after_cats:
				costMove = nodCurent.g + 1
				new_node = NodParcurgere(configuration_cats, nodCurent, cost=costMove, h=0)

				if not nodCurent.contineInDrum(configuration_cats):
					listaSuccesori.append(new_node)
				
		print(listaSuccesori)
		input()

		return listaSuccesori


	# euristica banala
	def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
		if tip_euristica=="euristica banala":
			return 0		

	def __repr__(self):
		sir=""
		for (k,v) in self.__dict__.items() :
			sir+="{} = {}\n".format(k,v)
		return(sir)
		
		
def breadth_first(gr, nrSolutiiCautate):

	#in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
	c=[NodParcurgere(gr.start, None)]
	
	while len(c)>0:
		#print("Coada actuala: " + str(c))
		#input()
		nodCurent=c.pop(0)

		if gr.testeaza_scop(nodCurent):
			print("Solutie:")
			nodCurent.afisDrum(afisCost=True, afisLung=True)
			print("\n----------------\n")
			input()
			nrSolutiiCautate-=1
			if nrSolutiiCautate==0:
				return
		lSuccesori=gr.genereazaSuccesori(nodCurent)	
		c.extend(lSuccesori)

def a_star(gr, nrSolutiiCautate, tip_euristica):
	#in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
	c=[NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
	
	while len(c)>0:
		nodCurent=c.pop(0)
		
		if gr.testeaza_scop(nodCurent):
			print("Solutie: ")
			nodCurent.afisDrum(afisCost=True, afisLung=True)
			print("\n----------------\n")
			input()
			nrSolutiiCautate-=1
			if nrSolutiiCautate==0:
				return
		lSuccesori = gr.genereazaSuccesori(nodCurent,tip_euristica=tip_euristica)	
		for s in lSuccesori:
			i=0
			gasit_loc=False
			for i in range(len(c)):
				#diferenta fata de UCS e ca ordonez dupa f
				if c[i].f>=s.f :
					gasit_loc=True
					break
			if gasit_loc:
				c.insert(i,s)
			else:
				c.append(s)

import sys
import os
import time

input_folder = None
output_folder = None
NSOL = None

try:
    input_folder = sys.argv[1]
except:
    print("Va rog sa dati folderul cu fisierele de intrare")

try:
    output_folder = sys.argv[2]
except:
    print("Va rog sa dati folderul cu fisierele de iesire")

try:
    NSOL = int(sys.argv[3])
except:
    print("Va rog sa dati numarul de solutii si sa fie intreg")
    sys.exit(0)

try:
    timeout_time = int(sys.argv[4])
except:
    print("Va rog sa dati timpul de timeout si sa fie intreg")
    sys.exit(0)

def import_files(folder):
    names = []

    for file in os.listdir(folder):
        if file.endswith(".txt"):
            names.append(file)

    return names

def write_to_file(folder, filename, content):
    file = open(folder + '/' + filename, "w")
    file.write(content)

# Start of timer
timer_start = time.perf_counter()

names = import_files(input_folder)

for file_name in names:
	gr = Graph(f'{input_folder}/{file_name}')
	print("\n\n##################\nSolutii obtinute cu A*:")
	a_star(gr, nrSolutiiCautate=int(NSOL), tip_euristica="euristica banala")


# End of timer
timer_end = time.perf_counter()
print(f"Time elapsed: {timer_end - timer_start} seconds")