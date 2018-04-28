import requests
import sys
from bs4 import BeautifulSoup
headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page = "https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query="
pageEnd = "&x=0&y=0"


##################### Class Player Information ##############
class playerInformationObject:
	def __init__ (self, name, born, cityBorn, nationality, heigth, position, endContract):
		self.name = name
		self.born = born
		self.cityBorn = cityBorn
		self.nationality = nationality
		self.heigth = heigth
		self.position = position
		self.endContract = endContract

##################### Search Player ##########################
def searchPlayer(name):
	urlPage = page + name + pageEnd
	pageTree = requests.get(urlPage, headers=headers)
	pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

	players = pageSoup.find_all("a", {"class": "spielprofil_tooltip"})
	print "Fisrt Player: " + players[0].text
	print "Link Reference Player: " + players[0]['href']
	playerpage = "https://www.transfermarkt.com" + players[0]['href']
	return playerpage 

#################### Get Player Information ##################
def removeWriteSpaces(text):
	return text.encode('utf-8').replace("\n", "").replace("\t", "").replace("\r", "")

def getInformation(linkPlayer):
	pageTree = requests.get(linkPlayer, headers=headers)
	pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

	playerInformation = pageSoup.find_all("h1", {"itemprop": "name"})
	name =  removeWriteSpaces(playerInformation[0].text)

	playerInformation = pageSoup.find_all("span", {"class": "dataValue"})
	born =  removeWriteSpaces(playerInformation[0].text)
	cityBorn =  removeWriteSpaces(playerInformation[1].text)
	nationality =  removeWriteSpaces(playerInformation[2].text)
	heigth =  removeWriteSpaces(playerInformation[3].text)
	position =  removeWriteSpaces(playerInformation[4].text)
	endContract =  removeWriteSpaces(playerInformation[5].text)
	
	player =  playerInformationObject(name, born, cityBorn, nationality, heigth, position, endContract)
	print player.__dict__

############################## Main #########################
linkPlayer = searchPlayer(sys.argv[1])
getInformation(linkPlayer)
