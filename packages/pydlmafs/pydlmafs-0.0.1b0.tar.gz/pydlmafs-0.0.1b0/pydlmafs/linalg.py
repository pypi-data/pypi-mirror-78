#!/usr/bin/env python3
# _*_ coding: utf_8 _*_
"""
Created on Mon Aug 10 16:24:13 2020

@author: booleangabs
"""

import helpers as hl 
from copy import deepcopy
from math import sqrt, acos, pi, floor, ceil
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import axes3d


#Constants ___________________________________________________________________# 
#_____________________________________________________________________________#
#_____________________________________________________________________________#

dtypes = ["<class 'int'>",
          "<class 'float'>", 
          "<class 'list'>"]
    
#Main classes and functions __________________________________________________# 
#_____________________________________________________________________________#
#_____________________________________________________________________________#

class Tensor:
    def __init__(self, lt: list):
        if len(lt) == 1: raise TypeError
        self.values = lt
        self.shape = hl.getShape(self.values)
        self.ndim = len(self.shape)
        if self.ndim == 0 or self.ndim > 2:
            raise hl.InvalidNdim(self)
        self.dtype = hl.getTypeof(self.values)
        if not (self.dtype in dtypes):
            raise hl.InvalidType(self)
        self.tr = False    
            
    def show(self):
        hl.prettyp(self, f'{self.ndim}d Tensor of type {self.dtype}:')
        
    def __str__(self):
        return f'<Tensor {tuple(self.shape)}>'
        
    def updateType(self, ntype):
        self.dtype = ntype
        
    def to_numpy(self, dtype):
        from numpy import array
        return array(self.values, dtype=dtype)
    
    def T(self):
        self.tr = not(self.tr)
        t = CreateTensorCopy(self, 'full')
        if t.ndim == 1: return t
        else:
            t.values = [list(row) for row in zip(*t.values)]
            t.shape[0], t.shape[1] = t.shape[1], t.shape[0]
            return t
        
    def iT(self):
        if self.ndim == 1: return self
        else:
            self.values = [list(row) for row in zip(*self.values)]
            self.shape[0], self.shape[1] = self.shape[1], self.shape[0]
            self.tr = not(self.tr)
            return self
        
    def mag(self):
        if self.ndim > 1: raise RuntimeError()
        else:
            m = 0
            for i in range(self.shape[0]):
                m += (self.values[i])**2
            m = (sqrt(m))
            return onefy(m)
        
    def __float__(self):
        EWise('func', self, func=float)
        return 1.0
        
    def __int__(self):
        EWise('func', self, func=int)
        return 1
        
    def __getitem__(self, k):
        if isinstance(k, slice):
            if self.ndim == 1:
                ind = range(*k.indices(len(self.list)))
                return Tensor([self.values[i] for i in ind])
        else: return self.values[k]
        
    def __setitem__(self, k, v):
        if isinstance(k, slice):
            if self.ndim == 1:
                ind = range(*k.indices(len(self.list)))
                for i in ind:
                    self.values[i] = v
        else: self.values[k] = v
    
    def __add__(self, other):
        t = CreateTensorCopy(self, 'full')
        if isinstance(other, float) or isinstance(other, int):
                EWise('scalar', t, ('+', other))
        else:
            if isinstance(other, Tensor):
                if t.ndim==1 and other.ndim==1:
                    n = 0
                    for i in t.values:
                        t.values[n] += other.values[n]
                        n += 1
                if t.ndim == 2 and t.shape==other.shape:
                    for i in range(len(t.values)):
                        for j in range(len(t.values[0])):
                            t.values[i][j] += other.values[i][j]
                elif t.ndim == 2 and other.ndim == 1:
                    for i in range(t.shape[0]):
                        for j in range(t.shape[1]):
                            t.values[i][j] += other.values[j]
            else: raise TypeError(other)
        return t
    
    def __sub__(self, other):
        t = CreateTensorCopy(self, 'full')
        if isinstance(other, float) or isinstance(other, int):
                EWise('scalar', t, ('-', other))
        else:
            if isinstance(other, Tensor):
                if t.ndim==1 and other.ndim==1:
                    n = 0
                    for i in t.values:
                        t.values[n] -= other.values[n]
                        n += 1
                if t.ndim == 2 and t.shape==other.shape:
                    for i in range(len(t.values)):
                        for j in range(len(t.values[0])):
                            t.values[i][j] -= other.values[i][j]
                elif t.ndim == 2 and other.ndim == 1:
                    for i in range(t.shape[0]):
                        for j in range(t.shape[1]):
                            t.values[i][j] -= other.values[j]
                else: raise ValueError(other)
            else: raise TypeError(other)
        return t
    
    def __mul__(self, other):
        t = CreateTensorCopy(self, 'full')
        if isinstance(other, float) or isinstance(other, int):
                EWise('scalar', t, ('*', other))
                return t
        else:
            if isinstance(other, Tensor) and not(self.ndim == other.ndim): 
                raise
            elif isinstance(other, Tensor) and self.ndim == other.ndim:
                if t.ndim == 1:
                    n = 0
                    for i in t.values:
                        t.values[n] *= other.values[n]
                        n += 1
                    return sum(t.values)
    
    def __matmul__(self, other):
        t = CreateTensorCopy(self, 'full')
        if isinstance(other, float) or isinstance(other, int):
            raise TypeError(f'Cannot take the element-wise product between:\
                            {self} and {other}')
        else:
            if isinstance(other, Tensor):
                if t.ndim == 1 and other.ndim==1:
                    return cross(self, other)
                # Some annoying bug is happening somewhere in here
                elif t.ndim == 2 and t.shape[1]==other.shape[0] and other.ndim == 2:
                    t2 = Tensor([[0]*other.shape[1]]*t.shape[0])
                    A = [*t.values]
                    B = [*other.values]
                    r = [[sum(a*b for a,b in zip(Al, Bc)) for Bc in zip(*B)]\
                         for Al in A]
                    t2.values = r
                #--------------------------------------------------
                elif t.ndim == 2 and other.ndim == 1:
                    if not(t.shape[1]==other.shape[0]): raise RuntimeError()
                    t2 = Tensor([0]*t.shape[0])
                    for j in range(t.shape[0]):
                        total = 0
                        for i in range(t.shape[1]):
                            total += t[j][i] * other[i]
                        t2[j] = total
                else: raise ValueError()
                return t2
        return t
    
    def __neg__(self):
        t = CreateTensorCopy(self, 'full')
        EWise('scalar', t, ('*', -1))
        return t
    
    def __truediv__(self, other):
        t = CreateTensorCopy(self, 'full')
        if isinstance(other, float) or isinstance(other, int):
                EWise('scalar', t, ('/', other))
        elif isinstance(other, Tensor): raise RuntimeError()
        return t
    
    def __mod__(self, other):
        t = CreateTensorCopy(self, 'full')
        if isinstance(other, float) or isinstance(other, int):
                EWise('scalar', t, ('%', other))
        else:
            raise TypeError(self, other)
        return t
    
    def __floordiv__(self, other):
        t = CreateTensorCopy(self, 'full')
        if isinstance(other, float) or isinstance(other, int):
                EWise('scalar', t, ('//', other))
        else:
            raise TypeError(self, other)
        return t
    
    def __pow__(self, other):
        t = CreateTensorCopy(self, 'full')
        if isinstance(other, float) or isinstance(other, int):
                EWise('scalar', t, ('**', other))
        else:
            raise TypeError(self, other)
        return t
    
    def __eq__(self, other):
        if not(isinstance(other, Tensor)): raise TypeError(self, other)
        else: return (self.values==other.values)
        
    def __ne__(self, other):
        if not(isinstance(other, Tensor)): raise TypeError(self, other)
        else: return (self.values!=other.values)
    
    def __gt__(self, other):
        if not(isinstance(other, Tensor)): raise TypeError(self, other)
        else: return (self.mag()>other.mag())
    
    def __lt__(self, other):
        if not(isinstance(other, Tensor)): raise TypeError(self, other)
        else: return (self.mag()<other.mag())
    
    def __ge__(self, other):
        if not(isinstance(other, Tensor)): raise TypeError(self, other)
        else: return (self>other) or (self==other)
        
    def __le__(self, other):
        if not(isinstance(other, Tensor)): raise TypeError(self, other)
        else: return (self<other) or (self==other)
        
    def __and__(self, other):
        if not(isinstance(other, Tensor)): raise TypeError(self, other)
        if self.ndim == 1 and other.ndim==1:
            return not(self<other) and not(self>other)
        elif self.ndim==2 and other.ndim==2:
            return self.shape==other.shape
        else: raise ValueError
        
    
    
# - Tensor generation
        
def CreateTensorCopy(copy_from, mode, scl=None):
    if not(mode in ('shape', 'full')):
        raise
    if mode == 'shape':
        if scl == None: raise ValueError(scl)
        c = Tensor(deepcopy(copy_from.values))
        EWise(mode='scalar', tensor=c, op_scl_tuple=('substitute',scl))
        c.tr = True if copy_from.tr else False
        return c
    else: return Tensor(deepcopy(copy_from.values))

def Zeros(n, m=None):
    l = None
    if n == None: raise TypeError(f'Missing 1 required positional \
                                  argument: "n"')
    if m == None: l = [[0 for i in range(n)] for j in range(n)]
    else: l = [[0 for i in range(m)] for j in range(n)]
    return Tensor(l)

def Ones(n, m=None):
    l = None
    if n == None: raise TypeError(f'Missing 1 required positional \
                                  argument: "n"')
    elif m == None: l = [[1 for i in range(n)] for j in range(n)]
    else: l = [[1 for i in range(m)] for j in range(n)]
    return Tensor(l)

def Identity(n=None, copy=False, copy_from=None):
    if copy:
        if n != None: raise TypeError("n is not a required argumment in \
                                      copy mode")
        t = CreateTensorCopy(copy_from=copy_from, mode='shape', scl=0)
        for n in range(t.shape[0]):
            for m in range(t.shape[1]): 
                if n == m:
                    t.values[n][m] = 1
    else:
        if n == None: raise TypeError(f'Missing 1 required positional \
                                      argument: "n"')
        t = Zeros(n)
        for n in range(t.shape[0]):
            for m in range(t.shape[1]): 
                if n == m:
                    t.values[n][m] = 1
    return t
        
def Diagonal(scl, n=None, copy=False, copy_from=None,):
    if not copy: 
        t = Zeros(n)
        if isinstance(scl, list):
            l = deepcopy(scl)
            w = 0
            for n in range(t.shape[0]):
                for m in range(t.shape[1]):
                    if n==m:
                        t.values[n][m] = l[w]
                        w += 1
        elif isinstance(scl, int) or isinstance(scl, float):
            for n in range(t.shape[0]):
                for m in range(t.shape[1]): 
                    if n == m:
                        t.values[n][m] = scl
    else:
        if copy_from == None: 
            raise TypeError(f'Missing 1 required positional \
                            argument: "copy_from"')
        if not n == None: 
            raise TypeError("n is not a required argummnt in copy mode")
        t = CreateTensorCopy(copy_from=copy_from, mode='shape', scl=0)
        if isinstance(scl, list):
            l = deepcopy(scl)
            w = 0
            for n in range(t.shape[0]):
                for m in range(t.shape[1]):
                    if n==m:
                        try:
                            t.values[n][m] = l[w]
                            w += 1
                        except:
                            pass
        elif isinstance(scl, int) or isinstance(scl, float):
            for n in range(t.shape[0]):
                for m in range(t.shape[1]): 
                    if n == m:
                        t.values[n][m] = scl
    return t

def Triangular(scl, n=None, copy=False, tensor=None, mode='upper'):
    if not(mode in ('upper', 'lower')): raise RuntimeError()
    if not copy:
        if n==None: return
        if isinstance(scl, int):
            t = Diagonal(scl, n)
            for i in range(t.shape[0]):
                for j in range(t.shape[1]):
                    if j>i:
                        t[i][j] = scl
            if mode=='lower': return t.T()
            
        if isinstance(scl, list):
            if not(len(scl)==n): return
            t = Zeros(len(scl))
            x = -1
            for i in range(t.shape[0]):
                l = deepcopy(scl)
                if mode == 'upper':
                    if len(scl[i])<t.shape[1]:
                        k = t.shape[1] - len(scl[i])
                        l[i] = [0]*k + l[i]
                    t[i] = l[i]
                if mode=='lower':
                    if len(scl[x])<t.shape[1]:
                        k = t.shape[1] - len(scl[x])
                        l[x] = (l[x] + [0]*k)
                    t[i] = l[x]
                    x -= 1
        return t
    
# - Basic operations
    
def Angle(x, y, mode=None):
    if x == y or areParallel(x, y) : return 0.0
    xy = x*y
    mxy = (x.mag()*y.mag())
    if not(mxy): return 0.0
    d = xy/mxy
    d = float(f'{d:.4f}')
    if d==0: return 90.0
    res = (acos(d)) * (180/pi)
    if mode == None: return float(f'%.6f'%res)
    elif mode == 'floor': return floor(res)
    elif mode == 'ceil': return ceil(res)
    elif mode == 'inbt': return float(f'%.4f'%((floor(res)+ceil(res)+res)/3)) 

def Unit(x):
    if x.ndim != 1: raise TypeError("Cannot take the unit vector of a matrix")
    t = CreateTensorCopy(x, 'full')
    tm = t.mag()
    return (t/tm)

def hadamard(t, t2):
    tens = CreateTensorCopy(t, 'full')
    if not(t.shape==t2.shape): raise ValueError()
    if t.ndim == 1:
        for i in range(t.shape[0]):
            tens[i] = t[i] * t2[i]
    return tens

def cross(x, y):
    if (isinstance(x, Tensor) & isinstance(y, Tensor)) and \
        not(x.ndim == y.ndim and x.shape==y.shape): raise RuntimeError()
    else:
        if x.ndim ==1 and y.ndim==1 and len(x.values)==len(y.values):
            if x.shape[0] == 2: x.values.append(0)
            if y.shape[0] == 2: y.values.append(0)
            t = CreateTensorCopy(x, 'full')
            t[0] = x[1]*y[2] - x[2]*y[1]
            t[1] = x[2]*y[0] - x[0]*y[2]
            t[2] = x[0]*y[1] - x[1]*y[0]
            return t
        
def dot(x, y):
    if (isinstance(x, Tensor) & isinstance(y, Tensor)) and \
        not(x.ndim == y.ndim and x.shape==y.shape): raise RuntimeError()
    t = CreateTensorCopy(x,'full')
    if t.ndim == 1:
        n = 0
        for i in t.values:
            t.values[n] *= y.values[n]
            n += 1
        return sum(t.values)

def EWise(mode, tensor, op_scl_tuple=None, func=None):
    if not(mode in ('scalar', 'func')):
        raise
    if mode == 'scalar':
        return hl.Returnsew(op_scl_tuple[0], op_scl_tuple[1], tensor)
    else: return hl.Returnfew(func, tensor)
    
def areParallel(t, t2):
    if len(t.shape) == 2 or len(t2.shape) == 2: raise TypeError
    elif t == t2: return True
    else: return True if abs(extreme(t*t2)-(t.mag()*t2.mag()))<0.5 else False

def arePerp(t, t2):
    return True if Angle(t, t2)==90 else False

def areCollinear(t, t2):
    if t.shape!=t2.shape: raise ValueError(f'Expected shape {t.shape}, got \
                                           {t2.shape} for second Tensor')
    if t.ndim!=1: raise ValueError('Can only be used with vectors')
    frac = []
    for i in range(len(t.values)):
        frac.append(t[1]/t2[1])
    t_f = Tensor(frac)
    m1 = hadamard(t_f,t)
    m2 = hadamard(t_f,t2)
    return True if m1 == t2 or m2 == t else False

def areOrthogonal(t, t2):
    return not(dot(t, t2)!=0)

def mixedproduct(t, t2, t3):
    return dot(t, cross(t2, t3))

def areCoplanar(t, t2, t3):
    return mixedproduct(t, t2, t3)==0

def extreme(n):
    return floor(n) if (int(n)-n)<-0.5 else ceil(n)

def onefy(n):
    return 1.0 if abs(1-n)<0.125 else n
        
def isSym(t):
    return True if t==t.T() else False

def isSkewSym(t):
    return True if t==-t.T() else False

def isSquare(t):
    if len(t.shape)==1: raise ValueError(t)
    return True if t.shape[0]==t.shape[1] else False

def from_numpy(x):
    return Tensor(x.tolist())

def proj(u, v):
    dot = u*v
    m = v.mag()**2
    f = dot/m
    return v * f

def initPlot(lim=(0, 10)):
    fig = plt.figure(figsize=(10, 10))
    x= fig.gca(projection='3d')
    x.set_xlim3d(lim[0], lim[1])
    x.set_xlabel('x')
    x.set_ylim3d(lim[0], lim[1])
    x.set_ylabel('y')
    x.set_zlim3d(lim[0], lim[1])
    x.set_zlabel('z')
    x.view_init(15, -60)
    n = (15, -60)
    return fig, x, n

def plotTensor(fig, x, tensor, origin=[0,0,0], in_norm=False,\
               color='blue', label=''):
    x.quiver(*origin,*tensor.values, length=0.75, normalize=in_norm, \
             color=color, label=label)
    fig.legend()

def rotPlot(x, n):
    x.view_init(n[0], n[1])
    
def det(matrix):
    if not(isSquare(matrix)): return None
    elif matrix.shape == [2, 2]:
        return (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])
    elif matrix.shape == [3, 3]:
        a1 = matrix[0][0]
        f1 = Tensor([[matrix[1][1], matrix[1][2]], [matrix[2][1], matrix[2][2]]])
        a2 = matrix[0][1]
        f2 = Tensor([[matrix[1][0], matrix[1][2]], [matrix[2][0], matrix[2][2]]])
        a3 = matrix[0][2]
        f3 = Tensor([[matrix[1][0], matrix[1][1]], [matrix[2][0], matrix[2][1]]])
        return (a1 * det(f1)) - (a2 * det(f2)) + (a3 * det(f3))
    else:
        from numpy.linalg import det as d
        npm = matrix.to_numpy('int64')
        return d(npm)

def getdiag(matrix):
    if matrix.ndim == 2:
        diag = []
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if i==j: diag.append(matrix[i][j])
        return diag
    else: raise ValueError(matrix)
    
def Tr(A):
    return sum(getdiag(A))

def adjustprec5(x):
    return float(f'{x:.5f}')

def adjustprec3(x):
    return float(f'{x:.3f}')

def adjustprec1(x):
    return float(f'{x:.1f}')

def adjustfloat(t, adjuster=adjustprec5):
    return EWise('func', t, func=adjuster)