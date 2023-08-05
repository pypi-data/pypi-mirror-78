# Magic printer for Python CLI
## Introduction
This python library will be useful for you to print beautiful colored texts with decorations and other utilities.
## How to Usage
### Install Library
```bash
  pip install mgprint
```
### Import Library
```python
  import mgprint
  # or
  from mgprint import *
```
### Syntax 'mg' and examples
#### Font color
![1](docs/img/1-min.png)

![Example1](docs/img/d1-min.png)
#### Background colors
![2](docs/img/2-min.png)
![Example2](docs/img/d2-min.png)
#### Text decorations
![3](docs/img/3-min.png)

![Example2](docs/img/d3-min.png)
> Some functions puts the reset char by default.
### Usage
```python
from mgprint import *
# Combine flags
mprint("%Rw% WARNING[!] %;r% Undefinded values...")
mprint("%g*%[SUCCESS]%;m% Process finished")
mprint("%Bw_% Links ")
# Print all text of red since this point
mprint("%r%Red text%;%", True)
print("No styled text")
mprint("%r%Red text forever...", True)  # don't put reset char
print("This")
print("text")
print("is")
print("red")
# Reset
mreset()
print("Normal print")
# Print an banner
printHead("Hello world!", 50)
# You can replace '%' to '&' eventually
mprint("&g&Value: &;y& %d\n" % (5.3))
```
#### Output
![img](docs/img/demo-min.png)

### Functions
Name       | Description
-----------|------------
**mprint(**str *string*, bool *strict*=False**)** | Print `string` using mg syntax and if `strict` is true doesn't put reset char.
**cprint(**str *string*, bool *strict*=False**)** | Print likes `mprint` but doesn't skip the line.
**mstr(**str _string_**)**| Return `string` with mg syntax converted.
**printHead(**str _string_, int _dim_**)** | Print `string` in a banner of `dim` size.
**mreset()**| Reset console style.
 **cls()**| Clean console

### Color references

Background | Font  | Reference
-----------|-------|----------
 **#**     | **0** | Black
 **B**     | **b** | Blue
 **C**     | **c** | Cyan
 **G**     | **g** | Green
 **M**     | **m** | Magenta
 **R**     | **r** | Red
 **W**     | **w** | White
 **Y**     | **y** | Yellow

### Decoration references
 Tag     | Usage
---------|------
 **\***  | Bold
 **\_**  | Underline
 **\-**  | Invert
