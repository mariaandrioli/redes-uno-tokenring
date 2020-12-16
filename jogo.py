from collections import namedtuple
from termcolor import colored

def cartas(): # faz o baralho
	baralho = [
		'0 AM',
		'1 AM',
		'2 AM',
		'3 AM',
		'4 AM',
		'5 AM',
		'6 AM',
		'7 AM',
		'8 AM',
		'9 AM',
		'+ AM',
		'+ AM',
		'- AM',
		'- AM',
		'0 AZ',
		'1 AZ',
		'2 AZ',
		'3 AZ',
		'4 AZ',
		'5 AZ',
		'6 AZ',
		'7 AZ',
		'8 AZ',
		'9 AZ',
		'+ AZ',
		'+ AZ',
		'- AZ',
		'- AZ',
		'0 VD',
		'1 VD',
		'2 VD',
		'3 VD',
		'4 VD',
		'5 VD',
		'6 VD',
		'7 VD',
		'8 VD',
		'9 VD',
		'+ VD',
		'+ VD',
		'- VD',
		'- VD',
		'0 VM',
		'1 VM',
		'2 VM',
		'3 VM',
		'4 VM',
		'5 VM',
		'6 VM',
		'7 VM',
		'8 VM',
		'9 VM',
		'+ VM',
		'+ VM',
		'- VM',
		'- VM',
		'. CR',
		'. CR',
		'. CR',
		'. CR']
	return baralho

def imprimeCartas(lista): # imrpime lista de cartas com cor
	cont = 1
	for c in lista:
		if c[0:1] == '+':
			if c[2:4] == 'AM':
				print cont, ':', colored('+2 AMARELO', 'yellow')
			elif c[2:4] == 'AZ':
				print cont, ':', colored('+2 AZUL', 'blue')
			elif c[2:4] == 'VD':
				print cont, ':', colored('+2 VERDE', 'green')
			elif c[2:4] == 'VM':
				print cont, ':', colored('+2 VERMELHO', 'red')
		elif c[0:1] == '-':
			if c[2:4] == 'AM':
				print cont, ':', colored('PULAR AMARELO', 'yellow')
			elif c[2:4] == 'AZ':
				print cont, ':', colored('PULAR AZUL', 'blue')
			elif c[2:4] == 'VD':
				print cont, ':', colored('PULAR VERDE', 'green')
			elif c[2:4] == 'VM':
				print cont, ':', colored('PULAR VERMELHO', 'red')
		elif c[0:1] == '.':
			print cont, ':', colored("CORINGA", attrs=['bold'])
		else:
			if c[2:4] == 'AM':
				print cont, ':', colored(c[0:1] + ' AMARELO', 'yellow')
			elif c[2:4] == 'AZ':
				print cont, ':', colored(c[0:1] + ' AZUL', 'blue')
			elif c[2:4] == 'VD':
				print cont, ':', colored(c[0:1] + ' VERDE', 'green')
			elif c[2:4] == 'VM':
				print cont, ':', colored(c[0:1] + ' VERMELHO', 'red')
		cont += 1
	print

def imprimeCarta(c): # imprime unica carta com cor
	if c[0:1] == '+':
		if c[2:4] == 'AM':
			print colored('+2 AMARELO', 'yellow')
		elif c[2:4] == 'AZ':
			print colored('+2 AZUL', 'blue')
		elif c[2:4] == 'VD':
			print colored('+2 VERDE', 'green')
		elif c[2:4] == 'VM':
			print colored('+2 VERMELHO', 'red')
	elif c[0:1] == '-':
		if c[2:4] == 'AM':
			print colored('PULAR AMARELO', 'yellow')
		elif c[2:4] == 'AZ':
			print colored('PULAR AZUL', 'blue')
		elif c[2:4] == 'VD':
			print colored('PULAR VERDE', 'green')
		elif c[2:4] == 'VM':
			print colored('PULAR VERMELHO', 'red')
	elif c[0:1] == '.':
		print colored("CORINGA", attrs=['bold'])
	else:
		if c[2:4] == 'AM':
			print colored(c[0:1] + ' AMARELO', 'yellow')
		elif c[2:4] == 'AZ':
			print colored(c[0:1] + ' AZUL', 'blue')
		elif c[2:4] == 'VD':
			print colored(c[0:1] + ' VERDE', 'green')
		elif c[2:4] == 'VM':
			print colored(c[0:1] + ' VERMELHO', 'red')
	print

def telaInicio(): # mostra tela de inicio
	for i in range(6):
		print                                                        
	print colored('    UUUUUUUU     UUUUUUUU NNNNNNNN        NNNNNNNN      OOOOOOOOO       ', 'red')
	print colored('    U::::::U     U::::::U N:::::::N       N::::::N    OO:::::::::OO   ', 'red')
	print colored('    U::::::U     U::::::U N::::::::N      N::::::N  OO:::::::::::::OO ', 'red')
	print colored('    UU:::::U     U:::::UU N:::::::::N     N::::::N O:::::::OOO:::::::O', 'red')
	print colored('     U:::::U     U:::::U  N::::::::::N    N::::::N O::::::O   O::::::O', 'red')
	print colored('     U:::::D     D:::::U  N:::::::::::N   N::::::N O:::::O     O:::::O', 'red')
	print colored('     U:::::D     D:::::U  N:::::::N::::N  N::::::N O:::::O     O:::::O', 'red')
	print colored('     U:::::D     D:::::U  N::::::N N::::N N::::::N O:::::O     O:::::O', 'red')
	print colored('     U:::::D     D:::::U  N::::::N  N::::N:::::::N O:::::O     O:::::O', 'red')
	print colored('     U:::::D     D:::::U  N::::::N   N:::::::::::N O:::::O     O:::::O', 'red')
	print colored('     U:::::D     D:::::U  N::::::N    N::::::::::N O:::::O     O:::::O', 'red')
	print colored('     U::::::U   U::::::U  N::::::N     N:::::::::N O::::::O   O::::::O', 'red')
	print colored('     U:::::::UUU:::::::U  N::::::N      N::::::::N O:::::::OOO:::::::O', 'red')
	print colored('      UU:::::::::::::UU   N::::::N       N:::::::N  OO:::::::::::::OO ', 'red')
	print colored('        UU:::::::::UU     N::::::N        N::::::N    OO:::::::::OO   ', 'red')
	print colored('          UUUUUUUUU       NNNNNNNN         NNNNNNN      OOOOOOOOO     ', 'red')
	print
	raw_input(colored('\t\t\tAperte ENTER para comecar', attrs=['bold']))  