## LCG RSA

# publik beskrivning
Kan du faktorisera 1024-bit tal?
Annars får du aldrig flaggan.

# ledtrådar
ledtrådar som kan släppas om det behövs:
hur genereras primtalen? # denna ledtråd pekar en i rätt riktning på var svagheten ligger
finns det någon relation mellan primtalen? # denna ledtråd ger nästan svaret

# lösning finns i baby_dsa_solution.py
en RSA uppgift med svag RNG
de två primtalen p, q är relaterade via en enkel ekvation
tänkt lösning är att lösa ett envariabels polynom över 2-adics
kan lösa det med Henseläs lemma eller forcera varje siffra i bas 2 med BFS eller DFS

# svårighetsgrad: medel

# hur man modifierar uppgiften
hela uppgiften består av två filer, där en är pythonkoden och den andra output.txt
för att ändra flaggan ska skriptet köras om och stdout måste pipas till output.txt 
notera att flaggan i flag.txt måste vara mindre än 128 karaktärer i längd
