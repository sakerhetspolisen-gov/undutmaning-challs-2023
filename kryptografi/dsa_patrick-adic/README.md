## dsa patrick-adic

# publik beskrivning
Jag har har implementerat DSA helt själv
Implementationen följer kryptografers rekommendationer, att k aldrig ska kunna återanvändas igen
För ökad säkerhet har jag dubblat antal bits i hashen och modulon

# ledtrådar
**P**atrick-**adic**
skapde min egna 1024-bit hashfunktion för det inte fanns någon annan

# lösning hittas i dsa_patrick-adic_solution.py
utmaningen är ett problem i talteori
det som efterfrågas är en lösning till den p-adiska logaritmen
går bara att lösa efter man utnyttjat `k = bytes_to_long(k + k)` från signeringsfunktionen

# svårighetsgrad: medel

# hur man återskapar utmaningen
uppgiften är två filer, pythonfilen och output.txt
för att ändra flaggan kör man om skriptet och måste pipa stdout till slutet av output.txt
notera att flaggans längd kan inte vara över 128 karaktärer i längd

det som ska laddas upp är dsa_patric-adic.py tillsammans med output från det programmet (chiffertexter)
om chiffertexterna klistras in i slutet av filen eller om det kommer med en till output.txt fil spelar ingen roll
