# Webfont

Denna lösning baserar sig på en hemmagjord font.
Den byter plats på väl valda tecken som gör att en vanlig mening blir en flagga.

*Exempel:*
`drabba dig!` -> `flagga{hej}`

Ett verktyg för att skapa en font är https://www.calligraphr.com/

# Storyline

TBA

# Utmaning

Konto-sidan innehåller en dold font som heter "inbakad.woff".
Sidans standard-font är dock `Cairo` vilket döljer flaggan.

# Lösning

Byter man ut `Cairo` mot `inbakad` som font för alla element *(under `* { font-family: ...}`)* så ersätts meningarna på sidan till huller och bullar, men en mening står ut.
Och det är `flagga{<värde>}`.
