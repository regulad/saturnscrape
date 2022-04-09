# saturnscrape

Scrapes information from https://saturn.live, a collaborate school scheduling system.

Currently, this Python package only aims to support the scheduling and members of a school.

## Example

```python
from asyncio import run
from typing import cast

from saturnscrape import *


async def runner():
    client = SaturnLiveClient("jwt", "refresh token")
    print(cast(FullStudent, await client.get_student("me")).phone_number)
    await client.close()
    

run(runner())
```

Also provides a simple command line tool for downloading the schedule and members of a school to vCard and vCalendar/iCalendar files.
