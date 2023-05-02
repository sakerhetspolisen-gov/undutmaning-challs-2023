# Beskrivning
Denna utmaning går ut på att forcera två algoritmer för att kunna återskapa flaggan.

# Bygge
1. Ändra på flag.txt till önskad flagga.
2. Kör `make flag && ./flag`.
3. Klistra in innehållet av stdout in i `main.h`.
4. Kör `make`.

# Story
För ett par dagar sedan fick Harald en lapp som det stod en halvförstörd flagga på. Harald råkade tyvärr glömma att han hade på sig lappen och använde därför degblandaren, vilket olyckligtvis ledde till att den hamnade i degen. Kan du hjälpa honom få ut vad den ursprungliga flaggan var?

# Lösning
Denna utmaning har två olika steg till sig. Det första steget är att analysera och förstå hur värderna sitter i arrayn och det andra steget handlar om att återskapa flaggans värde från dessa värden.

Steg 1:
Analysersa och komma fram till att varannat värde i arrayn placeras in slumpmässigt. Eftersom utmaningen använder sig av ett statiskt frö så kommer dessa positioner alltid att vara detsamma.

Steg 2:
Hitta och identifiera värderna, och kör därefter operationerna `(x2 - y2) - (x1 + y1)` för att få fram en karaktär i flaggan. Gör om för varje karaktär i flaggan. Givet ett scenario där man är på början av arrayn så är variablerna uppsatta på detta sätt: `x1` är `b[0]`, `y1` är `b[b[1]]`, `x2` är `b[2]` och `y2` är `b[b[3]]`.

Automatisk lösning:
Kör `make solve`.

# Svårighetsgrad
Lätt/medel med symboler, medel/svår utan.
