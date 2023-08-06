"""
>>> import collateral as ll
>>>
>>> C = ll.Collateral({ 0: True, 'foo': 'bar' }, { 1: False, 'bar': 'foo' })
>>> for k in C:
... 	print(f"key: {k} and value: {C[k]}")
key: Collateral< 0 // 1 > and value: Collateral< True // False >
key: Collateral< 'foo' // 'bar' > and value: Collateral< 'bar' // 'foo' >
>>>
"""
