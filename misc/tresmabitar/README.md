# Beskrivning
<details>
  <summary>Spoiler warning</summary>
En enklare utmaning där man ska återställa en "korrupt" fil. Utmaningen kräver även att man förstår sig på viss funktionalitet i komprimeringsformatet zstandard.  
  
Zstandard har en funktion som kallas "dictionary" där man kan separera uppslagsverket (som används för komprimeringen) från den komprimerade filen.  
  
Filen har blivit korrupt genom att 3 bitar i fältet "Dictionary_ID" har ändrats (se https://github.com/facebook/zstd/blob/dev/doc/zstd_compression_format.md#dictionary-format) och zstd vill inte avkomprimera filen om dictionary ID inte är samma i dictionaryn och den komprimerade filen. 
  
Kommandot "file" visar dictionary ID på varje fil.  

T.ex. startar dictionary ID (4 byte) i (räknat från noll) position 4h i ordboken, och position 5h i den komprimerade filen.
</details>

Filerna "recept.ordbok" och "recept.hemligt" ska användas i CTFen.

# För att återskapa:
## Komprimering
Träna en "dictionary" baserad på diverse gamla kokböcker hittade på Project Gutenberg.  
t.ex. `zstd --ultra -20 --train books/* -B64 --maxdict=13337 -o bitflip/recept.ordbok`

för att komprimera filen recept.txt med filen recept.ordbok  
`zstd --ultra -20 -D recept.ordbok ../recept.txt -o recept.zstd`

## Avkomprimera
`zstd -d -D recept.ordbok recept.zstd -o recept.uncompressed.txt`

# Story
Titel: Tre små bitar
Svårighetsgrad: Lätt

Ibland händer det att vi på Säkerhetsbageriet stöter på nya bakelser.
Alla nya bakelser behöver analyseras djupgående och det görs enklast med hjälp av originalreceptet.

Gustav Giffel var nere på bageriet för att hämta receptet men råkade i förbifarten köra sitt statligt utförda USB-minne RAKT ner i en nybakad *zeppola*! Katastrof!
Konstapel Giffel blev utkastad och som grädde på moset verkar datan på USB-minnet blivit korrupt på något vis. Kan ni hjälpa oss?

# Flagga
undut{hbiBTdXJkZWchIEhhbiBmbHlyIGbDtnJtb2RsaWdlbiBtb3QgZGFubWFyayBkw6Ug}

# Övrig info 
https://github.com/facebook/zstd/blob/dev/doc/zstd_compression_format.md#dictionary-format
https://en.wikipedia.org/wiki/Zeppole
