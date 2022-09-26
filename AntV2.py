import numpy as np
import math 
from web3 import Web3, HTTPProvider
import logging
import random

connection = Web3(HTTPProvider('https://mainnet.infura.io/v3/a54ddb59e9a94434828abdca9fea3e21'))

logging.basicConfig(level=logging.INFO) #To Log Blocks


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
		self.pos = numpy.array([x, y])
		self.carrying = matrix.get_matrix()[x][y]
		self.matrix = matrix

	#def a_move(self, size, cons):
		step_size = random.randint(1, 9)
		# Adicionar algum vector (-1,+1) * step_size à localização das formigas
		self.pos += nrand.randint(-1 * step_size, 1 * step_size, 2)
		# Modificar a nova localização pelo tamanho da matriz para evitar o overflow
		self.pos = numpy.mod(self.pos, self.matrix.size)
		# Obter o objeto nesse local na matriz
		o = self.matrix.get_matrix()[self.pos[0]][self.pos[1]]
		# Se a celula estiver ocupada, mova-se novamente 
		if o is not None:
			# Se a formiga não estiver carregando um objeto
			if self.carrying is None:
				# Verificar se a formiga pega o objeto
				if self.o_take(size, cons) >= random.random():
					# Pegar o objeto e remover da matriz
					self.carrying = o
					self.matrix.get_matrix()[self.pos[0]][self.pos[1]] = None
					# Se não se mover
				else:
					self.a_move(size, cons)
			# Se carregando um objeto, basta mover-se
			else: 
				self.a_move(size, cons)		
		#Se a celula estiver vazia	
		else:
			if self.carrying is not None:
				# Verificar se a formiga solta o objeto
				if o_drop(size, cons) >= random.random:
					# Solte o objeto no local vazio
					self.matrix.get_matrix()[self.pos[0]][self.pos[1]] = self.carrying
					self.carrying = None

	def o_take(self, size, cons):
		ant = self.matrix.get_matrix()[self.pos[0]][self.pos[1]]
		return 1 - self.matrix.get_probability(ant, self.pos[0], self.pos[1], size, cons)

	#def o_drop(self, size, cons):
		ant = self.carrying
		return self.matrix.get_probability(ant, self.pos[0], self.pos[1], size, cons)



def populate_matrix(matrix, size, seed, ant, dead):
	aux = True
	aux2 = 0
	np.random.seed(seed)
	matrix = np.random.randint(low = 0, high = size**2, size = (size,size))
	while ant > 0:
		#print('ANT',ant)
		for j in range(size):
			for k in range(size):
			#print(j,'IN RANGE',size)
				if matrix[j][k]==aux2:
					if ant > 0:
						matrix[j][k]= -1
						ant -= 1
		aux2+= 1
		j=0
	aux2 = size**2
	while dead > 0:
		#print('DED',dead)
		for j in range(size):
			for k in range(size):
			#print(j,'IN RANGE',size)
				if matrix[j][k]==aux2:
					if dead > 0:
						matrix[j][k] = -2
						dead -= 1

		aux2-= 1
	j=0
	for j in range(size):
		for k in range(size):
			if matrix[j][k]>0:
				matrix[j][k]=0
	return matrix			

def generate_matrix(size):
	matrix=np.zeros((size,size))
	return matrix

def verify_pos(matrix,pos):
	return matrix[pos]

def main():

	out = 0
	block = connection.eth.get_block('latest')
	seed = int(block['hash'].hex(),16)
	seed = int(str(seed)[:9])
	new = Block()
	choice = -1


	size = int(input('Enter Matrix Size : '))
	n_ants = size**2+1
	n_dead = size**2+1
	matrix = generate_matrix(size)
	size_orig = size
	size = size**2

	while n_ants > size:
		n_ants = int(input('Number of Ants: '))
		if n_ants > size:
			print ('Type a lower Value - ')

	while n_dead > size:
		n_dead = int(input('Number of Bodies: ')) 
		if n_dead > size:
			print ('Type a Lower Value - ')

	choice = int(input ('0 - No Input / 1 - Last Block / 2 - Custom Block: '))


	if choice == 1 : 
		new=Block(block['number'], block['hash'].hex(), seed)
		print (seed)
	if choice == 2:
		choice = int(input ('Type Block Number: '))
		block = connection.eth.get_block(choice)
		seed = int(block['hash'].hex(),16)
		seed = int(str(seed)[:9])
		new = Block(block['number'], block['hash'].hex(), seed)

	
	matrix = populate_matrix(matrix, size_orig, seed, n_ants, n_dead)


	n_iteractions = int(input('Type Number of Iteractions: '))

	mov_ants(matrix, size_orig, n_ants)



	print(np.matrix(matrix))


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
