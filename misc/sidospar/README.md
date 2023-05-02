# Sidospår

:warning: Detta är den gamla versionen av utmaningen och dess beskrivning.

## How to build

Run to build image

```docker run --rm -v $(realpath .):/work -w /work -u $(id -u):$(id -g) docker.io/rust:latest cargo build --release```

## How to run

Run image with
```docker run --rm --name misc-chall -v $(realpath target/x86_64-unknown-linux-gnu/release/challenge):/challange -p 8000:2323 -it debian:latest /challange```

Find the IP of container using (look for the MiscChallenge container)

```docker network inspect bridge```

## Sections:

<ol> <li>En `README.md` som beskriver:</li>
 <ol>
 <li>Övergripande beskrivning av vad det är för utmaning</li>
    Det går ut på att man via en remote uppkoppling kan med hjälp av fel i implementationen i koden kunna ta fram lösenordet enbart via en TCP uppkoppling.

 <li>Steg för att återskapa utmaningen (gärna scriptform)</li>
    Se ovan 'How to build' och 'How to run'
 <li>Storyline (ta hjälp av HR för att kontakta ansvarig för story)</li>
    Harald har hittat ett utländskt kassaskåp vars lösenord verkar vara för långt för att gissa. Kan du hjälpa honom att låsa upp kassaskåpet?
 <li>Beskrivning av stegen i utmaningen</li>
    Man ansluter via en TCP anslutning till port 2323 på containern, därifrån ska man försöka ta fram lösenordet, man bör inte få tillgång till binären eller källkoden direkt. Man rekommenderas att scripta upp det här i python men går i teorin att lösa det via netcat.
 <li>Lösningar, gärna ett flertal (eller script för att lösa)</li>
Get the IP address and use the solution.py, (replace 127.0.0.1 with the new IP of the docker container).
Få Ip addressen via att köra solution.py, byt ut 127.0.0.1 i scriptet med IP:n som är på den körande docker containern.

Se IP:n med :

```docker network inspect bridge```

Lösningen är strängen: YeThisIsTheFlag!
Man kan verifiera detta med

```nc <IP of docker container> 2323```

och sen skriva in lösenordet.

Stegen är i princip dem följande:
<ol>
<li>Sätt ihopp ett script för att testa olika längder som inputs</li>
<li>Notera att 16 längden är den enda som ger ett längre svar (1 sekund per försök), early-exit på alla andra längder.</li>
<li>Försök med längd 16, notera att icke ASCII-tecken ger en varning om att de inte är tillåtna</li>
<li>Notera att längd det är i princip enbart ifall man har icke-ASCII i början som ger varningen.</li>
<li>Inse därifrån att man utvärderar från vänster till höger i strängen med en exit ifall man stöter på ett icke-ASCII tecken eller fel bokstav.</li>
<li>Fyll en sträng med icke ASCII sen sätt in möjliga ASCII-tecken på första indexet tills man får en varning om att det inte är ASCII, då vet man att första tecknet är rätt</li>
<li>Fortsätt med nästa tecken tills man får varningen, tillslut så får man fram hela strängen tack vare varningen om att det är ASCII-tecken.</li>
</ol>
 <li>Svårighetsgrad *(uppskattad)* på utmaningen (lätt, medel, svår)</li>
 Lätt
 </ol>
 <li>En färdig binär/fil/docker-compose om utmaningen kräver det *(1.2 gäller fortfarande)*</li>
 Se ovan för att köra dockerfilen
 <li>En `flag.txt` med ett flagg-värde, format: `flagga{[a-Az-Z0-9\-._ ]+}`. Det är detta värde som läggs in</li>
   Se flag.txt
 </ol>
