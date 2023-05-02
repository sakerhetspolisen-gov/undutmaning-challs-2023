# Discord Utmaning #1

Denna lösning baserar sig på [snekbox](https://github.com/python-discord/snekbox).
Användarens kod läggs till i slutet på nedan kod.

# Storyline

*Harald Von Schwarzwald* hade anlitat en skum programmeringsfirma som inte riktigt förstod säkerhetsnivån som Harald ville uppnå.

# Utmaning

Utmaningen är att få ut en "privat" variabel från en dataklass i Python.
Som känt finns det inte "true private variables" i python, men detta är ett försök till att emulera detta beteende trots allt.

```python
import inspect
import os
import dataclasses

@dataclasses.dataclass
class Vault:
    _flag: str = lambda val=os.environ['FLAGGA']: val if inspect.stack()[0].function == '<lambda>' and inspect.stack()[1].function == 'flag' and inspect.stack()[1].lineno == inspect.stack()[0].lineno+4 else None

    @property
    def flag(self):
        val = self._flag()
        if val != None:
            return f"{id(val)}"

secret = Vault()
del(os.environ['FLAGGA'])
# Här kommer användarens kod läggas in
```

Det är en lambda-funktion som kontrollerar vilket radnummer och funktionsanrop som försöker komma åt flaggan.
Du startar utmaningen lokalt genom att köra:
```bash
$ python script.py flag-goes-here
```

# Lösningar

Det finns tre kända lösningar.

## Lösning 1 - Lambda funktioner

Detta är den lättaste lösningen.
lambda-funktioner i Python lagrar sina frysta parametrar i den variabel som exponeras:

**python <3.11**
```python
print(secret._flag.defaults[0])
```

**python >3.11**
```python
print(secret._flag.__defaults__[0])
```

## Lösning 2 - Minnesaddresser

```python
import ctypes
var = 1
print(ctypes.cast(id(var)+717120, ctypes.py_object).value)
```

Minnessaddressens offset är olika från dator till dator, men kan forceras fram relativt enkelt.
Efter man hittat offseten så är det alltid samma.

## Lösning 3 - Magisk lösning

```python
from types import SimpleNamespace
inspect = SimpleNamespace(**{"stack": lambda: [SimpleNamespace(**{"function":"<lambda>", "lineno":0}), SimpleNamespace(**{"function":"flag", "lineno":4})]})

print(secret.flag)
print(secret._flag())
```

Denna lösning skapar ett objekt som `inspect` kan analysera där `.lineno` är manuellt satt till rätt nummer.
Detta kräver att deltagaren hämtar ut källkoden (vilket också går).

## Installera

Ändra `envar: "FLAGGA=` i `snekbox.cfg` som finns i `web/` rooten *(ja, dum placering)*.
Se till att `docker-compose` innehåller:
```yaml
    discord:
        image: docker.io/tiangolo/uvicorn-gunicorn-fastapi:python3.10
        command:
            - /bin/sh
            - -c 
            - |
              pip install --upgrade pip
              pip install --no-cache-dir --upgrade -r /app/app/requirements.txt
              python3 /app/app/bot.py
        restart: always
        environment:
            - DB_ADDR=db
            - DB_USER=undutmaning
            - DB_PASS=undutmaning
            - DB_NAME=undutmaning
            - 'DISCORD_SECRET=some.secret.key'
            - 'BASE_URL=https://undutmaning.se'
            - 'URL_PREFIX='
        volumes:
            - ./backend/api_undutmaning_se/:/app/app/:ro
        networks:
            default:
            db-internal:
            discord-internal:
    snekbox:
        container_name: snekbox
        hostname: snekbox
        privileged: true
        image: ghcr.io/python-discord/snekbox:2023.3.13.0
        ports:
         - "8060:8060"
        init: true
        ipc: none
        tty: true
        environment:
            SNEKBOX_DEBUG: 1
            PYTHONDONTWRITEBYTECODE: 1
        volumes:
            - ./gunicorn.conf.py:/snekbox/config/gunicorn.conf.py
            - ./snekbox.cfg:/snekbox/config/snekbox.cfg
            - user-base:/snekbox/user_base
        networks:
            discord-internal:
```

Sedan bör `backend/api_undutmaning_se/bot.py` starta och all `!code <kod>` som skickas till boten kommer evalueras i `snekbox` containern.