<div align="center">
    <h1>Modrinth.py 🧪</h1>
    <h2>⚠️ WIP</h2>
    <img width="64px" alt="icon" src="./modrinth.svg">
</div>

About:
---
Asynchonous **Labrinth API** (v2) wrapper: https://docs.modrinth.com/ <br>
Supports basic ratelimiting via https://github.com/mjpieters/aiolimiter <br>
Has poor error handling (Better than nothing)

Usage examples:
---
[Nothing here for now, only dev tests](https://github.com/DrugsNotIncluded/modrinth.py/blob/main/main.py)

Basic usage:
---
```python
from modrinthpy import ModrinthClient

async def main():
    try:
        client = ModrinthClient()
        response = await client.Projects.get_multiple_projects(ids=['create','sodium'])
        print(response)
    finally:
        client.close()
```

Supported Labrinth API "parts":
---
- [x] Projects **(Full support, search included, more examples in https://github.com/DrugsNotIncluded/modrinth.py/blob/main/main.py for the moment)**
- [ ] Versions
- [ ] Version Files
- [ ] Users
- [ ] Notifications
- [ ] Threads
- [ ] Teams
- [ ] Tags
- [ ] Miscellaneous

TODO:
---
- [x] Rewrite abstract class for http client
- [ ] Adjust rateliming
- [ ] Add better Facet class

Similar projects:
---
* https://github.com/betapictoris/modrinth.py - Unfortunately incomplete, synchronous, doesn't have ANY error handling and ratelimit handling
* You always can use Python OpenAPI client generator from official specs