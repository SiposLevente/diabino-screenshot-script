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
from selenium.webdriver.firefox.options import Options


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
        exit("Bejelentkezés nem sikerült!")

    element.click()

    if comments:
        print("Bejelentkezés sikeres!")
        print("Oldal betöltött!")

def kepKeszitese(KEPEKMAPPA, driver, datum, comments):
    element = driver.find_element_by_xpath("//div[@class='v-card v-sheet theme--light']")
    if comments:
        print("Kép készítése...")
    driver.execute_script('''
            var element = document.getElementsByClassName("v-sheet theme--light v-toolbar v-app-bar v-app-bar--fixed primary"), index;
            for (index = element.length - 1; index >= 0; index--) {
                element[index].parentNode.removeChild(element[index]);
            }
        ''')
    sleep(1)
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        element.screenshot(str(KEPEKMAPPA) + '/%s.png' % datum.strftime('%Y%m%d'))
    elif platform == "win32":
        element.screenshot(str(KEPEKMAPPA) + '\\%s.png' % datum.strftime('%Y%m%d'))
    if comments:
        print("Kép elkészült!")


def napLeptet(driver, balra):
    # ha balra:"True" akkor jobbra lép, ha balra:"False" akkor jobbra lép
    driver.set_window_size(450, 820)
    if balra:
        element = driver.find_element_by_xpath(
            "/html/body/div[3]/div/div/div[1]/main/div/div/div[2]/div[2]/div/div[1]/div[1]/div[3]/div[3]/div/div/div[2]/button")
    else:
        element = driver.find_element_by_xpath(
            "/html/body/div[3]/div/div/div/main/div/div/div[2]/div[2]/div/div[1]/div[1]/div[3]/div[3]/div/div/div[4]/button")
    sleep(0.5)
    element.click()
    driver.set_window_size(1920, 1080)


def honapLeptet(driver, balra):
    # ha balra:"True" akkor jobbra lép, ha balra:"False" akkor jobbra lép
    if balra:
        element = driver.find_element_by_xpath(
            "/html/body/div[3]/div/div/div[1]/main/div/div/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[1]/button/span/i")
    else:
        element = driver.find_element_by_xpath(
            "/html/body/div[3]/div/div/div[1]/main/div/div/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[3]/button/span/i")
    element.click()


def getDatum(driver):
    dateSting = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div/div[1]/main/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div/div/div/div[2]/div[2]").text
    dateSting = dateSting + " " + driver.find_element_by_xpath(
        "/html/body/div[3]/div/div/div/main/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div/div/div/div[1]/strong").text
    dateSting = dateSting.replace('.', '')
    datum = dateSting.split(' ')
    datum[1] = melyikHonap(datum[1])
    return datum


def datumKeres(driver, keresettDatum):
    while int(getDatum(driver)[0]) != int(keresettDatum[0]):
        if int(getDatum(driver)[0]) > int(keresettDatum[0]):
            for i in range(0, 12):
                honapLeptet(driver, True)
        if int(getDatum(driver)[0]) < int(keresettDatum[0]):
            for i in range(0, 12):
                honapLeptet(driver, False)

    while int(getDatum(driver)[1]) != int(keresettDatum[1]):
        if int(getDatum(driver)[1]) > int(keresettDatum[1]):
            honapLeptet(driver, True)

        if int(getDatum(driver)[1]) < int(keresettDatum[1]):
            honapLeptet(driver, False)
    sleep(2)
    while int(getDatum(driver)[2]) != int(keresettDatum[2]):
        if int(getDatum(driver)[2]) > int(keresettDatum[2]):
            napLeptet(driver, True)

        if int(getDatum(driver)[2]) < int(keresettDatum[2]):
            napLeptet(driver, False)
    sleep(3)


def hasznalatiUtasitasok():
    print("Program használata: ")
    print("\t\tA programnak 3 féle módja van: ")
    print("\t\t\t1, diabinoScreenshot.py")
    print(
        "\t\t\t\tA program bejelentkezik a diabinóba és a mai nap vércukor értékeit lefényképezi és elmenti a megadott mappába")
    print("\t\t\t2, diabinoScreenshot.py ÉÉÉÉ-HH-NN")
    print(
        "\t\t\t\tA program bejelentkezik a diabinóba és a megadott dátumothoz tartozó adatokat lefényképezi és elmenti a megadot mappába")
    print("\t\t\t3, diabinoScreenshot.py ÉÉÉÉ-HH-NN ÉÉÉÉ-HH-NN")
    print(
        "\t\t\t\tA program bejelentkezik a diabinóba és a megadott intervallumon lévő napokhoz tartozó adatokat lefényképezi és elmenti a megadot mappába\n")
    print("\t\tMegfelelő dátum beviteli formátum: \"ÉÉÉÉ-HH-NN\" (pl:2020-07-27)")
    print("\t\tBeállítások a settings.txt fájlban találhatóak abban a mappában ahol a program található")


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


# -----------------------------------BEÁLLíTÁSOK-----------------------------------
config = configparser.ConfigParser()
config.read('settings.ini')
try:
    EMAIL = config["ADATOK"]["email"]
    JELSZO = config["ADATOK"]["jelszo"]
    KEPEKMAPPA = config["ADATOK"]["kepekmappa"].replace('\\', '\\\\')
    KOMMENTEK = bool(int(config["ADATOK"]["kommentek"]))
except KeyError:
    exit("Konfigurációs file nem megfelelően van kitöltve vagy nem létezik!")

# ---------------------------------------------------------------------------------

if not os.path.isdir(str(KEPEKMAPPA)):
    print("Képek mappa létrehozva!")
    os.mkdir(str(KEPEKMAPPA))

options = Options()
options.log.level = "fatal"

# -----------------------
# Villogó ablakok fognak megjelenni ha ezt kikapcsoljuk, epilepszia veszély!!!
options.headless = True
# -----------------------

if platform == "linux" or platform == "linux2":
    driver = webdriver.Firefox(options=options, executable_path=r'./driver/lin/geckodriver',
                               service_log_path=r'/dev/null/geckodriver.log')
elif platform == "darwin":
    driver = webdriver.Firefox(options=options, executable_path=r'./driver/mac/geckodriver',
                               service_log_path=r'/dev/null/geckodriver.log')
else:
    driver = webdriver.Firefox(options=options, executable_path=r'.\driver\win\geckodriver.exe',
                               service_log_path=r'C:\Windows\Temp\geckodriver.log')

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
        datumKeres(driver, startDateArray)
        kepKeszitese(KEPEKMAPPA, driver, startDate, KOMMENTEK)
        startDate = startDate + datetime.timedelta(days=1)
        if KOMMENTEK:
            print("[" + str(counter) + "/" + str(deltaDays) + "]")
            counter = counter + 1

elif len(argv) == 2:
    datumTeszt(argv[1], driver)
    bejelentkezes(EMAIL, JELSZO, driver, KOMMENTEK)
    keresettDatum = argv[1].split('-')
    datumKeres(driver, keresettDatum)
    datum = datetime.datetime(int(keresettDatum[0]), int(keresettDatum[1]), int(keresettDatum[2]))
    kepKeszitese(KEPEKMAPPA, driver, datum, KOMMENTEK)

elif len(argv) == 1:
    bejelentkezes(EMAIL, JELSZO, driver, KOMMENTEK)
    kepKeszitese(KEPEKMAPPA, driver, datetime.datetime.now(), KOMMENTEK)

else:
    hasznalatiUtasitasok()

if KOMMENTEK:
    print("Program lefutott!")

driver.close()