"""
This module offers a tool to manipulate several objects behaving
similarly in parallel. To do so, the objects to manipulate,
called _collaterals_, are gathered in a particular `Collateral`
object, whose attributes and methods allow a user to manipulate
all collaterals.

>>> import collateral as ll
>>> C = ll.Collateral([3, 4, 5, 3], (4, 3, 5))
>>> C
Collateral< [3, 4, 5, 3] // (4, 3, 5) >
>>> C.count(4)
Collateral< 1 // 1 >
>>> C.count(3)
Collateral< 2 // 1 >
>>> D = C.collateral_map(list)
>>> D
Collateral< [3, 4, 5, 3] // [4, 3, 5] >
>>> D.append(8)
>>> D
Collateral< [3, 4, 5, 3, 8] // [4, 3, 5, 8] >
"""
import collateral.tools as tools
import collateral.exception as exception
import collateral.collateral as collateral
import collateral.decorators as decorators

__version__ = "1.0.4"
__all__ = [ 'Collateral', 'CollateralError', 'tools', 'collateral', 'exception', 'decorators' ]

Collateral = collateral.Collateral
CollateralError = exception.CollateralError

