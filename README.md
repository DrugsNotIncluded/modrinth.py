<div align="center">
    <h1>Modrinth.py 🧪</h1>
    <h2>⚠️WIP, Unstable, structure will change drastically⚠️</h2>
    <img width="64px" alt="icon" src="./modrinth.svg">
</div>

About:
---
Asynchonous **Labrinth API** wrapper <br>
Supports basic ratelimiting via https://github.com/mjpieters/aiolimiter <br>
Has poor error handling (Better than nothing)

Usage examples:
---
[Nothing here for now, only dev tests](https://github.com/DrugsNotIncluded/modrinth.py/blob/main/main.py)

Basic usage:
---
```python
# The name and structure of the package is about to change dramatically, only use it if you really need it.
from modrinth.labrinth import ModrinthClient

async def main():
    try:
        client = ModrinthClient()
        response = await client.Projects.get_multiple_projects(ids=['create','sodium'])
        print(response)
    finally:
        client._labrinth_client.close()
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
- [ ] Adjust rateliming
- [ ] Rewrite abstract class for http client
- [ ] Add better Facet class