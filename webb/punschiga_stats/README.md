# Webbutmaning - Punschiga Stats
Peter Punsch håller full koll på sin fina server. Kom ihåg att hans filer är hans och ingen annans!

## Skapa utmaning
1. Lägg korrekt flagga i variabeln `FLAG` i filen `app/app.py`.
2. Bygg Docker container: `docker build . -t punschiga-stats`.
3. Kör utmaning: `docker run --rm -p 5000:5000 punschiga-stats`. 

## Mål
Få flaggan genom att logga in med korrekt creds på `/dev-admin-sida`.

## Lösning
1. Läs ut sqlite databasen: `http://<ip:port>/api/stats/fd/3`.
2. I databasen finns URL-path och creds till adminsidan.
3. Väl inloggad på `/dev/admin-sida` med creds `peter:jEdIw0Kdw249Kd3SDfjIww4`.