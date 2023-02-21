import requests
from bs4 import BeautifulSoup
import numpy
import re

webAddressMain = 'https://www.cargurus.ca/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip=N9C%204E1&inventorySearchWidgetType=PRICE&showNegotiable=false&sortDir=ASC&sourceContext=popularLinks&distance=500&minPrice=1&sortType=NEWEST_CAR_YEAR#resultsPage=10'
idList = []

for iPage in range(1):
    if iPage==0:
        webAddress = webAddressMain
    else:
        webAddress = webAddressMain + '#resultsPage='+str(iPage+1)
        
    response = requests.get(webAddress)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    titleList = soup.find_all('h4',attrs={'class':'titleText'})
    priceList = soup.find_all('span',attrs={'class':'price'})
    
    print('\n-------------------------------------------')
    for iList in range(len(titleList)):
        print(str(iList+1) + ": "+ (titleList[iList].text).strip() + "; price: " + priceList[iList].text.strip())
    print('\n-------------------------------------------')
    
    #idList = soup.find_all('a', {'href': re.compile('^#listing=|/NONE')})    starts with '#listing='

    anchorList = soup.find_all('a', {'href': re.compile('^(?=^#listing=)(?=.*/NONE$)')})
    soup=None
    
    
    
    for idElement in anchorList:
        print(idElement['href'])
        idNew=int(re.split('/',(re.split('=',idElement['href'])[1]))[0])
        idList.append(idNew)
    
idList = list(set(idList))
#idList.sort()    
for i in range(len(idList)):
    print(idList[i])

            
            
        
        
    
