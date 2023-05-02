# Lactose industries research lab

# Notis från tävlingsledning
Där blev ett fel i denna utmaning, "/model_top_secret" i robots.txt var inkorrekt då orden stod i fel ordning.

Level: Hard

## Beskrivning

I denna CTF ska man ta sig in på ett hemligt forskningslabb med hjälp av ett foto-ID. Måste vi leta rätt på en person som har access för att sedan stjäla personens foto-id, eller kan vi ta oss in genom bakdörren?


## Flaggan

undut{Z2FybmEgaGFyIHVuZGVyIHRpZGVuIGthbGxhdHMgaW4gb2NoIGRvbSBhbmzDpG5kZX}

## Story

Den världsledande laktosproduktstillverkaren Lactose industries har tagit in en AI vid namn Al som hanterar allt från content till autentisering. Företagets topphemliga receptlabb är det senaste tillskottet i AI-utvecklingen. Men är implementationen helt rätt gjort? Hur bra fungerar robotar och AI:n tillsammans?


## Lösning

Det finns vad jag kan se minst två potentiella lösningar till problemet. Testar man att logga in i forskningslabbet så inser man att det krävs ett ID i form av en bild. När man laddar upp en bild av rätt storlek och typ (jpg,jpeg,png) så får man ett svar på sidan hur lik bilden är den bilden vi söker. Vi får också en ledtråd, i form av att bilden är x% lik klass 100. Kollar man in robots.txt så ser vi att det gömmer sig en hemlig modell. Vi kan då välja ett av två steg: 
1) Antingen att tanka hem modellen och låsa modellen med dess vikter. Givet att vi då vet vad output ska vara (klass 100) så kan vi skicka in en bild och manipulera denna med brus i ett antal iterationer tills vi når 80% likhet. 
2) Istället för att joxa med maskininlärning kan vi notera att det är klass 100 som söks. Om vi gör en liten eftersökning på modellen så ser vi att den är tränad på ImageNet1000, som innehåller 1000 klasser. Dessa klasser finns specificerade och klass 100 är svarta svanar. Alltså räcker det med att ladda upp en svart svan för att ta sig igenom.  

## Driftsättning

Kör ./start.sh. 



