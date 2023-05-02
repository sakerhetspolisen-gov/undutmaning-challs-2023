## 2x shuffle

# publik beskrivning
Detta är en black-box reverse/crypto uppgift
Kommunicera med servern över TCP och lista ut vad den gör för att dekrypotera flaggan
`nc <server ip> 1337`

# ledtrådar
Vilka längder på inputs accepterar servern och vad är längden av output?
Får samma input alltid samma output?
Hur ändras output om en byte i input ändras?

## lösning
en utmaning för nybörjare
uppgiften är en black box reverse. en service som läser en sträng som input och returnerar en sträng av samma längd där alla bytes har substituerats och positioner permuterats
deltagare ska nå tjänsten över tcp. exempelvis med `nc server_ip 1337`

det första servern skickar är en krypterad flagga
sedan frågar den efter input att kryptera. genom att testa sig fram bör man tidigt se ett mönster, alla bytes substitueras och permuteras men det är alltid deterministiskt
man måste beräkna två saker, substitueringen av bytes och permutationen
först för substituering, det är alltid samms substitution för varje byte oberoende av position
substitueringen kan forceras genom att testa alla printable asciikaraktärer
när man vet substitutionen kan man enkelt beräkna permutationen genom att skicka en sträng av unika karaktärer och se var deras substitution hamnar i position
nu är alla okända variabler kända. ta inversen av substitutionen och permutationen för att avkryptera flaggan

# Svårighetsgrad: lätt

# Steg för att återskapa utmaningen
all konfiguration finns i mapp `container`
den här uppgiften kräver nätverksåtkomst för att fungera
portnummer kan ändras i xinetd_config
flagga kan ändras i flag.txt
ingen fil ska laddas upp, enbart publik beskrivning
