# coding=utf-8
import socket, time, sys
import emoji, random, jogo

HOST = socket.gethostname()
euPort = int(sys.argv[1])
proximoPort = int(sys.argv[2])

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
	primeiro = bool(input("Primeiro a jogar? "))
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
					meuSock.sendto(baralho.pop(i), (HOST,proximoPort))

				mensagem = taComToken
				meuSock.sendto(mensagem, (HOST,proximoPort))
				primeiro = False
				ultima = baralho.pop(random.randint(0,27))
			
			try:
				dado, (end, port) = meuSock.recvfrom(65535)
			except socket.error, e:
				print "Error sending data: %s" % e
				sys.exit(1)

			donoToken = dado[0:4]
			if donoToken == str(euPort): # hora de quem ta com o token jogar
				print emoji.emojize('Sua vez de jogar! :smile:', use_aliases=True)
				print 'Ultima carta jogada:'
				jogo.imprimeCarta(ultima)
				print emoji.emojize('Suas cartas: :stuck_out_tongue_winking_eye:', use_aliases=True)
				jogo.imprimeCartas(deck)

				if ultima[0] == '+' and ultima[4:8] == str(euPort) and not comprouDuas: # quando a ultima for +2
						print emoji.emojize('Voce teve que comprar duas cartas :cry:, mas pode jogar :smile:', use_aliases=True)
						time.sleep(2)
						mensagem = 'K' + str(euPort)
						meuSock.sendto(mensagem, (HOST,proximoPort))
						comprouDuas = False
				elif ultima[0] == '-' and ultima[4:8] == str(euPort): # quando a ultima for pula vez
					print emoji.emojize('Sua vez foi pulada :sob:', use_aliases=True)
				 	temToken = False
				 	mensagem = tokenChegou
				 	meuSock.sendto(mensagem, (HOST,proximoPort))
				else: # se a ultima for diferente de +2 e de pula vez
					numCarta = int(input("Escolha qual carta quer jogar. Caso nao tenha carta para jogar, digite 0 \n")) - 1
					if numCarta == -1: # quando a pessoa quiser comprar
						mensagem = 'C' + str(euPort)
						meuSock.sendto(mensagem, (HOST,proximoPort))
					elif (numCarta >= len(deck) or numCarta < -1): # se a pessoa colocar um numero errado menor que 0 ou maior que a qtd do deck
						print 'Escolha uma carta no intervalo de 1 a', len(deck)
						time.sleep(3)
						mensagem = taComToken
						meuSock.sendto(mensagem, (HOST,proximoPort))
					else: # faz a jogada
						carta = str(deck[numCarta])
						if ultima[0] == '.' or ultima[2:4] == carta[2:4] or ultima[0] == carta[0] or carta[0] == '.':
							mensagem = 'jogou ' + deck[numCarta] + str(proximoPort)
							meuSock.sendto(mensagem, (HOST,proximoPort))
							deck.pop(numCarta)
							if len(deck) == 1: # só uma carta
								print emoji.emojize(':fire: :sunglasses: UNO! :sunglasses: :fire:', use_aliases=True)
						else:
							print emoji.emojize('Esta carta nao pode ser jogada :disappointed:, tente de novo', use_aliases=True)
							mensagem = taComToken
							meuSock.sendto(mensagem, (HOST,proximoPort))

			if dado[0:3] == 'UNO': # quando recebe a propria mensagem de uno
					temToken = False
				 	mensagem = tokenChegou + deck[numCarta-1]
				 	meuSock.sendto(mensagem, (HOST,proximoPort))

			if dado[0:5] == 'jogou':
				if dealer:
					baralho.append(ultima)
					random.shuffle(baralho)
				if len(deck) == 1: # manda msg de uno
					mensagem = 'UNO' + str(euPort)
					meuSock.sendto(mensagem, (HOST,proximoPort))
				elif len(deck) == 0: # quando o jogador vencer
					mensagem = 'venceu' + str(euPort)
					meuSock.sendto(mensagem, (HOST,proximoPort))
					temToken = False
					print str(euPort), emoji.emojize('VENCEU!!! :blush: :tada: :blush: :tada:', use_aliases=True)
					return
				else: # outras jogadas
				 	temToken = False
				 	mensagem = tokenChegou + deck[numCarta-1]
			 		meuSock.sendto(mensagem, (HOST,proximoPort))

			elif dado[0:1] == 'C' and dealer: # compra 1 carta
				mensagem = 'D' + str(baralho.pop(0))
				meuSock.sendto(mensagem, (HOST,proximoPort))

			elif dado[0:1] == 'K' and dealer: # compra 2 cartas
				for m in range(2):
					mensagem = 'D' + str(baralho.pop(0))
					meuSock.sendto(mensagem, (HOST,proximoPort))

			elif dado[0:1] == 'D': # recebe a compra
				if ultima[0] != '+' or comprouDuas: # testa quantas comprou
					deck.append(dado[1:5])
					mensagem = taComToken
					meuSock.sendto(mensagem, (HOST,proximoPort))
				else:
					deck.append(dado[1:5])
					mensagem = 'K' + str(euPort)
					meuSock.sendto(mensagem, (HOST,proximoPort))
					comprouDuas = True

		elif not temToken: # quando nao eh a maquina com token

			if not recebeu: # recebimento de cartas
				for j in range(7):
					dado, (end, port) = meuSock.recvfrom(65535)	
					deck.append(dado)
				print emoji.emojize('Suas cartas: :stuck_out_tongue_winking_eye:', use_aliases=True)
				jogo.imprimeCartas(deck)
				recebeu = True	

			dado, (end, port) = meuSock.recvfrom(65535)
			
			if dado[0:15] == tokenChegou: #quando chega o token
				temToken = True
				mensagem =  taComToken
				meuSock.sendto(mensagem, (HOST,proximoPort))
			elif dado[0:1] == 'C' and dealer: # se o dealer nao tiver o token
				mensagem = 'D' + str(baralho.pop(0))
				meuSock.sendto(mensagem, (HOST,proximoPort))
			elif dado[0:1] == 'K' and dealer:
				mensagem = 'D' + str(baralho.pop(0))
				meuSock.sendto(mensagem, (HOST,proximoPort))
			else: # outras mensagem que podem ser recebidas
				if dado[0:5] == 'jogou': # atualiza o topo da pilha de jogadas e recoloca no baralho
					ultima = dado[6:14]
					if dealer: 
						baralho.append(ultima)
						random.shuffle(baralho)	
				if dado[0:3] == 'UNO': # quando alguem diz uno
					print dado[3:7], emoji.emojize(' disse :fire: :sunglasses: UNO! :sunglasses: :fire:', use_aliases=True) 
				if dado[0:6] == 'venceu': #quando alguem venceu
					print dado[6:10], emoji.emojize('VENCEU!!! :blush: :tada: :blush: :tada:', use_aliases=True)
					meuSock.sendto(dado, (HOST, proximoPort))
					meuSock.close()
					return
				meuSock.sendto(dado, (HOST, proximoPort))
			

if __name__ == '__main__':
	main()
