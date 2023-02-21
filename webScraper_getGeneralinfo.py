# With google chrome: Shows the webpage
# INSERT INTO usedcar_cargurus.maintable

import time
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import math
import mysql.connector



def saveDataIntoDatabase(ID,price,mileage,title,address,estimatedPrice,
                        database='usedcar_cargurus',table='maintable'):
             
    user = 'mk'
    host = 'localhost'
    password = 'admin'
    
    mydb = mysql.connector.connect(
      host=host,
      user=user,
      password=password,
      database = database
    )
    
    mycursor = mydb.cursor()
    
    for iRow in range(len(ID)):
        sql = "INSERT IGNORE INTO " + table + \
            " (ID,price,mileage,title,address,estimated_price) " + \
            " VALUES (%s, %s, %s, %s, %s, %s)"
        val = (ID[iRow],price[iRow],mileage[iRow],title[iRow],address[iRow],estimatedPrice[iRow])

        mycursor.execute(sql, val)
        
    mydb.commit();
    mycursor.close()
    mydb.close()
    
    print('Data were successfully inserted!')
    
    return 0
    
# TEST INSERT Query:
#saveDataIntoDatabase([1,2],[100,200],[1000,2000],["t1","t2"],["ad1","ad2"],[10,11])

priceMin=1

while 1<2:
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    '''
    f = open("lastPriceSaved.txt", "r")
    priceMin=int(f.readlines()[0])
    f.close()
    print("priceMin=",priceMin)
    '''



    #priceMin=17388
    priceMax = 1000000
    webAddressMain = 'https://www.cargurus.ca/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip=N9C%204E1&inventorySearchWidgetType=PRICE&maxPrice=' + str(priceMax)+ '&showNegotiable=false&sortDir=ASC&sourceContext=popularLinks&distance=500&minPrice=' + str(priceMin)+ '&sortType=PRICE'

    idList = []
    priceList = []
    titleList = []
    mileageList = []
    addressList = []
    marketAnalysis = []
    estimatedPrice = []


    saveInterval = 200

    iPage=1
    nPages=2
    nCasesPerPage =15

    while iPage <=nPages:
    #while iPage <=10:

        lenStart = len(idList)
        if iPage==1:
            webAddress = webAddressMain
        else:
            webAddress = webAddressMain + '#resultsPage='+str(iPage)
        
        driver.get(webAddress)
            
        time.sleep(1) # Let the user actually see something!
       
       
        html = driver.execute_script("return document.documentElement.innerHTML;")
        soup = BeautifulSoup(html,'html.parser')
        

        if iPage==1:
            nCases = int(soup.find('span',{'class':'eegHEr'}).findChildren('strong')[1].text.replace(',',''))
            nPages = math.ceil(nCases/nCasesPerPage)
            
            print('---------------------------------')
            print('Number of Cases: ' + str(nCases))
            print('Number of Pages: ' + str(nPages))
            print('---------------------------------')
            
        print('\n Page=',iPage)
        print('-------------------------')
        
        anchorList = soup.find_all('a', {'href': re.compile('^(?=^#listing=)(?=.*/NONE$)'), 'class':'lmXF4B c7jzqC A1f6zD'})
        
        
        for idElement in anchorList:
            #print(idElement['href'])
            idNew=int(re.split('/',(re.split('=',idElement['href'])[1]))[0])
            idList.append(idNew)
            
            goalElement = idElement.find("div",{'class':'biZGS4'}).find().findChildren('h4',{'class':'ihi1SG'})[0]    # class: 'ihi1SG'
            price = goalElement.find('div',recursive=False).find('span',recursive=False).text.split(" ")[0]
            price = int(price.replace('$','').replace(',',''))
            priceList.append(price)
            
            titleList.append(idElement.findChildren('h4',{'class':'vO42pn'})[0]['title'] )
            
            mileage = idElement.findChildren('span',{'class':'SLB6rU'})[0].text.replace(' km','').replace(',','')
            if mileage.isnumeric():
                mileage=int(mileage)
            else:
                mileage=0
            mileageList.append(mileage)
            
            
            maVal=0
            maTxt=idElement.findChildren('div',{'class':'Z3BA9L'})[0].text
            if "below" in maTxt:
                maVal = int(maTxt.replace(' below market','').replace('$','').replace(',',''))
            elif "above" in maTxt:
                maVal = -int(maTxt.replace(' above market','').replace('$','').replace(',',''))
             
            estimatedPrice.append(price + maVal)
           
            addressList.append(idElement.findChildren('span',{'class':'A7SYzv'})[0].text)
                    
        for i in range((iPage-1)*15-1,len(idList)):
            print(idList[i], priceList[i],titleList[i],mileageList[i],addressList[i],estimatedPrice[i])
        
        iPage +=1
        
        if len(idList)==saveInterval:
            saveDataIntoDatabase(ID=idList,price=priceList,mileage=mileageList,
                                title=titleList,address=addressList,estimatedPrice=estimatedPrice)
            idList=[]
            priceList=[]
            titleList=[]
            mileageList=[]
            addressList=[]
            estimatedPrice=[]

        lenEnd = len(idList)
        
        if lenStart==lenEnd:
            break
            
    saveDataIntoDatabase(ID=idList,price=priceList,mileage=mileageList,
                                title=titleList,address=addressList,estimatedPrice=estimatedPrice)
    
    priceMin=priceList[-1]

    print('ERROR!')
    driver=None
exit()    

       


