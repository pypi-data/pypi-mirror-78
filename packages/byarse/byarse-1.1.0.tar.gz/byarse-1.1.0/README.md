# Bytes Argument Serializer

```python
import os, datetime
from byarse import Pickle
from byarse import BAS


bas = BAS(safe=True, len64=False) # Serializer/Deserializer


class Test: # Test class (for pickling)
    randomdata = os.urandom(16)


i = input("Read or write? (r/w)\n")


if i.lower().startswith('w'): # 'w'
    # ----
    # Serialize
    # ----
    with open('test', 'wb') as f:
        f.write(bas.s([
            'Hello, world!',
            b'Hello, world!',
            42,
            2.5,
            datetime.datetime.utcnow(),
            # Pickle(Test) # Will raise TypeError when read if safe mode is enabled.
        ]))
else: # 'r'
    # ----
    # Deserialize
    # ----
    with open('test', 'rb') as f:
        ua = bas.u(f.read()) # Unserialize

        for i in ua:
            print(type(i).__name__, ':', i) # Output: "type : argument" (ex. str : Hello, world!)
```
