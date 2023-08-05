# Collateral
This tool package provides a simple way to manipulate _collateral_ objects in parallel.
Basically, it provides `Collateral` objects, which gather several objects, called _collaterals_.
The object has two kinds of methods/attributes: _collateral_ and _transversal_.

## Collateral methods and attributes
A collateral method returns a `Collateral` object (or `None`),
which is formed by the result of calling the corresponding method
on each of the collaterals.
Similarly, a collateral attribute has as value,
the `Collateral` object (or `None`)
formed by the result of getting the corresponding attribute
from each of the collaterals.
Hence, a collateral method/attribute behaves on each of the collaterals **independently**.
Collateral methods/attributes exist in a `Collateral` object
if and only if they exist in at least one of its collaterals.

## Transversal methods and attributes
Every `Collateral` object has the same, few, _transversal_ methods and attributes,
which aim to provide basic manipulation method and information on the `Collateral` object itself,
that is, not only on its collaterals.
These methods are methods/attributes of the object
that manipulate the whole object.
They typically do not manipulate the collaterals idenpendently.
E.g., the attribute `collaterals` is a property returning the tuple of collaterals.

## Examples:
```python
import collateral as ll

pL = ll.Collateral([3, 4], [5, 2])
pL[0]
#returns a Collateral object with two collaterals: 3 and 5
pL[1]
#returns a Collateral object with two collaterals: 4 and 2
pL.append(9)
#returns None
pL[2]
#returns a Collateral object with two collaterals: 9 and 9
pL.pop(0)
#returns a Collateral object with two collaterals: 3 and 5
#and pL is a Collateral object with two collaterals: [4, 9] and [2, 9]
pL[0]
#returns a Collateral object with two collaterals: 4 and 2
```
