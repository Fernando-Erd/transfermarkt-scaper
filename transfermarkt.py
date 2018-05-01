import requests
import sys
from bs4 import BeautifulSoup
headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page = "https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query="
pageEnd = "&x=0&y=0"


class SimpleClass(object):
  pass

##################### Class Player Information ##############
class playerInformationObject:
	def __init__ (self, name, born, cityBorn, nationality, heigth, position, endContract, transfer):
		self.name = name
		self.born = born
		self.cityBorn = cityBorn
		self.nationality = nationality
		self.heigth = heigth
		self.position = position
		self.endContract = endContract
		self.transfer = transfer

	def __str__(self):
		print "Name: " + self.name
		print "Born: " + self.born
		print "City Born: " + self.cityBorn
		print "Nationality: " + self.nationality
		print "Heigth: " + self.heigth
		print "Position: " + self.position
		print "End of Contract: " + self.endContract
		print "------- Tranfers ----------"
		for i in self.transfer:
			print "Season: " + i.seasonTransfer + ", Date: " + i.dateTransfer + ", From: " + i.fromTransfer + ", To: " + i.toTransfer
		return ""

##################### Search Player ##########################
def searchPlayer(name):
	urlPage = page + name + pageEnd
	pageTree = requests.get(urlPage, headers=headers)
	pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

	players = pageSoup.find_all("a", {"class": "spielprofil_tooltip"})
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
	
	transfer_date = pageSoup.find_all("td", {"class": "zentriert hide-for-small"})
	club = pageSoup.find_all("td", {"class": "hauptlink no-border-links hide-for-small vereinsname"})
	i = 0
	j = 0
	transfer = []

	while (j < len(club)):
		x = SimpleClass()
		x.seasonTransfer =  removeWriteSpaces(transfer_date[i].text)
		x.dateTransfer = removeWriteSpaces(transfer_date[i + 1].text)
		x.fromTransfer =  removeWriteSpaces(club[j].text)
		x.toTransfer =  removeWriteSpaces(club[j + 1].text)
		i = i + 3
		j = j + 2
		transfer.append(x)
        
	player =  playerInformationObject(name, born, cityBorn, nationality, heigth, position, endContract, transfer)
	print player
	#print "Print Player Information"
	#print player.__dict__

	#playerInformation = pageSoup.find_all("div", {"class": "table-footer"})
	#playerInformation = playerInformation[0].findChildren('a')
	#playerpage = "https://www.transfermarkt.com" + playerInformation[0]['href']

	#pageTree = requests.get(playerpage, headers=headers)
	#pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

	#playerInformation =	pageSoup.find_all( 'div', string="Performance per club")
	#playerInformation = playerInformation[0].parent
	#print playerInformation.text
	

############################## Main #########################
linkPlayer = searchPlayer(sys.argv[1])
getInformation(linkPlayer)
