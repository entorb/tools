# Cartesian product of multi-value lists

* reads several lists from `cartesian-csv-gen.ini`
* generates Cartesian product of all combinations

## Example

Input

```ini
MyVar1 = Door1, Door2, Door3
MyVar2 = OK, NOK
MyVar3 = 0, 1
```

Output

```text
Door1 OK 0
Door1 OK 1
Door1 NOK 0
Door1 NOK 1
Door2 OK 0
Door2 OK 1
Door2 NOK 0
Door2 NOK 1
Door3 OK 0
Door3 OK 1
Door3 NOK 0
Door3 NOK 1
```
