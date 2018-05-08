import requests
import sys
from bs4 import BeautifulSoup
headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page = "https://www.transfermarkt.com/campeonato-brasileiro-serie-a/transfers/wettbewerb/BRA1/saison_id/2017"

#################### Get Player Information ##################
def removeWriteSpaces(text):
	return text.encode('utf-8').replace("\n", "").replace("\t", "").replace("\r", "")

def getInformationTransfer(pageSoup):
	player = pageSoup.find_all("span", {"class": "hide-for-small"})
	age = pageSoup.find_all("td", {"class": "zentriert alter-transfer-cell"})
	country = pageSoup.find_all("td", {"class": "zentriert nat-transfer-cell"})
	position = pageSoup.find_all("td", {"class": "pos-transfer-cell"})
	to = pageSoup.find_all("td", {"class": "no-border-links verein-flagge-transfer-cell"})
	valueTransfer = pageSoup.find_all("td", {"class": "rechts"})


	i = 0
	while (i < 5):
		print "------------Player-------------"
		print "Name: " + removeWriteSpaces(player[i].text)
		print "Age: " + removeWriteSpaces(age[i].text)
		print "Country: " + removeWriteSpaces(country[i].findChildren('img')[0]['alt'])
		print "Position: " + removeWriteSpaces(position[i].text)
		print "ValueMarket: " + removeWriteSpaces(valueTransfer[2*i].text)
		print "to: " + removeWriteSpaces(to[i].text)
		print "ValueTransfer: " + removeWriteSpaces(valueTransfer[2*i + 1].text)
		print "\n"
		i = i + 1

def getClub(pageSoup):
	club = pageSoup.find_all("div", {"class": "table-header"})
	print "oie"
	for a in club:
		if "Transfer" not in removeWriteSpaces(a.text):
			print removeWriteSpaces(a.text)
	getInformationTransfer(pageSoup)


def getTbody(pageSoup):
	table = pageSoup.find_all("div", {"class": "box"})
#	with open("output1.html", "w") as file:
#		file.write(str(table[10]))
	getClub(table[10])
############################## Main #########################
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
#getInformationTransfer(pageSoup)
#getClub(pageSoup)
getTbody(pageSoup)
