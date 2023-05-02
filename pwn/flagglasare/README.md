# Beskrivning
Detta är en utmaning som går ut på att komma förbi en check som sker på en global variabel.

# Bygge
Kör `dotnet build -c Release` eller `dotnet run -c Release` i denna mapp.

Observera att `Dockerfile.jail` samt `flagglasare.csproj.jail` ej kan användas utan modifikation, då utmaningen kräver att /tmp delas mellan xinitd-anslutningarna

# Story

# Lösning
1. Öppna en instans av utmaningen.
2. Anteckna ner det GUID som du får.
3. Klicka på menyval 2, det vill säga, "Bli flaggläsare".
4. Öppna ännu en instans av utmaningen. Var noga med att inte stänga den gamla.
5. Ange menyval 1, det vill säga, "Logga in som annat GUID".
6. Mata in det GUID du antecknat.
7. Ange menyval 3, det vill säga, "Få flagga".

# Svårighetsgrad
lätt