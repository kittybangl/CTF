from time import time
from datetime import datetime, timezone
ts = datetime.now(tz=timezone.utc)
ts.replace(microsecond=0)
a = int(ts.timestamp()).to_bytes(4, "little")
print(a)
b = datetime.fromtimestamp(int.from_bytes(a, 'little'), tz=timezone.utc)
print(int(b.timestamp()).to_bytes(4, "little"))
time_str = '2023-03-20T15:15:47.091999+00:00'
dt = datetime.fromisoformat(time_str)
print(int(dt.timestamp()).to_bytes(4, "little"))
print(dt)