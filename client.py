import requests
import blackjack
import time
import random

BASE_URL = 'http://localhost:5000/'

resp = blackjack.registerPlayer('geoff')

# local only...
requests.get(BASE_URL + 'start')


# state variables
wager = -1
def getInitialDeck():
	return [[1,1,1,1],[2,2,2,2],[3,3,3,3],[4,4,4,4],[5,5,5,5],[6,6,6,6],[7,7,7,7],[8,8,8,8],[9,9,9,9],[10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]]

deck = getInitialDeck()

def doTurn():
	global wager
	global deck

	playerState = blackjack.getPlayerInfo()
	gameState = blackjack.getGameInfo()

	

	if wager < 0:
		wager = max(5, playerState['chips'] / 5)

		blackjack.setWager(wager)
		print "have {} chips, set wager for {} dollars".format(playerState['chips'], wager)
		return  # wait for all other players

	# check what your hand is
	pointValue = playerState['hand']['value']

	# check dealer
	dealerCard = gameState['dealerUpCard']['value']

	# update the deck
	deckSize = 52
	for card in gameState['revealedCards']:
		deck[card['value'] - 1].pop()
		deckSize = deckSize - 1

	# update probabilities
	probabilities = {}
	for i in range(1, 10 + 1):
		probabilities[i] = float(len(deck[i - 1])) / deckSize

	print probabilities

	print "dealt {}".format(pointValue)

	# Consider doubling down on these scenarios:
	# if pointValue == 11 or pointValue == 10 and 4 <= gameState['dealerUpCard']['value'] <= 6 or pointValue == 9 and 5 <= gameState['dealerUpCard']['value'] <= 6:
	# 	cardValue = blackjack.doubleDown()['value']
	# 	pointValue = pointValue + cardValue

	# 	print "hard double down; receive {}; total {}".format(cardValue, pointValue)

	# 	blackjack.stand()
	# 	wager = -1
	# 	deck = getInitialDeck()
	# 	print "stand"
	# 	return

	if not playerState['hand']['soft']:
		if pointValue == 9 and 2 <= dealerCard and dealerCard <= 6 \
		or pointValue == 10 and 2 <= dealerCard and dealerCard <= 9 \
		or pointValue == 11:
			cardValue = blackjack.doubleDown()['value']
			pointValue = pointValue + cardValue

			print "hard double down; receive {}; total {}".format(cardValue, pointValue)

			blackjack.stand()
			wager = -1
			deck = getInitialDeck()
			print "stand"
			return
	else:
		if 13 <= pointValue <= 18 and 4 <= dealerCard and dealerCard <= 6:
			cardValue = blackjack.doubleDown()['value']
			pointValue = pointValue + cardValue

			print "hard double down; receive {}; total {}".format(cardValue, pointValue)

			blackjack.stand()
			wager = -1
			deck = getInitialDeck()
			print "stand"
			return

	# you gotta know when to stand
	if not playerState['hand']['soft']:
		if 12 <= pointValue and 2 <= dealerCard <= 6:
			blackjack.stand()
			wager = -1
			deck = getInitialDeck()
	else:
		if 18 <= pointValue:
			blackjack.stand()
			wager = -1
			deck = getInitialDeck()

	# hit me
	while pointValue <= 16 and random.random() < (21 - pointValue) / 10:
		cardValue = blackjack.hit()['value']
		pointValue = pointValue + cardValue
		print "hit; receive {}; total {}".format(cardValue, pointValue)

	blackjack.stand()  # end our turn
	wager = -1  # reset wager
	deck = getInitialDeck()

	if pointValue <= 21:
		print "stand at {}".format(pointValue)
	else:
		print "BROKE!!!!"


# the main code
while True:
	myTurn = blackjack.isMyTurn()
	print "\n"
	if myTurn:
		doTurn()
	time.sleep(1)
