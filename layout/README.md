# track.py

...

# via.py

## How to use:

This library is ment to be called by *kicadpy* and is used to manipulate vias.

E.g.

```python
kp.via.place(10,10,0.2,0.5)
```

---

## Functions

### place()

```Python
def place(             # no return
    x_mm,              # postion x in millimeters [mm]
    y_mm,              # postion y in millimeters [mm]
    drillDiameter_mm,  # via hole diameter in millimeters [mm]
    width_mm)          # via diameter in millimeters [mm]
```
Place a via at a given position. 

How to call it.

```Python
import kicadpy as kp
kp.via.place(...)
```



