# Signalknas

## Beskrivning
Utmaningen går ut på att återskapa ett meddelande. Data för utmaningen är
strängar med fyra olika tecken, där varje tecken motsvarar två bitar. Varje
sträng är behäftad med felaktigheter som försvunna tecken, eller tecken som
ändrats.

Kategori: misc eller kanske krypto

## Återskapa utmaning
Scriptet kräver att några program är installerade:
`apt install clustalw emboss`.

Kör script enligt:
```
./signalknas.rb N FLAG > utmaning-input.txt
```
där N är antal meddelanden och FLAG är flagg-strängen, tex:
```
./signalknas.rb 128 "flagga{en liten testflagga}"
```
I samband med att data skapas för utmaningen, försöker scriptet även lösa den.
Det är inte alltid det går, och då skrivs ett felmeddelande ut till STDERR.
Prova igen, om det inte går efter flera försök, justera antal meddelanden
och/eller längden på flagg-strängen.

## Storyline
Förslag (fritt att ändra!):

### Signalknas: Genialisk analys underlättar.

Det har blivit något knas i etern när Harald beställde lite råvaror till sitt bageri. Samma meddelande har skickats många gånger men det blir ändå fel - går det att knåda ihop det? Hjälp! Skriker Harald.. Här kan det vara bra att vara lite genialisk.

## Steg
För att lösa denna utmaning bör man först försöka återskapa rätt
meddelandesträng. Genom att inse att varje rad i input är ett och samma
meddelande, men att en del tecken saknas eller har ändrats, så kan man få fram
den korrekta meddelandesträngen. Ett sätt för att åstadkomma detta är att
använda verktyg från bioinformatik, där man ofta hanterar snarlika strängar med
4 olika tecken (närmare bestämt A, T, G, C som betecknar DNA-baser - därav
ledtråden om genialisk analys i titeln).

Därefter kan man klura ut hur meddelandet är inkodat. Eftersom innehållet
endast har 4 olika tecken, kan man inse att det borde vara två bitar per
tecken. Om man provar samtliga möjliga mappningar och tolkar som ascii med fyra
bitar per tecken, kan man se att en av dem ger flaggan.

## Lösning
`cat input.txt | ./signalknas.rb -s`
Lösnings-scriptet kallar på programmen 'clustalw' och 'em_cons' för att
återskapa korrekt signalsträng, därefter skrivs alla möjliga mappningar ut.
Notera att lösningen inte lyckas varje gång, så man kan behöva köra
lösningskommandot flera gånger.

## Svårighetsgrad
Medel.


