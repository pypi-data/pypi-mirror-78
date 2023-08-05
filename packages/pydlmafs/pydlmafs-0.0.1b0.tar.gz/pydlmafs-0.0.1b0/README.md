# pydlmafs: math done the wrong way

## This package contains three modules:
###     calc: Calculus with python functions
###     linalg: bad Linear Algebra implementation
###     probstat: Probability and Statistics *kinda*

### Note that the code in here was written without any concern about efficiency and has no use in real applications

## Installation

```python
pip install pydlmafs
```
```python
#Testing
import pydlmafgs.calc as clc
import pydlmafgs.linalg as ldl
import pydlmafgs.probstat as pst

def f(x):
    return 2*(x**2) + 2

print(clc.uni_deriv(f, 5))

vec = ldl.Tensor([6, -5, 2])
eye = ldl.Identity(3)

(eye @ vec).show()

ldl.EWise('func', vec, func=pst.sigmoid)
vec.show()
```


