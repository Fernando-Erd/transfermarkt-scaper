import requests
import sys
from bs4 import BeautifulSoup
import time

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page = "https://www.transfermarkt.com/campeonato-brasileiro-serie-a/transfers/wettbewerb/BRA1/saison_id/2017"

#################### Get Player Information ##################
def removeWriteSpaces(text):
	return text.encode('utf-8').replace("\n", "").replace("\t", "").replace("\r", "")

def getInformationTransfer(pageSoup, count, club):

	#get information
	player = pageSoup.find_all("span", {"class": "hide-for-small"})
	age = pageSoup.find_all("td", {"class": "zentriert alter-transfer-cell"})
	country = pageSoup.find_all("td", {"class": "zentriert nat-transfer-cell"})
	position = pageSoup.find_all("td", {"class": "pos-transfer-cell"})
	to = pageSoup.find_all("td", {"class": "no-border-links verein-flagge-transfer-cell"})
	valueTransfer = pageSoup.find_all("td", {"class": "rechts"})

#	print "Name" + str(len(player))
#	print "Age" + str(len(age))
#	print "Country" + str(len(country))
#	print "Position" + str(len(position))
#	print "Value" + str(len(to))
#	print "To" + str(len(valueTransfer))
#	while (i < 0):
#		print "------------Player-------------"
#		print "Name: " + removeWriteSpaces(player[i].text)
#		print "Age: " + removeWriteSpaces(age[i].text)
#		print "Country: " + removeWriteSpaces(country[i].findChildren('img')[0]['alt'])
#		print "Position: " + removeWriteSpaces(position[i].text)
#		print "ValueMarket: " + removeWriteSpaces(valueTransfer[2*i].text)
#		print "to: " + removeWriteSpaces(to[i].text)
#		print "ValueTransfer: " + removeWriteSpaces(valueTransfer[2*i + 1].text)
#		print "\n"
#		i = i + 1

	#Write in csv file
	i = 0
	with open("teste.csv", "a") as file:
		while (i < len(age)):
			file.write(removeWriteSpaces(player[i].text) + ";")
			file.write(removeWriteSpaces(age[i].text) + ";")
			file.write(removeWriteSpaces(country[i].findChildren('img')[0]['alt']) + ";")
			file.write(removeWriteSpaces(position[i].text) + ";")
			file.write(removeWriteSpaces(valueTransfer[2*i].text) + ";")
			
			if count == 1:
				file.write(removeWriteSpaces(club) + ";")
				file.write(removeWriteSpaces(to[i].text) + ";")
			else:
				file.write(removeWriteSpaces(to[i].text) + ";")
				file.write(removeWriteSpaces(club) + ";")
			
			file.write(removeWriteSpaces(valueTransfer[2*i + 1].text) + "\n")
			i = i + 1
			print i


## init in table[4]
def getTable_and_Club(pageSoup):
	tableBox = pageSoup.find_all("div", {"class": "box"})

	for i in range (4,len(tableBox)):
		try:
			club = tableBox[i].find_all("div", {"class": "table-header"})
			print "Club:" + club[0].text

			beginTable = tableBox[i].find_all("table")

			count = 0
			for j in beginTable:
				getInformationTransfer(j, count, club[0].text)
				count = count + 1
		except:
			pass

############################## Main #########################
with open("teste.csv", "a") as file:
	file.write("Player;Age;Country;Position;MarketValue;De;Para;TransferValue\n")
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
getTable_and_Club(pageSoup)
