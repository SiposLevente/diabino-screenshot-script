# A program jelenleg tesztelés alatt áll!

# Tartalom
- [DiaBino-Screenshot-Script](#diabino-screenshot-script)
- [Script működéséhez szükséges előkövetelmények](#script-működéséhez-szükséges-előkövetelmények)
- [A Script működése](#a-script-működése)
- [Settings.ini](#settingsini)
  * [email](#email)
  * [jelszo](#jelszo)
  * [kepekmappa](#kepekmappa)
  * [kommentek](#kommentek)
- [WebDriverek](#webdriverek)
- [Plusz Tennivalók Linux és Mac rendszerelen](#plusz-tennivalók-linux-és-mac-rendszerelen)

# DiaBino-Screenshot-Script
Ez az alkalmazás lehetővé teszi, hogy a DiaBino oldalról az adatokat lementsük képek formájában.


# Script működéséhez szükséges előkövetelmények
Windows felületen Microsoft Visual C++, ezt [innen](https://support.microsoft.com/hu-hu/help/2977003/the-latest-supported-visual-c-downloads) le lehet tölteni

[Firefox](https://www.mozilla.org/hu/firefox/new/) vagy [Chrome](https://www.google.com/intl/hu/chrome/) böngésző

A webdrivert aszerint válasszuk ki hogy milyen böngésző van a gépünkre telepítve.

Webdriverek beszerezhetőek itt:

[Firefox webdriver (geckodriver)](https://github.com/mozilla/geckodriver/releases)

[Chrome webdriver (chromedriver)](https://chromedriver.chromium.org/downloads)

### **A webdrivereket a driver mappában abba az almappába helyezzük amilyen rendszerünk van (Windows=win, Linux=lin, Mac=mac)**

# A Script működése

A programnak 3 féle módja van
1. **diabinoScreenshot.py**

    A program bejelentkezik a DiaBinoba és a mai nap vércukor értékeit lefényképezi és elmenti a megadott mappába"
   
1. **diabinoScreenshot.py "ÉÉÉÉ-HH-NN"**

    A program bejelentkezik a DiaBinoba és a megadott dátumokhoz tartozó adatokat lefényképezi és elmenti a megadott mappába"

1. **diabinoScreenshot.py "ÉÉÉÉ-HH-NN" "ÉÉÉÉ-HH-NN"**

    A program bejelentkezik a DiaBino és a megadott intervallumon lévő napokhoz tartozó adatokat lefényképezi és elmenti a megadott mappába
 
 
 
 
Megfelelő dátum beviteli formátum: \"ÉÉÉÉ-HH-NN\" (pl:2020-07-27)

Beállítások a settings.txt fájlban találhatóak abban a mappában, ahol a maga a script található van.

# Settings.ini
A DiaBinoba való bejelentkezéshez szükséges adatokat ebbe a fájlba kell beleírni. Ezeken kívül még itt találjuk azokat a beállításokat is, hogy a készített képeket a script hova mentse, futása közben kiírja-e, hogy éppen mi történik 

## email
Itt kell megadni a bejelentkezéshez szükséges email címet, az email címet a valaki@valami.hu helyére kell írni.
```
email = valaki@valami.hu
```
## jelszo
Itt kell megadni a bejelentkezéshez szükséges jelszót, a jelszót a titkosJelszo helyére kell írni.
```
jelszo = titkosJelszo
```
## kepekmappa
Itt kell megadni azt, hogy a script hova mentse a készített képeket, ez alapértelmezett beállításként a script mappájában található Screenshots mappába menti.
```
kepekmappa = Screenshots
```
## kommentek
Itt lehet megadni, hogy a script a futása közben kommentálja, hogy éppen mit csinál. Ha ez igazra van állítva akkor a program kommentál. (1 = Igaz; 0 = Hamis)
```
kommentek = 1
```
## webdriver
Itt lehet kiválasztani hogy a program melyik webdrivert használja, olyan webdrivert használjunk mint amilyen böngésző van a gépünkön. Lehetséges értékek: "firefox", "chrome"
```
webdriver = firefox
```

vagy

```
webdriver = chrome
```

# WebDriverek
A webdriverek a driver mappában találhatóak.

Link a geckodriverhez: https://github.com/mozilla/geckodriver/releases

Link a chromedriverhez: https://chromedriver.chromium.org/downloads

# Plusz tennivalók Linux és Mac rendszerelen
A geckodriver/chromedriver fájlt a driver mappában futtathatóvá kell tenni. Ezt a következő parancsal tudjuk megtenni:
```
chmod +x geckodriver
```
```
chmod +x chromedriver
```
