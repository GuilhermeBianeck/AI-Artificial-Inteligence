
import numpy as np
import math 
from web3 import Web3, HTTPProvider
import logging
import random

connection = Web3(HTTPProvider('https://mainnet.infura.io/v3/YOUR_KEY'))

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

	#def set_number(self, number):
	#def set_hash(self, hash_code):


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

def random_object(amount_object, object_type):
	return amount_object

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


	if choice == 1 : new=Block(block['number'], block['hash'].hex(), seed)
	if choice == 2:
		choice = int(input ('Type Block Number: '))
		block = connection.eth.get_block(choice)
		seed = int(block['hash'].hex(),16)
		seed = int(str(seed)[:9])
		new = Block(block['number'], block['hash'].hex(), seed)

	print (seed)
	matrix = populate_matrix(matrix, size_orig, seed, n_ants, n_dead)



	print(np.matrix(matrix))


	#if n_ants < size * 2:
	#	out = 1

	#while (out==0)

	#	print ('Too Much Ants, Try a lower Amount')



	#n_dead =

	#Gerar 

if __name__ == '__main__':
    main()


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

Verificar se Campo não esta ocupado'''



