 # Retrotiles
 
 ## Beskrivning
 Retrotiles är ett online-spel som körs i en webläsare. Flera spelare kan
 ansluta samtidigt. Utmaningen är att hitta två flaggor. Den enklaste flaggan
 får man genom att få sin figur i spelet att besöka skattkistan. Flagga två
 erhålls om man lyckas besegra Cthulhu.
 
 Kategori: web
 
 ## Återskapa utmaning
 Uppdatera flaggsträngarna i Dockerfile och starta servern.
 
 ## Storyline
 Bagare som använder margarin istället för smör hamnar i ett parallellt
 universum. För att kunna återvända måste de både finna skatten och besegra
 Cthulhu. Cthulhu kan dock endast besegras om man har ett **magiskt** svärd,
 typ.

 ### Beskrivning
 1: Storbagaren Jon Sigmarsson råkar använda margarin istället för smör i en baktävling och hamnar i ett parallellt universum där Döden hotar. Innan Jon återvänder, vill han komma åt skattkistan. Skynda och hjälp honom så att han inte hamnar i bakvattnet!

 Du hittar Jon på ip:port.
 2: Storbagaren Jon måste besegra Cthulhu för att kunna återvända. Cthulhu kan dock inte besegras med ett vanligt svärd, utan det måste vara magiskt, typ. Hjälp Jon skyndsamt innan den hala protoplasman i portalen smälter för gott!

 ## Steg för att lösa
 Båda flaggorna kan hittas med hjälp av webläsarens konsoll. För flagga 1 måste
 man ta sig till skattkistan, som finns i ett avspärrat område av kartan. Genom
 att uppdatera variablerna för spelarens position, kan man ändå nå dit:
 ```
 this.game.player.x = 270;
 this.game.player.y = 485;
 ```
 När spelaren befinner sig i sammar ruta som skattkistan, visas flaggsträngen på
 skärmen.
 
 För flagga två behöver man lura servern att spelaren har ett magiskt svärd och
 sedan gå till monstret Cthulhu.
 
 För att lösa flagga två bör man göra en s.k. javascript prototype injection i
 funktionen som skickar spelar-info till servern:
 ```
 this.game.player.info = function() {
    const p = this.game.player
    return({name: "haxor 123", health: p.health, x: p.x, y: p.y, dir: p.dir,
       frame: p.frame, charno: p.charno, tile: p.game.map.getTileCoord(p.x, p.y),
       cthuluEncounter: true, items: '__proto__,{"MagicalSword":true}'
 })
 }
 ´´´
 Efter att ha ändrat funktionen enligt ovan, erhålls flaggan när spelaren
 träffar på Cthulhu.
 
 ## Svårighetsgrad
 Flagga 1: lätt.
 Flagga 2: medel.
