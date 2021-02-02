# coding=utf-8
import socket, time, sys
import random, jogo

HOST = socket.gethostname()
euPort = int(sys.argv[1])
proximoIP = sys.argv[2]
proximoPort = int(sys.argv[3])

def main():
	meuSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #cria socket 
	meuSock.bind((HOST,euPort))

	jogo.telaInicio() # mostra tela de inicio

	# criacao de variaveis
	deck = []
	dealer = False
	recebeu = False
	dado = None
	comprouDuas = False
	taComToken = str(euPort) + ' esta com o token'
	primeiro = bool(input("Primeiro a jogar? 0/1\n"))
	temToken = primeiro
	tokenChegou = 'o token chegou '


	while 1:
		if temToken:
			if primeiro:	# primeira jogada	
				dealer = True
				baralho = jogo.cartas()
				random.shuffle(baralho)

				# distribui cartas
				for i in range(7):
					deck.append(baralho.pop(i))
				recebeu = True

				for i in range(21):
					meuSock.sendto(baralho.pop(i), (proximoIP,proximoPort))

				mensagem = taComToken
				meuSock.sendto(mensagem, (proximoIP,proximoPort))
				primeiro = False
				ultima = baralho.pop(random.randint(0,27))
			
			dado, (end, port) = meuSock.recvfrom(65535)

			donoToken = dado[0:4]
			if donoToken == str(euPort): # hora de quem ta com o token jogar
				print 'Sua vez de jogar!'
				print 'Ultima carta jogada:'
				jogo.imprimeCarta(ultima)
				print 'Suas cartas:'
				jogo.imprimeCartas(deck)

				if ultima[0] == '+' and ultima[4:8] == str(euPort) and not comprouDuas: # quando a ultima for +2
						print 'Voce teve que comprar duas cartas, mas pode jogar'
						time.sleep(2)
						mensagem = 'K' + str(euPort)
						meuSock.sendto(mensagem, (proximoIP,proximoPort))
						comprouDuas = False
				elif ultima[0] == '-' and ultima[4:8] == str(euPort): # quando a ultima for pula vez
					print 'Sua vez foi pulada'
				 	temToken = False
				 	mensagem = tokenChegou
				 	meuSock.sendto(mensagem, (proximoIP,proximoPort))
				else: # se a ultima for diferente de +2 e de pula vez
					numCarta = int(input("Escolha qual carta quer jogar. Caso nao tenha carta para jogar, digite 0 \n")) - 1
					if numCarta == -1: # quando a pessoa quiser comprar
						mensagem = 'C' + str(euPort)
						meuSock.sendto(mensagem, (proximoIP,proximoPort))
					elif (numCarta >= len(deck) or numCarta < -1): # se a pessoa colocar um numero errado menor que 0 ou maior que a qtd do deck
						print 'Escolha uma carta no intervalo de 1 a', len(deck)
						time.sleep(3)
						mensagem = taComToken
						meuSock.sendto(mensagem, (proximoIP,proximoPort))
					else: # faz a jogada
						carta = str(deck[numCarta])
						if ultima[0] == '.' or ultima[2:4] == carta[2:4] or ultima[0] == carta[0] or carta[0] == '.':
							mensagem = 'jogou ' + deck[numCarta] + str(proximoPort)
							meuSock.sendto(mensagem, (proximoIP,proximoPort))
							deck.pop(numCarta)
							if len(deck) == 1: # só uma carta
								print 'UNO!'
						else:
							print 'Esta carta nao pode ser jogada, tente de novo'
							mensagem = taComToken
							meuSock.sendto(mensagem, (proximoIP,proximoPort))

			if dado[0:3] == 'UNO': # quando recebe a propria mensagem de uno
					temToken = False
				 	mensagem = tokenChegou + deck[numCarta-1]
				 	meuSock.sendto(mensagem, (proximoIP,proximoPort))

			if dado[0:5] == 'jogou':
				if dealer:
					baralho.append(ultima)
					random.shuffle(baralho)
				if len(deck) == 1: # manda msg de uno
					mensagem = 'UNO' + str(euPort)
					meuSock.sendto(mensagem, (proximoIP,proximoPort))
				elif len(deck) == 0: # quando o jogador vencer
					mensagem = 'venceu' + str(euPort)
					meuSock.sendto(mensagem, (proximoIP,proximoPort))
					temToken = False
					print str(euPort), 'VENCEU!!!'
					return
				else: # outras jogadas
				 	temToken = False
				 	mensagem = tokenChegou + deck[numCarta-1]
			 		meuSock.sendto(mensagem, (proximoIP,proximoPort))

			elif dado[0:1] == 'C' and dealer: # compra 1 carta
				mensagem = 'D' + str(baralho.pop(0))
				meuSock.sendto(mensagem, (proximoIP,proximoPort))

			elif dado[0:1] == 'K' and dealer: # compra 2 cartas
				for m in range(2):
					mensagem = 'D' + str(baralho.pop(0))
					meuSock.sendto(mensagem, (proximoIP,proximoPort))

			elif dado[0:1] == 'D': # recebe a compra
				if ultima[0] != '+' or comprouDuas: # testa quantas comprou
					deck.append(dado[1:5])
					mensagem = taComToken
					meuSock.sendto(mensagem, (proximoIP,proximoPort))
				else:
					deck.append(dado[1:5])
					mensagem = 'K' + str(euPort)
					meuSock.sendto(mensagem, (proximoIP,proximoPort))
					comprouDuas = True

		elif not temToken: # quando nao eh a maquina com token
			comprouDuas = False
			if not recebeu: # recebimento de cartas
				for j in range(7):
					dado, (end, port) = meuSock.recvfrom(65535)	
					deck.append(dado)
				print 'Suas cartas:'
				jogo.imprimeCartas(deck)
				recebeu = True	

			dado, (end, port) = meuSock.recvfrom(65535)
			
			if dado[0:15] == tokenChegou: #quando chega o token
				temToken = True
				mensagem =  taComToken
				meuSock.sendto(mensagem, (proximoIP,proximoPort))
			elif dado[0:1] == 'C' and dealer: # se o dealer nao tiver o token
				mensagem = 'D' + str(baralho.pop(0))
				meuSock.sendto(mensagem, (proximoIP,proximoPort))
			elif dado[0:1] == 'K' and dealer:
				mensagem = 'D' + str(baralho.pop(0))
				meuSock.sendto(mensagem, (proximoIP,proximoPort))
			else: # outras mensagem que podem ser recebidas
				if dado[0:5] == 'jogou': # atualiza o topo da pilha de jogadas e recoloca no baralho
					ultima = dado[6:14]
					if dealer: 
						baralho.append(ultima)
						random.shuffle(baralho)	
				if dado[0:3] == 'UNO': # quando alguem diz uno
					print dado[3:7], ' disse UNO!' 
				if dado[0:6] == 'venceu': #quando alguem venceu
					print dado[6:10], 'VENCEU!!!'
					meuSock.sendto(dado, (proximoIP, proximoPort))
					meuSock.close()
					return
				meuSock.sendto(dado, (proximoIP, proximoPort))
			

if __name__ == '__main__':
	main()