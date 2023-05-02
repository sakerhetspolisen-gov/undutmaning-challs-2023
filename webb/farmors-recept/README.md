# Webbutmaning - Farmors Recept
Farmor har sparat alla sina favoritrecept på sin hemsida - men den hemliga såsen vill hon inte dela med sig av..

## Skapa utmaning
Bygg Dockercontainer: `docker build . -t farmors-recept`
Kör containern: `docker run --rm -p 8443:8080 farmors-recept`

## Mål
Utnyttja en SQL-injektion för att läcka data från kolumnen "secret_sauce" i databasen vars innehåll är flaggan.

## Lösning
Lösningen finns i Python-skriptet "solve.py". Exekvera skriptet och verifiera att korrekt flagga skrivs ut.
