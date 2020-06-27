# Még tesztelés alatt

# DiaBino-Screenshot-Script
Ez az alkalmazás lehetővé teszi, hogy a DiaBino oldalról az adatokat lementsük képek formájában.

# A Script működése

A programnak 3 féle módja van
1. diabinoScreenshot.py

    A program bejelentkezik a DiaBinoba és a mai nap vércukor értékeit lefényképezi és elmenti a megadott mappába"
   
1. diabinoScreenshot.py "ÉÉÉÉ-HH-NN"

    A program bejelentkezik a DiaBinoba és a megadott dátumokhoz tartozó adatokat lefényképezi és elmenti a megadott mappába"

1. diabinoScreenshot.py "ÉÉÉÉ-HH-NN" "ÉÉÉÉ-HH-NN"

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
