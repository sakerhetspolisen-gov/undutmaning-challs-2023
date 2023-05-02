# Beskrivning
Ett virus som letar efter en fil vars innehåll matchar en specifik MD5, och infekterar den. När den infekterade filen körs kommer viruset dumpa orginalfilen till disk, exekvera den och sedan dekryptera en URL och ringa ut till en C2 server. URL:en är flaggan, och den kan bara dekrypteras om viruset har lyckats med infektionen.

# Bygge
1. Ändra på flag.txt till önskad flagga.
2. Kör `make vir`

# Story
Harald fick ett mejl med fantastiska recept bifogade som ett dokument - recept.doc.exe. När han öppnade filen verkade dock inget hända...

# Lösning
1. Reversa och förstå att viruset letar efter en fil med rätt MD5
2. Googla på MD5:an, och se att den matchar "emacs-28.2-installer.exe"
3. Ladda ner filen och placera i ~/Downloads
4. Kör viruset
5. Kör den infekterade filen med Wireshark eller liknande igång -> URL/Flagga
6. (Installera Emacs)

# Svårighetsgrad
Medel kanske?