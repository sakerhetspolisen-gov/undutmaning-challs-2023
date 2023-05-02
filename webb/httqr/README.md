# CTF: httqr

## Kort beskrivning

Den onde Evil Cake Genius har gömt information om en hemlig ingrediens. Man
startar med en Onion-adress och får använda sig av lite allmän webbkunskap,
förmåga att läsa lite programkod samt använda lite kommandoradsverktyg
gentemot TOR-nätverket.

## Svårighetsgrad

Medel

## Att driftsätta

### Förberedelser

Utöver den lokala driftsättningen måste en del ytterligare förberedelser göras.
Inför CTF23 är detta dock redan gjort.

### Plattformskrav

 * Verifierad på Debian 10.

 * Kräver Docker och docker-compose. Nyare versioner av Docker har kommandot
`compose` inbyggt.

### Installation

 1. Checka ut repot till katalogen `/root/httqr`.

 1. Kör scriptet `setup.sh`. Notera att exekveringen avslutas med att startpunkten
    för utmaningen skrivs ut.

        $ /root/httqr/setup.sh

 2. Testa att starta tjänsten

        $ docker-compose build && docker-compose up; docker-compose down

 3. Kopiera in service-filen till systemd-katalogen, aktivera den och starta
    den

        $ cp httqr.service /etc/systemd/system/.
        $ systemctl daemon-reload
        $ systemctl enable httqr
        $ systemctl start httqr

 4. Använd en TOR-browser för att surfa till de adresser som anges i filerna
    `tor/services/alpha/hostname` och `tor/services/bravo/hostname`. Just första
    anropet kan ta lite tid, så det är bra om det är du och inte en användare
    som råkar ut för timeouts.

Not 1: Om du behöver köra om `setup.sh` så kan du först behöva rensa bort de
filer som tidigare skapats genom att köra `setup.sh clean`

Not 2: Startadressen för utmaningen ligger i filen `tor/services/alpha/hostname`.

Not 3: Om du installerar till en annan katalog än `/root/httqr` behöver du
redigera service-filen.

Not 4: Om kommandot `docker-compose` inte fungerar utan man måste använda
`docker compose` behöver du redigera service-filen.

## Storyline

Den onde Evil Cake Genius har gömt information om en hemlig ingrediens.

## Lösning

Startpunkten är en onion-adress. Använd en TOR-kompatibel browser
för att följa URL:en. Äldre webbläsare (t.ex. vissa versioner av
Brave) klarar inte av den nyckelstandard som används.

Sidan du kommer till anger helt enkelt "This is not the site
you are looking for". Tricket här är att titta på certifikatet (i
sidans html-kod finns tipset "See TLS data").
Det kan hända att du får en certifikatsvarning på väg till sidan,
vilket ger dig en god möjlighet att undersöka certifikatet. Nyare
versioner av TOR Browser godtar dock självsignerade certifikat,
vilket då gör saker lite krångligare, men du kan använda torsocks
och openssl för att få ut certifikatet:

    $ torsocks openssl s_client -connect <address>.onion:443 | openssl x509 -noout -text

Certifikatet är självsignerat, vilket man bland annat ser på att
Issuer och Subject har samma information. I det här fallet är
informationen en adress till ett bageri i USA.  En sak som
sticker ut är att e-postadressen ligger på domänen "github.com".
Om du surfar till https://github.com och söker så hittar du
ganska enkelt ett användarkonto och ett repository.

Dokumentationen för projektet innehåller referens till en RFC. Om
man googlar ser man att det är specifikationen för X509, alltså
standarden för certifikat. Siffrorna som följer efter RFC-numret
är en sektion i dokumentet som handlar om "Subject Alternative
Name". Tittar man åter på certifikatet man hämtade från Onion-sajten
ser man att det under Extensions finns en Subject Alternative Name-sektion
(kan också benämnas "subjektAltName", precis som anges i RFC:n). Den
innehåller ett par entries märkta "DNS:". Det ena är helt enkelt
onion-adressen, men det andra är en lång hexadecimal sekvens.

Om man fortsätter titta runt i github-projektet så hittar man en
ensam Python-fil. Den innehåller bl.a kod för hur man gör om en nolla
respektive en etta i en bitmap till en stor pixel. Man kan nu
också titta på projektnamnet, "msb7bitpad33x33", och eventuellt
räkna ut att 7+33*33=1096 bitar, vilket är 137 bytes, vilket är
exakt så lång som hexadecimalsekvensen man hittat är. Man kan
då skriva ihop ett litet Python-script som tar denna sekvens,
hoppar över de första 7 bitarna, gör om övriga bitar till ASCII-
pixlar och skriver ut de med 33 pixlar per rad i 33 rader.

Ett enklare sätt är dock att upptäcka att github-projektet har
en branch, där ett färdigt script finns tillgängligt. I dokumentationen
för branchen påpekas att man kan ändra konfigurationskonstanter i
koden. Om man testar att ändra de versala variablerna i toppen av
filen så får man ganska snart ett användbart resultat.

Om man skriver ut de sista 1089 bitarna i hexadecimalsekvensen
som ASCII-pixlar i 33 rader med 33 pixlar per rad så får man
fram en QR-kod, vilken innehåller en ny URL, bestående av en
onion-adress och pathen "/java".

Surfa till den nya URL:en. Resultatet blir en sida som anger
"Status code: Unable to serve requested product".

Tanken är här att man ska öppna Utvecklarläge i sin webbläsare
och leta rätt på den statuskod man fick, vilken är 418. Det här
är en standardkod men väldigt speciell, och betyder "I am a
tea pot". Detta, tillsammans med information "Unable to serve
requested product", får den uppmärksamme att ändra path i URL:en,
från "/java" till "/tea". När man surfar till denna URL så
blir man redirectad till pathen "/cookie", och en bild med
kakor och/eller kakburkar och information om att man gått för
långt.

Nu går man tillbaka till Utvecklarläget och ser att när man
surfade till "/tea"-pathen så fick man en kaka som innehåller
"do_redirect=true". Om man ändrar denna cookie till
"do_redirect=false" och åter surfar till "/tea"-pathen så
skickas man inte vidare, men får meddelandet
"Misdirected when repeatedly redirected: some redirections are
good".

Om du sätter om kakan till "do_redirect=false" (eller tar bort
kakan helt och hållet) och åter surfar till "/tea"-pathen så
kan du i Utvecklarläget se att du blir redirectad inte bara
en utan två gånger: först till en path med ett ganska konstigt
namn, och först därefter till den URL som har kakbilden. Sätt
nu kakan till "do_redirect=false" och surfa till den URL som du
först blev redirectad till. Du hamnar då på en sida med bilder
på tårtor och meddelandet "Fix the script, pick the flag".

Om du tittar på källkoden till sidan så finns där ingen
scriptkod, men några .js-filer importeras. De flesta är
standardfiler, men en heter "cakes.js". Du kan använda
Debugger-läget i Utvecklarverktyget för att titta på
innehållet i filen. Förhoppningsvis hittar du ganska snart
att den innehåller ett POST-anrop till path `/cakeview` med
JSON-objektet `{"include_flag": false}`.

Det kan vara lite klurigt att ändra scriptet så att `true`
skickas. Ett sätt är att återigen använda torsocks, nu med
curl.

    # torsocks curl -X POST <adress>.onion/cakeview -H 'Content-Type: application/json' -d '{"include_flag": true}' -o flag.json

Man får då ner en JSON-fil som specar värdet på `src`- respektive
`title`-attributen för `<img>`-taggar. Ett av värdena stickar
ut, eftersom det inte är ett URL-referens utan ett rent Base64-värde.
Man kan base64-avkoda värdet till en binärfil. Ett annat alternativ
är att man stoppar in det i en ny, minimal HTML-fil:

    <html><body><img title="Unzip me" src="data:image/gif;base64,..."></body></html>

I en webbläsare kan man då högerklicka på bilden och spara ner den.

Man fick ett tydligt tips tillsammans med bildens källinformation: `Unzip me!`.

Det man behöver göra är nu att packa upp bildfilen med unzip:

    $ unzip <filnamn>

Man kommer då avkrävas ett lösenord. Man får ett tips om att använda
en zip-kod (om man inte får tipset vid lösenordsprompten kan man köra
`strings`-kommandot på filen). Förhoppningsvis kommer man ihåg att
certifikatsfilen man
läste i början av flaggjakten innehöll en "zip code" ("Zone Improvement
Plan code", dvs amerikanskt postnummer) som en del av adressinformationen
till Issuer och Subject. Anger man den koden så packas zip-filen upp till
två filer. Den ena filen man får ut specificerar att den inte innehåller
flaggan, medan den andra säger motsatsen, och innehåller det flaggvärde
som är specat i filen `flag.txt`.

## Extrainformation

### Github

Man behöver skapa ett konto på github, och där skapa ett repository. Man ska
där lägga in kod i main trunk samt i en branch. Se information i `github`-
katalogen. Namn på konto och repository måste stoppas in i filen `bin/setup.conf`
för att användas när kommandot `setup.sh` exekveras.

### Zip-kod

Den kod som ska användas för att kryptera flaggan, och som ska skrivas in i
certifikatet, behöver anges i filen `bin/setup.conf` för att användas när
kommandot `setup.sh` exekveras.

### Evil Cake Genius

Evil Cake Genius var ett enmansföretag i Minneapolis som drevs av Robin Lynn Martin.
Det verkar ha varit aktivt fram till 2021. Därefter startade Martin företaget Gateaux, Inc.,
som har en mer uppdateras webbsida än `https://evilcakegenius.com`. Dessutom så är det
telefonnummer som anges som kontaktinformation för Evil Cake Genius listat på
Gateux, Inc.

### Robert Hansen

Robert Hansen var känd som The Butcher Baker. Han var en respekterad bagare i Alaska samt
en serimördare aktiv i över ett decennium innan han åkte fast.

