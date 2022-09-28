from re import S
from turtle import width
import numpy as np
import numpy.random as nrand
import math 
from web3 import Web3, HTTPProvider
import logging
import random
import matplotlib.pylab as plt
from pprint import pprint

connection = Web3(HTTPProvider('https://mainnet.infura.io/v3/a54ddb59e9a94434828abdca9fea3e21'))

view = 1
freq = 500



logging.basicConfig(level=logging.INFO) #To Log Block


class LoggedAccess:

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        value = getattr(obj, self.private_name)
        logging.info('Accessing %r giving %r', self.public_name, value)
        return value

    def __set__(self, obj, value):
        logging.info('Updating %r to %r', self.public_name, value)
        setattr(obj, self.private_name, value)


class Block:
	number = LoggedAccess()
	hash_code = LoggedAccess()

	def __init__(self, number=None, hash_code=None, seed=None):

		if number == None : number = 0	
		self.number = number

		if hash_code == None : hash_code = 0
		self.hash_code = hash_code

		if seed == None : seed = 0
		self.seed = seed


class Ant:
	def __init__(self, x, y, matrix):
		self.pos = np.array([x, y])
		self.carrying = matrix.get_matrix()[x][y]
		self.matrix = matrix

	def a_move(self, view, cons):
		step_size = random.randint(1, 9)
		# Adicionar algum vector (-1,+1) * step_size à localização das formigas
		self.pos += nrand.randint(-1 * step_size, 1 * step_size, 2)
		# Modificar a nova localização pelo tamanho da matriz para evitar o overflow
		self.pos = np.mod(self.pos, self.matrix.dim)
		# Obter o objeto nesse local na matriz
		o = self.matrix.get_matrix()[self.pos[0]][self.pos[1]]
		# Se a celula estiver ocupada, mova-se novamente 
		if o is not None:
			# Se a formiga não estiver carregando um objeto
			if self.carrying is None:
				# Verificar se a formiga pega o objeto
				if self.o_take(view, cons) >= random.random():
					# Pegar o objeto e remover da matriz
					self.carrying = o
					self.matrix.get_matrix()[self.pos[0]][self.pos[1]] = None
					# Se não se mover
				else:
					self.a_move(view, cons)
			# Se carregando um objeto, basta mover-se
			else: 
				self.a_move(view, cons)		
		#Se a celula estiver vazia	
		else:
			if self.carrying is not None:
				# Verificar se a formiga solta o objeto
				if self.o_drop(view, cons) >= random.random:
					# Solte o objeto no local vazio
					self.matrix.get_matrix()[self.pos[0]][self.pos[1]] = self.carrying
					self.carrying = None

	def o_take(self, view, cons):
		ant = self.matrix.get_matrix()[self.pos[0]][self.pos[1]]
		return 1 - self.matrix.get_probability(ant, self.pos[0], self.pos[1], view, cons)

	def o_drop(self, view, cons):
		ant = self.carrying
		return self.matrix.get_probability(ant, self.pos[0], self.pos[1], view, cons)


class Matrix:
	def __init__(self, height, width , file):
		self.path = file
		self.dim = np.array([height, width])
		self.matrix = np.zeros([height,width])
		#print (self.matrix)

		plt.ion() #Plot Matrix
		plt.figure(figsize=(20, 20))		

	def populate_matrix(self, height, width, seed, ant, dead, ants_agents):
		aux = True
		aux2 = 0
		np.random.seed(seed)
		self.matrix = np.random.randint(low = 0, high = height*width, size = (height,width))
		while ant > 0:
			for j in range(height):
				for k in range(width):
					if self.matrix[j][k]==aux2:
						if ant > 0:
							self.matrix[j][k]= -1
							#print(self.matrix)
							ants = Ant(j,k, self)
							ants_agents.append(ants)

							ant -= 1
				aux2+= 1
			j=0
		aux2 = height*width
		
		while dead > 0:
			#print('DED',dead)
			for j in range(height):
				for k in range(width):
				#print(j,'IN RANGE',size)
					if self.matrix[j][k]==aux2:
						if dead > 0:
							self.matrix[j][k] = -2
							dead -= 1

				aux2-= 1
		pprint(ants_agents)
		j=0
		for j in range(height):
			for k in range(width):
				if self.matrix[j][k]>0:
					self.matrix[j][k]=0
		print (self.matrix)
		return self.matrix
		
	def plot_matrix(self, name="", save_figure=True):
		plt.matshow(self.matrix, cmap="RdBu", fignum=0)
		if save_figure:
			plt.savefig(self.path + name + '.png')
        # plt.draw()
	
	def get_matrix(self):		
		return self.matrix

	def get_chances(self, d, y , x, view, cons):
		y_s = y-n
		x_s = x-n
		total = 0.0
		# for i in range( vizinhos
		for i in range((n*2)+1):
			## Se estamos olhando para um vizinho
			if j != x and i != y:
				yj = (y_s+j)% self.dim[1]
				#pega o vizinho o
				o = self.matrix[xi][yj]
				# verifica a similaridade entre x e o 
				if o is not None:
					s = d.similarity(o)
					total += s
		#normaliza a densidade parapara a visão maxima dos dados 
		md= total/(math.pow((n*2)+1, 2)-1)
		if md > self.max_d:
			self.max_d = md
		density = total / (self.max_d*(math.pow((n*2)+1,2)-1))
		density = max(min(density, 1), 0 )
		t = math.exp(-c*density)
		probability = (1-t)/ (1+t)
		return probability

		
def runs(height, width, ant, dead, number, constant, file = "image"):
	pass
	
def main():

	out = 0
	choice = 0 #-1 
	seed=0

	#height = int(input('Enter Matrix height : '))
	height = 20
	#width = int(input('Enter Matrix width : '))
	width = 20

	n_ants = (height*width)+1
	n_dead = (height*width)+1
	#matrix = generate_matrix(size)
	max_size = height*width

	while n_ants > max_size:
		#n_ants = int(input('Number of Ants: '))
		n_ants = 20
		if n_ants > max_size:
			print ('Type a lower Value - ')

	while n_dead > max_size-n_ants:
		#n_dead = int(input('Number of Bodies: ')) 
		n_dead = 20
		if n_dead > max_size-n_ants:
			print ('Type a Lower Value - ')

	#choice = int(input ('0 - No Input / 1 - Last Block / 2 - Custom Block: '))

	matrix = Matrix(height, width , "image")
	#print (matrix.matrix)

	if choice == 1 : 
		block = connection.eth.get_block('latest')
		seed = int(block['hash'].hex(),16)
		seed = int(str(seed)[:9])

		new = Block(block['number'], block['hash'].hex(), seed)
		print (seed)

	if choice == 2:
		choice = int(input ('Type Block Number: '))
		block = connection.eth.get_block(choice)
		seed = int(block['hash'].hex(),16)
		seed = int(str(seed)[:9])

		new = Block(block['number'], block['hash'].hex(), seed)

	
	ants_agents=[]
	matrix.populate_matrix(height, width, seed, n_ants, n_dead, ants_agents)
	#matrix.plot_matrix("file")
	for i in range(n_dead):
		for ant in ants_agents:
			ant.a_move(view, view)
		if i % freq == 0:
			print(i)
			s = "img" + str(i).zfill(6)
			matrix.plot_matrix(s)



	#matrix = Matrix(height, width , "image")

	
	#matrix = populate_matrix(matrix, size_orig, seed, n_ants, n_dead)

	#n_iteractions = int(input('Type Number of Iteractions: '))

	#a_move(matrix, size_orig, n_ants)


	#5print(np.matrix(new.matrix))


if __name__ == '__main__':
    main()


#NOTES
#INSTANCIAR FORMIGAS e METER MATRIX TOGETHER

'''
Montar Sistema para Simular Agrupamento de Itens:
Definir uma Matriz (Tamanho)
Definir Quantidade de Formigas 
Verificar se é inferior ao tamanho da matriz
Definir Quantidade de Objetos
Verificar se é inferior ao Tamanho da matriz - Quantidade de Formigas
Botar Formigas na Matriz (Estados)
Verificar se Campo não esta ocupado
Botar Objetos na Matriz (Estados)
Verificar se Campo não esta ocupado
Critério de Parada
'''
