## Beskrivning
kategori: Reversing / Övrigt
Svårighetsgrad:
- med mainframe erfarenhet: lätt
- utan mainframe erfarenhet: svår

Utmaningen här är miljön. allt du får är en fil som heter "extr_run.bin" (extract, run binary)
det är en binär som är packat i IBMs version av zip (typ) som du ska extrahera och köra för att få ut flaggan. 
binären är skriven i COBOL och kompilerad i COBOL MVT (kompilator från 70 talet) på MVS 3.8 / OS/370 operativsystemet från 70 talet.

det kommer i princip vara omöjligt att göra något med denna fil utanför den korrekta miljön.
(EBCDIC, annan arch, annat set av maskininstruktioner etc etc)

det är inget som är svårt i sig med att flytta öven en fil till miljön, extrahera den och köra den. 
det svåra är som sagt att veta hur man ens tar sig runt i miljön och hur man gör saker i den. 
allting går att googla fram om man är specifik och vet vad man ska googla efter. 

man kommer att bli exponerad för JCL (Job controll language) men det går att googla exempel. 

## återskapa utamningen
För eran sinnesro så hoppas jag att ni inte tappar bort binären men om så skulle vara fallet så...
i The Legacy/annat/ så finns det en uppsatt vm med source och compile JCL. extrahera den (BuildVM.tar.gz)
och snurra upp samt logga in som HERC02 (viktigt med usern...). pw: CUL8TR
submitta 'HERC02.TEST.JCL' så landar binären i HERC02.TEST.LOADLIB(ACCOUNTS). 
Packa den genom att submitta SYS2.JCLLIB(TRANSBIN) så landar den packade binären i HERC02.XMIT.OUTPDS. 
sen skickar man filen via send/receive (obs! från command line) i binary mode. 
tappar ni bort buildVM så kan man köra från en baseVM och skicka upp filerna cobjcl.txt samt XMITOUT.TXT till VMen (på samma sätt som ovan) och submitta dem.

## steg för att lösa
1. starta miljön (./mvs i emulator foldern)
2. ladda ner en TN3270 emulator för att connecta till miljön (finns flera st. pick one), exempelvis pw3270 eller x3270
3. logga in med default creds som är uppsatta i tur(n)key4 (usr=HERC01, pw=CUL8TR)
4. flytta över filen till miljön. detta är lite beroende på vilken 3270 terminal man använder. 
   för pw3270 så är det send/receive. den kan även allokera filen korrekt direkt i flytten (inte alla kan det)
   det viktiga här är RECLEN = 80, BLKSIZE = 80, RECFM = FB
   samt att output filen är omgiven av ''. ex 'herc01.test.xmitin'
   OBS! två saker att notera. 
   1) du måste stå på command line i miljön innan du skickar upp filen. snabbkommando "1.3.6" när man loggat in
   2) i princip så kan saker i miljön inte ha mer än 8 tecken i sig...  
5. gå in till SYS2.JCLLIB och skapa ny fil "S filnamn" i kommandoraden
6. skriv "COPY RECV370P" i kommandoraden
7. ändra följande:
   //             MSGCLASS=D,
   och
   //XMIT370 PROC XMI='var du skickade din pakade fil till',  (ex 'HERC01.TEST.XMITIN')
   //             PDS='var du vill att filen ska hamna',      (ex 'HERC01.TEST.LOADLIB2')
   samt 
   //             DCB=(LRECL=0,BLKSIZE=&BLK,DSORG=PO,RECFM=U), LRECL ska vara 0 och RECFM ska vara U.
   ta bort allt under samt kommateckenet i:
   //RECEIVE  EXEC RECV370, 
7. tryck enter för att spara och sen skriv SUB i kommand line för att submitta jobbet. 
8. om du inte fick några fel kommer binären att extraheras till specat ställe. binären heter ACCOUNTS
9. dags att köra programmet. skapa en ny fil i JCLLIB (S RUNNER)
   och skriv in följande:
   //HERC01R JOB  (SETUP),
   //             'TEST COBOL',
   //             CLASS=A,
   //             MSGCLASS=D,
   //             MSGLEVEL=(1,1)
   //*
   //STEP001   EXEC PGM=ACCOUNTS
   //STEPLIB   DD DSN=HERC01.TEST.LOADLIB2,DISP=SHR
   //SYSOUT    DD SYSOUT=*
   //SYSABEND  DD SYSOUT=*
   
   OBS! kopiera inte utan skriv manuellt för att undvika huvudvärk
10. tryck enter för att spara och sen SUB på kommandoraden. går allt bra får du flaggen i outputten. 
11. titta på outputten. 3.8 (utilites. outlist)
   s framför ditt jobb och page down tills du ser flaggan! 
