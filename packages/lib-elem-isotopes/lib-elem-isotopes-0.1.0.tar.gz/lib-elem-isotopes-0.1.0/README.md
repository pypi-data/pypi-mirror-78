### Installation
To install this package it is best to use pip3.

In order to install this package type: *pip3 install lib-kaasknak*

### Usage
In order to use the package import lib in your python editor of choice.

The commands that can be used are:
- ElementZ(input) which gives the Z-value of the corresponding element.
- ElementN(input) which gives the name of the element corresponding to this Z-value.
- NatComp(input) which gives the isotopes in nature and their fractions.

### Example

```python
import lib
a=lib.ElementZ("Gd")
b,c=lib.NatComp("Gd")
print(a)
print(b)
print(c)
```
```output
64
[152, 154, 155, 156, 157, 158, 160]
[0.002, 0.0218, 0.148, 0.2047, 0.1565, 0.2484, 0.2186]
```

### Sidenote
If the element has no natural occuring isotopes it will return a list with one 0 in it. If the element only has traces of an isotope occuring in nature it will return the mass numbers of these traces. In both cases the fractions list will contain a single 0.

Data is gather from the wikipedia page for every individual element.

