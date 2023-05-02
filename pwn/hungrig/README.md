# Utmaning: hungrig
En liten binär som gärna vill låta dig exekvera godtycklig kod men som är lite för glupsk..

## Skapa utmaning
Exekvera Python-skriptet `create_hungrig.py` som kommer att skapa binären `hungrig`.
Skapa filen `flag.txt` innehållandes flaggsträngen och lägg den i samma mapp som binären.

Skapa sedan en xinitd i en container och exponera bara binären.

## Mål
Exekvera kod och läs ut "flag.txt" från samma mapp.

## Lösning
Lösning finns i Python-skriptet `solve_hungrig.py`. Exekvera skriptet i samma mapp som `hungrig`-binären och verifiera att flaggsträngen 
skrivs ut till stdout.
