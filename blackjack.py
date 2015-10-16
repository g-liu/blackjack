global __DBNAME__

import requests

BASE_URL = 'http://localhost:5000/'


playerId = None
gameId = None

def registerPlayer(name):
	global playerId
	global gameId

	response = requests.post(BASE_URL + 'player?name={}'.format(name)).json()
	playerId = response['playerId']
	gameId = response['game']['id']

def isMyTurn():
	return requests.get(BASE_URL + 'myTurn?playerId={}'.format(playerId)).json()['myTurn']

def setWager(wager):
	return requests.get(BASE_URL + 'setWager?playerId={}&wager={}'.format(playerId, wager)).json()

def getPlayers():
	return requests.get(BASE_URL + 'players').json()

def getPlayerInfo():
	global playerId
	return requests.get(BASE_URL + 'player/{}'.format(playerId)).json()

def getGames():
	return requests.get(BASE_URL + 'games').json()

def getGameInfo():
	global gameId
	return requests.get(BASE_URL + 'game/{}'.format(gameId)).json()

#################
# make the plays
#################

def hit():
	return requests.get(BASE_URL + 'hit?playerId={}'.format(playerId)).json()

def doubleDown():
	return requests.get(BASE_URL + 'doubleDown?playerId={}'.format(playerId)).json()

def stand():
	return requests.get(BASE_URL + 'stand?playerId={}'.format(playerId)).json()

def surrender():
	return requests.get(BASE_URL + 'surrender?playerId={}'.format(playerId)).json()
