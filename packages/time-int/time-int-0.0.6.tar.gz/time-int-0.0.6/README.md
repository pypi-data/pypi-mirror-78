# time-int
Integer subclass to represent naive time since epoch.

### The Idea
UNIX has a venerable tradition of representing time as seconds since the
start of 1970. This has its limitations, but it is sometimes desirably
simple. This package sub-classes int to give a little handy functionality
to this simple approach.

### Important Limitations
* Supported range starts at 0 or TimeInt.MIN on Jan 1, 1970
* Supported range ends at a 32-bit limit or TimeInt.MAX on Apr 2, 2106
* Values are rounded off to the nearest second.
* Values do not track what time-zone they represent.

### Quick Example
```python
from time_int import TimeInt

start_time = TimeInt.utcnow()
some_slow_operation()
end_time = TimeInt.utcnow()

print(f"Operation started at {start_time.get_pretty()}")
print(f"Operation ended  at  {end_time.get_pretty()}")
print(f"Operation took {end_time - start_time} seconds")
```

