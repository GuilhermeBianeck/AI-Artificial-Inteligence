
import numpy as np
from web3 import Web3, HTTPProvider
import random

connection = Web3(HTTPProvider('https://mainnet.infura.io/v3/YOUR_TOKEN'))


def generate_matrix(size):
	matrix=np.zeros(size)
	return matrix

def verify_pos(matrix,pos):
	return matrix[pos]

def random_object(amount_object, object_type):
	return amount_object

def 


def main():

	out = 0

	size = int(input('Enter Matrix Size : '))
	print ('Size ', size)
	block = connection.eth.get_block('latest')
	seed = (int(block['hash'].hex(),16))
	seed = random.seed(seed)

	print(random.random())
	matrix = generate_matrix(size)

	n_ants = input('Number of Ants: ')

	#if n_ants < size ** 2:
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