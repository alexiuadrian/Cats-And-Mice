"""
Dati enter dupa fiecare solutie afisata.

Presupunem ca avem costul de mutare al unui bloc egal cu indicele in alfabet, cu indicii incepănd de la 1 (care se calculează prin 1+ diferenta dintre valoarea codului ascii al literei blocului de mutat si codul ascii al literei "a" ) . Astfel A* are trebui sa prefere drumurile in care se muta intai blocurile cu infomatie mai mica lexicografic pentru a ajunge la una dintre starile scop
"""

import copy
import numpy as np

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
		nodDrum=self
		while nodDrum is not None:
			if(infoNodNou==nodDrum.info):
				return True
			nodDrum=nodDrum.parinte
		
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

		def parseFile(file_content):
			lines_of_content = file_content.split('\n')

			n = len(lines_of_content) - 1
			m = len(lines_of_content[1].split(' ')) - 1
			# Minimum number of mices that have to get out of the map
			self.no_of_sol = int(lines_of_content[0])
			matrix = np.chararray((n, m))

			# matrix = matrix.decode("utf-8")
			for line_index in range(1, n):
				elements = lines_of_content[line_index].split()
				print(elements)
				# for element_index in range(m):
				# 	matrix[line_index - 1][element_index] = elements[element_index]
			
			return matrix

		f = open(nume_fisier, 'r') 

		continutFisier = f.read()

		self.start = parseFile(continutFisier)
		# print("Stare Initiala: ", self.start)
		input()

	def testeaza_scop(self, nodCurent):
		return nodCurent.info in self.scopuri

	#va genera succesorii sub forma de noduri in arborele de parcurgere	


	def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
		listaSuccesori=[]
		stive_c=nodCurent.info # stivele din nodul curent
		nr_stive=len(stive_c)
		for idx in range(nr_stive):
			copie_interm=copy.deepcopy(stive_c)
			if len(copie_interm[idx])==0 :
				continue
			bloc=copie_interm[idx].pop()
			for j in range(nr_stive):
				if idx == j:
					continue
				stive_n=copy.deepcopy(copie_interm)#lista noua de stive
				stive_n[j].append(bloc)
				costMutareBloc=1+ord(bloc)-ord("a")
				nod_nou=NodParcurgere(stive_n,nodCurent, cost=nodCurent.g+costMutareBloc,h= self.calculeaza_h(stive_n, tip_euristica))
				if not nodCurent.contineInDrum(stive_n):
					listaSuccesori.append(nod_nou)

		return listaSuccesori


	# euristica banala
	def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
		if tip_euristica=="euristica banala":
			if infoNod not in self.scopuri:
				return 1
			return 0			
		else:
			#calculez cate blocuri nu sunt la locul fata de fiecare dintre starile scop, si apoi iau minimul dintre aceste valori
			euristici=[]
			for (iScop,scop) in enumerate(self.scopuri):
				h=0
				for iStiva, stiva in enumerate(infoNod):
						for iElem, elem in enumerate(stiva):
							try:
								#exista în stiva scop indicele iElem dar pe acea pozitie nu se afla blocul din infoNod
								if elem!=scop[iStiva][iElem]:
									h+=1
							except IndexError:
								#nici macar nu exista pozitia iElem in stiva cu indicele iStiva din scop
								h+=1
				euristici.append(h)
			return min(euristici)

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
		lSuccesori=gr.genereazaSuccesori(nodCurent,tip_euristica=tip_euristica)	
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

gr=Graph("input.txt")				

#Rezolvat cu breadth first
#print("Solutii obtinute cu breadth first:")
#breadth_first(gr, nrSolutiiCautate=3)

# print("\n\n##################\nSolutii obtinute cu A*:")
# print("\nObservatie: stivele sunt afisate pe orizontala, cu baza la stanga si varful la dreapta.")
# nrSolutiiCautate=3
# a_star(gr, nrSolutiiCautate=3,tip_euristica="euristica nebanala")


"""
a b c
d e
g


g e c
d a b
|

"""