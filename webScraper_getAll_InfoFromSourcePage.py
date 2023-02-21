# With google chrome: Shows the webpage
# INSERT INTO usedcar_cargurus.maintable

import time
import mechanicalsoup
import mysql.connector

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import math

from selenium.webdriver.chrome.options import Options


def getIDs(database='usedcar_cargurus',table='extended_table'):
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
    
    # sourcePage:
    sql = " SELECT * FROM variables"
    mycursor.execute(sql)
    rowResults = mycursor.fetchall()
    sourcePage = rowResults[0][0]
        
    # idList:
    year_min=input("Year_min:")
    year_max=input("Year_max:")
    sql = "SELECT id FROM " + table + " WHERE (year BETWEEN " + year_min + " AND " + year_max + ")"
    
    #Find untouched rows:--------------------------
    sql = sql + " AND " + \
    "transmission is null AND " + \
    "drivetrain is null AND " + \
    "engine_hp is null AND " + \
    "engine_litre is null AND " + \
    "engine_cylinder is null AND " + \
    "fuel_type is null AND " + \
    "fuel_economy is null AND " + \
    "n_doors is null AND " + \
    "color_interior is null AND " + \
    "color_Exterior is null AND " + \
    "battery_range is null AND " + \
    "charge_time is null "
    #--------------------------Find untouched rows
    sql = sql + " ORDER BY make"
    
    mycursor.execute(sql)
    rowResults = mycursor.fetchall()
    idList=[]
    for row in rowResults:
        ID=row[0]
        idList.append(ID)
    
    mycursor.close()
    mydb.close()
    
    print('-----------------------')
    print('Number of Cases:',len(idList))
    print('-----------------------')
    
    return idList, sourcePage


def insertInDB(ID,transmission,
                driveTrain,
                engineHP,
                engineLitre,
                engineCylinder,
                fuelType,
                fuelEconomy,
                nofDoors,
                colorInt,
                colorExt,
                batteryRange,
                chargeTime,
                database='usedcar_cargurus',
                table='extended_table'):
    
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

    sql = "UPDATE " + table + " SET "
    sqlQuery=""
    if not ( transmission is None): sqlQuery = sqlQuery + " transmission = '" + transmission + "'," 
    if not ( driveTrain is None): sqlQuery = sqlQuery + " drivetrain = '" + driveTrain + "',"
    if not ( engineHP is None): sqlQuery = sqlQuery + " engine_hp = " + str(engineHP) + "," 
    if not ( engineLitre is None): sqlQuery = sqlQuery + " engine_litre = " + str(engineLitre) + "," 
    if not ( engineCylinder is None): sqlQuery = sqlQuery + " engine_cylinder = '" + engineCylinder + "'," 
    if not ( fuelType is None): sqlQuery = sqlQuery + " fuel_type = '" + fuelType + "'," 
    if not ( fuelEconomy is None): sqlQuery = sqlQuery +       " fuel_economy = " + str(fuelEconomy) + "," 
    if not ( nofDoors is None): sqlQuery = sqlQuery +       " n_doors = " + str(nofDoors) + "," 
    if not ( colorInt is None): sqlQuery = sqlQuery + " color_interior = '" + colorInt + "'," 
    if not ( colorExt is None): sqlQuery = sqlQuery + " color_Exterior = '" + colorExt + "'," 
    if not ( batteryRange is None): sqlQuery = sqlQuery + " battery_range = " + str(batteryRange) + "," 
    if not ( chargeTime is None): sqlQuery = sqlQuery + " charge_time = " + str(chargeTime) + "," 
    
    if len(sqlQuery)>0:
        sql = sql + sqlQuery[0:len(sqlQuery)-1] + " WHERE id = " + str(ID)
    
    mycursor.execute(sql)
    
    mydb.commit();
    mycursor.close()
    mydb.close()

    return 0
    
    
idList,sourcePage = getIDs()


nFails=0
nSuccess=0

for ID in idList:
    print('id:',ID)
    transmission=None
    driveTrain=None
    engineHP=None
    engineLitre=None
    engineCylinder=None
    fuelType=None
    fuelEconomy=None
    nofDoors=None
    colorInt=None
    colorExt=None
    batteryRange=None
    chargeTime=None

    webAddress = sourcePage + str(ID)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),chrome_options=chrome_options)
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #driver.minimize_window()
    
    driver.get(webAddress)
    time.sleep(0.1)
    html = driver.execute_script("return document.documentElement.innerHTML;")
    time.sleep(0.1)
    soup = BeautifulSoup(html,'html.parser')
    
    
    
    # Find details:
    ulElements = soup.find_all('ul',{'class':'E5hc4E'})
    if len(ulElements)==0:
        ulElements = soup.find_all('ul',{'class':'E5hc4E J32xgN'})
    if len(ulElements)==0:
        nFails+=1
        print("Unable to load the page!")
        print("Seccess: ",nSuccess)
        print("Fails: ",nFails)
        print('----------------------------')
        continue;
    nSuccess+=1
    ulElement = ulElements[0]
    
    element_img=ulElement.find_all('img')
        
    for element in element_img:
        featureName=element['alt']
        featureValue=element.findNext('p').text
        
        if featureName=='Transmission:':
            transmission=featureValue
        elif featureName=="Drivetrain:":
            driveTrain=featureValue
        elif featureName=="Engine:":
            splitByHP=featureValue.split("hp")
            if len(splitByHP)>1:
                engineHP=int(splitByHP[0])
                splitByL=splitByHP[1].split("L")
                if len(splitByL)>1: 
                    engineLitre=float(splitByL[0])
                    engineCylinder=splitByL[1][1:2]
                
        elif featureName=="Fuel Type:":
            fuelType=featureValue
        elif featureName=="Number of doors":
            nofDoors=int(featureValue.replace(" doors",""))
        elif featureName=="Fuel Economy:":
            splitted = featureValue.split("L/100km")
            if len(splitted)>1:
                fuelEconomy=float(splitted[0])
        elif featureName=="Interior Colour:":
            colorInt=featureValue
        elif featureName=="Exterior Colour:":
            colorExt=featureValue
        elif featureName=="Battery Range":
            batteryRange=int(featureValue.replace("km",""))
        elif featureName=="Charge Time":
            chargeTime=float(featureValue.replace("hr",""))
    
    
    # Find image sources:
    

    
    insertInDB(ID,transmission,
                driveTrain,
                engineHP,
                engineLitre,
                engineCylinder,
                fuelType,
                fuelEconomy,
                nofDoors,
                colorInt,
                colorExt,
                batteryRange,
                chargeTime)
    
    
    print("Success: ",nSuccess)
    print("Fail: ",nFails)
    print('----------------------------')
    
    if nFails+nSuccess>10 and nFails>5*nSuccess:
        print("**********************")
        print("**********************")
        print("**********************")
        print("Quit! Too many fails detected!")
        exit()
    driver=None
    

exit()
