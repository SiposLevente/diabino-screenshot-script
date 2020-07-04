import os
import datetime
import configparser
from calendar import monthrange
from time import sleep
from sys import platform
from sys import argv
from sys import exit
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# Adott string hónap hanyadik hónap
def melyikHonap(honap):
    honap = honap.lower()
    if honap == "január":
        return 1
    if honap == "február":
        return 2
    if honap == "március":
        return 3
    if honap == "április":
        return 4
    if honap == "május":
        return 5
    if honap == "június":
        return 6
    if honap == "július":
        return 7
    if honap == "augusztus":
        return 8
    if honap == "szeptember":
        return 9
    if honap == "október":
        return 10
    if honap == "november":
        return 11
    if honap == "december":
        return 12


# DiaBino-ba bejelentkezés
def bejelentkezes(EMAIL, JELSZO, driver, comments):
    if comments:
        print("Bejelentkezés...")

    driver.get('https://app.diabino.com/hu/signin')
    element = driver.find_element_by_xpath("//input[@type='email']")
    element.send_keys(EMAIL)
    element = driver.find_element_by_xpath("//input[@type='password']")
    element.send_keys(JELSZO)
    element.send_keys(Keys.RETURN)
    driver.implicitly_wait(10)

    if comments:
        print("Oldal betöltése...")
        sleep(3)

    try:
        element = driver.find_element_by_xpath("//a[@href='/hu/diary']")
    except:
        driver.close()
        exit("Bejelentkezés nem sikerült!")

    element.click()

    if comments:
        print("Bejelentkezés sikeres!")
        print("Oldal betöltött!")


# Kép készítése
def kepKeszitese(KEPEKMAPPA, driver, driverType, datum, comments):
    element = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[1]/main/div/div/div[2]/div[2]/div[1]/div[1]")
    if comments:
        print("Kép készítése...")
    driver.execute_script('''
            var element = document.getElementsByClassName("v-sheet theme--light v-toolbar v-app-bar v-app-bar--fixed primary"), index;
            for (index = element.length - 1; index >= 0; index--) {
                element[index].parentNode.removeChild(element[index]);
            }
        ''')
    sleep(3)
    if driverType == "firefox":
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            element.screenshot(str(KEPEKMAPPA) + '/%s.png' % datum.strftime('%Y%m%d'))
        elif platform == "win32":
            element.screenshot(str(KEPEKMAPPA) + '\\%s.png' % datum.strftime('%Y%m%d'))
    else:
        element = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[1]/main/div/div/div[2]/div[2]/div[1]/div[1]")
        total_height = element.size["height"] + 1000
        driver.set_window_size(1920, total_height)
        sleep(3)
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            element.screenshot(element.screenshot(str(KEPEKMAPPA) + '/%s.png' % datum.strftime('%Y%m%d')))
        elif platform == "win32":
            element.screenshot(str(KEPEKMAPPA) + '\\%s.png' % datum.strftime('%Y%m%d'))

    if comments:
        print("Kép elkészült!")


# Nap léptetése, ha balra:"True" akkor jobbra lép, ha balra:"False" akkor jobbra lép
def napLeptet(driver, balra):
    driver.set_window_size(450, 820)

    if balra:
        element = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[1]/main/div/div/div[2]/div[2]/div/div[1]/div[1]/div[3]/div[3]/div/div/div[2]/button")
    else:
        element = driver.find_element_by_xpath("/html/body/div[3]/div/div/div/main/div/div/div[2]/div[2]/div/div[1]/div[1]/div[3]/div[3]/div/div/div[4]/button")

    sleep(0.5)
    element.click()
    driver.set_window_size(1920, 1080)


# Honap léptetése, ha balra:"True" akkor jobbra lép, ha balra:"False" akkor jobbra lép
def honapLeptet(driver, driverType, balra):
    if driverType == "chrome":
        sleep(1)
    if balra:
        element = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[1]/main/div/div/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[1]/button/span/i")
    else:
        element = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[1]/main/div/div/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[3]/button/span/i")
    element.click()


# A script éppen melyik napnál tart
def getDatum(driver):
    dateSting = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[1]/main/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div/div/div/div[2]/div[2]").text
    dateSting = dateSting + " " + driver.find_element_by_xpath("/html/body/div[3]/div/div/div/main/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div/div/div/div[1]/strong").text
    dateSting = dateSting.replace('.', '')
    datum = dateSting.split(' ')
    datum[1] = melyikHonap(datum[1])
    return datum


# Adott dátumhoz lépés
def datumKeres(driver, driverType, keresettDatum):
    while int(getDatum(driver)[0]) != int(keresettDatum[0]):
        if int(getDatum(driver)[0]) > int(keresettDatum[0]):
            for i in range(0, 12):
                honapLeptet(driver, driverType, True)
        if int(getDatum(driver)[0]) < int(keresettDatum[0]):
            for i in range(0, 12):
                honapLeptet(driver, driverType, False)

    while int(getDatum(driver)[1]) != int(keresettDatum[1]):
        if int(getDatum(driver)[1]) > int(keresettDatum[1]):
            honapLeptet(driver, driverType, True)

        if int(getDatum(driver)[1]) < int(keresettDatum[1]):
            honapLeptet(driver, driverType, False)
    sleep(2)
    while int(getDatum(driver)[2]) != int(keresettDatum[2]):
        if int(getDatum(driver)[2]) > int(keresettDatum[2]):
            napLeptet(driver, True)

        if int(getDatum(driver)[2]) < int(keresettDatum[2]):
            napLeptet(driver, False)
    sleep(3)


# Script használatát kiíró script
def hasznalatiUtasitasok():
    print("Script használata: ")
    print("\t\tA scriptnek 3 féle módja van: ")
    print("\t\t\t1, diabinoScreenshot.py")
    print("\t\t\t\tA script bejelentkezik a DiaBinóban és a mai nap vércukor értékeit lefényképezi és elmenti a megadott mappába")
    print("\t\t\t2, diabinoScreenshot.py ÉÉÉÉ-HH-NN")
    print("\t\t\t\tA script bejelentkezik a DiaBinóban és a megadott dátumokhoz tartozó adatokat lefényképezi és elmenti a megadott mappába")
    print("\t\t\t3, diabinoScreenshot.py ÉÉÉÉ-HH-NN ÉÉÉÉ-HH-NN")
    print("\t\t\t\tA script bejelentkezik a DiaBinóban és a megadott intervallumon lévő napokhoz tartozó adatokat lefényképezi és elmenti a megadott mappába\n")
    print("\t\tMegfelelő dátum beviteli formátum: \"ÉÉÉÉ-HH-NN\" (pl:2020-07-27)")
    print("\t\tBeállítások a settings.ini fájlban találhatóak abban a mappában ahol a script van")


# Helyes bemenet vizsgálat
def datumTeszt(stringDatum, driver):
    datumArray = stringDatum.split("-")
    if len(datumArray) != 3:
        driver.close()
        exit('Nem megfelelő bemenet, a bemeneti dátumnak hasonlóképpen kell kinéznie: ÉÉÉÉ-HH-NN')
    if int(datumArray[0]) > datetime.datetime.now().year or int(datumArray[0]) < 2010:
        driver.close()
        exit("Megadott év az értelmezhető intervallumon kívülre esik")
    if int(datumArray[1]) > 12 or int(datumArray[1]) < 1:
        driver.close()
        exit("Megadott hónap az értelmezhető intervallumon kívülre esik")
    napokSzama = monthrange(int(datumArray[0]), int(datumArray[1]))
    if int(datumArray[2]) > napokSzama[1] or int(datumArray[2]) < 1:
        driver.close()
        exit("Megadott nap az értelmezhető intervallumon kívülre esik")
    if datetime.datetime.now().year == datumArray[0]:
        if datetime.datetime.now().month == datumArray[1]:
            if datetime.datetime.now().day < datumArray[2]:
                driver.close()
                exit("Megadott dátum jövőbeli!")


# Chrome vagy Firefox webdriver létrehozása
def initDriver(driverType, headLess):
    driver = None
    if driverType == "firefox":
        from selenium.webdriver.firefox.options import Options
        options = Options()
        options.log.level = "fatal"
        options.headless = headLess
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            if not os.path.isfile("./driver/geckodriver"):
                exit("Nincs 'geckodriver' file a './driver/' mappában!")
            driver = webdriver.Firefox(options=options, executable_path=r'./driver/geckodriver', service_log_path=r'/tmp/geckodriver.log')
        else:
            if not os.path.isfile(".\\driver\\geckodriver.exe"):
                exit("Nincs 'geckodriver.exe' file a '.\\driver\\' mappában!")
            driver = webdriver.Firefox(options=options, executable_path=r'.\driver\geckodriver.exe', service_log_path=r'C:\Windows\Temp\geckodriver.log')

    elif driverType == "chrome":
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()

        if headLess:
            chrome_options.add_argument("--headless")

        if platform == "linux" or platform == "linux2" or platform == "darwin":
            if not os.path.isfile("./driver/chromedriver"):
                exit("Nincs 'chromedriver' file a './driver/' mappában!")
            driver = webdriver.Chrome(options=chrome_options, executable_path=r'.\driver\chromedriver', service_args=["--log-path=/tmp/chromedriver.log"])
        else:
            if not os.path.isfile(r".\driver\chromedriver.exe"):
                exit("Nincs 'chromedriver.exe' file a '.\\driver\\' mappában!")
            driver = webdriver.Chrome(options=chrome_options, executable_path=r'.\driver\chromedriver.exe', service_args=["--log-path=C:\\Windows\\Temp\\chromedriver.log"])
    else:
        exit("Nem megfelelő driver a konfigurációs fájlban")
    return driver


# Beállítások beolvasása settings.ini fájlból
config = configparser.ConfigParser()
config.read('settings.ini')
try:
    EMAIL = config["ADATOK"]["email"]
    JELSZO = config["ADATOK"]["jelszo"]
    KEPEKMAPPA = config["ADATOK"]["kepekmappa"]
    KOMMENTEK = bool(int(config["ADATOK"]["kommentek"]))
    DRIVER = config["ADATOK"]["webdriver"]
except KeyError:
    exit("Konfigurációs file nem megfelelően van kitöltve vagy nem létezik!")

# Driver létrehozása
driver = initDriver(DRIVER, True)

# Képek mappa létezésének vizsgálata
if not os.path.isdir(str(KEPEKMAPPA)):
    print("Képek mappa létrehozva!")
    os.mkdir(str(KEPEKMAPPA))

# 2 argumentum lekezelése, ez két dátum közötti intervallumon készít képeket
if len(argv) == 3:
    datumTeszt(argv[1], driver)
    datumTeszt(argv[2], driver)
    startDate = argv[1].split('-')
    endDate = argv[2].split('-')
    startDate = datetime.datetime(int(startDate[0]), int(startDate[1]), int(startDate[2]))
    endDate = datetime.datetime(int(endDate[0]), int(endDate[1]), int(endDate[2]))
    if startDate > endDate:
        temp = startDate
        startDate = endDate
        endDate = temp
    bejelentkezes(EMAIL, JELSZO, driver, KOMMENTEK)
    endDate = endDate + datetime.timedelta(days=1)
    deltaDays = abs((startDate - endDate).days)
    counter = 1
    while startDate != endDate:
        startDateArray = [startDate.year, startDate.month, startDate.day]
        datumKeres(driver, DRIVER, startDateArray)
        kepKeszitese(KEPEKMAPPA, driver, DRIVER, startDate, KOMMENTEK)
        startDate = startDate + datetime.timedelta(days=1)
        if KOMMENTEK:
            print("[" + str(counter) + "/" + str(deltaDays) + "]")
            counter = counter + 1

# 1 argumetnum lekezelése, egy adott dátumról készít képet
elif len(argv) == 2:
    datumTeszt(argv[1], driver)
    bejelentkezes(EMAIL, JELSZO, driver, KOMMENTEK)
    keresettDatum = argv[1].split('-')
    datumKeres(driver, DRIVER, keresettDatum)
    datum = datetime.datetime(int(keresettDatum[0]), int(keresettDatum[1]), int(keresettDatum[2]))
    kepKeszitese(KEPEKMAPPA, driver, DRIVER, datum, KOMMENTEK)

# 0 argumentum lekezelése, mai nap adatairól készít képet
elif len(argv) == 1:
    bejelentkezes(EMAIL, JELSZO, driver, KOMMENTEK)
    kepKeszitese(KEPEKMAPPA, driver, DRIVER, datetime.datetime.now(), KOMMENTEK)

# Hibás bemenet esetén kiírja hogy a scriptet hogyan lehet használni
else:
    hasznalatiUtasitasok()

if KOMMENTEK:
    print("Script lefutott!")

driver.close()
