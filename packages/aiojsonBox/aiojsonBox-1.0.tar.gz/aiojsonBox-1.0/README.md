# jsonbox-python


# how use
```python
import asyncio
from aiojsonbox import JsonBox


    async def main():
        s = JsonBox()
        print(await s.create_box(text="""{
            "b": "3"
        }"""))
        await s.edit_data_link(url=input(), text="""{
            "a": 1
        }""")
        await s.close()


    asyncio.run(main())
```
