## Beskrivning
kategori: Reversing
Svårighetsgrad: lätt / medel

utmaningen kommer kräva att man patchar en kodrad i ex Ghidra. 
man får en hint om att det ska gå att få ut äppelskrutt efter ormen har ätit dem. 
äppelskutten har symbolen + vilket hintas om också i texten. 
äppelskrutten kommer att bilda flaggan när man spelat en stund.


## återskapa utamningen
compile.sh
- ```gcc snake.c -o snake ```
- ```strip snake ```


## steg för att lösa
för att få äppelskrutten att komma fram behöver man patcha en kodrad i ex ghidra 
där man ändrar ett asignment från 0 till 1. 

man får spåra var + användas och villka funktioner som är involverade. 
man kommer då se en variabel dycka upp på några ställen. 

variabeln har ett deklarationsvärde på 1 men sätts till 0 i main funktionen. 
denna ska patchas till 1 i main funktionen så att funktionerna som sparar 
och printar ut äppelskrutten träffas av koden (går ner i if statement). 

man skulle kunna ändra värdet i en debugger och detacha den efter 
man ändrat värdet i variabeln till 1.

Sen är det bara att spela spelet ett tag. 
Reversing krävs i bägge fallen. 

man kan ev få ut alla koordinater för äpplena från den 2 dimensionella int arrayen och printa ut dem allt i ett. 
