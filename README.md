A tool for comparison of JSON-like structures.

It recursively walks through both structures and reports any mismatches found, such as:

- missing keys in dict
- type mismatch
- value mismatch
- list length difference

---
Usage:

```
Call:

from mismatcha import compare


d1 = {
    "user": {
        "id": 512341,
        "name": "Alex",
        "active": True,
        "score": 4.5,
        "tags": ["qa", "python", {"extra": False}]
    }
}

d2 = {
    "user": {
        "id": 6512,
        "active": "yes",
        "score": 4.5,
        "tags": ["qa", "python", {"extra": True}]
        "extra_param": "boo!"
    }
}

compare(expected=d1, actual=d2, ignore=["user.tags.extra"])
```

```
Output:

[user.id] Value mismatch 
Expected: 512341 (int) 
Actual: 6512 (int)

[user.name] Param not found 
Expected: name (str) 
Actual: None (NoneType)

[user.active] Type mismatch 
Expected: True (bool) 
Actual: yes (str)
```

---
Comparison rules:

- `dict`s are compared only by keys present in the `expected` structure
  (extra keys in the `actual` will be ignored)
- `list`s are compared by index (order matters)
- `int` and `float` are treated as compatible numeric types
- Anything other than `dict`/`list` will be compared as is.

---
Install: `pip install mismatcha`
