# Beskrivning
Detta är en utmaning som går ut på att reverse:a en chattapp för att kunna hitta ett par artifakter.

# Bygge
Självaste challengen är en diskdump av en riktig Android-mobil med appen installerad, och en konversation inspelad. 

# Lösning
1. Ladda ner .7z eller .zipfilen som innehåller dumpen av Androidsystemet.
2. Hitta dig till data/app/com.cryptchat och kopiera över base.apk någonstans.
3. Unpacka base.apk och kom fram till att RC4 används och att artifacter lagras i internal och external storage.
4. Navigera till /sdcard/Android/data/com.cryptchat/files för att hitta den krypterade chattloggen.
5. Navigera till /data/com.cryptchat/cache för att hitta den cache:ade RC4-nyckeln.
6. Avkoda bas64:an som finns i chattloggen, och applicera därefter RC4 med nyckeln från cachefilen.

# Svårighetsgrad
medel-
