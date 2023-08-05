#Error classes _______________________________________________________________# 
#_____________________________________________________________________________#
#_____________________________________________________________________________#

class InvalidType(Exception):
    def __init__(self, mt):
        self.mt = mt
    
    def __str__(self):
        return (f'Invalid {self.mt.dtype} in Tensor object')
    
class InvalidNdim(Exception):
    def __init__(self, mt):
        self.mt = mt
    
    def __str__(self):
        return (f'{self.mt.ndim} is not a supported number of dimensions for Tensor object')

class InvalidMode(Exception):
    def __init__(self, mode):
        self.mode = mode
    
    def __str__(self):
        return (f'"{self.mode}" is an invalid mode for Tensor object creation')
                
#Tensor helper functions _____________________________________________________# 
#_____________________________________________________________________________#
#_____________________________________________________________________________#

def prettyp(mt, info):
    if mt.ndim == 1:
        print(info)
        print(mt.values)
    else:
        if mt.shape[0]>mt.shape[1] or mt.shape[0]==mt.shape[1] or mt.tr:
            print(info)
            for i in range(mt.shape[0]):
                print(mt.values[i])
        else:
            x = mt.shape[1]
            print(info)
            try:
                for i in range(x):
                    print(mt.values[i])
                #error on transposed: 'someday' I'll fix it
            except: pass

def getShape(lt):
    if type(lt) != list:
        return []
    return [len(lt)] + getShape(lt[0])

def getTypeof(lt):
    if len(getShape(lt)) == 2:
        return getTypeof(lt[0])
    elif len(getShape(lt)) == 3:
        return getTypeof(lt[0][0])
    else:
        return str(type(lt[0]))
    
def oper(el, op, scl):
    if op == '+':
        return el+scl
    if op == '*':
        return el*scl
    if op == '-':
        return el-scl
    elif op == '/':
        return el/scl 
    elif op == '%':
        return el%scl
    elif op == '**':
        return el**scl
    elif op == '//':
        return el//scl
    elif op == 'substitute':
        return scl
    else: raise
    

def Returnsew(op, scl, tensor):
    nd = tensor.ndim
    if nd == 1:
        n = 0
        for i in tensor.values:
            tensor.values[n] = oper(tensor.values[n], op, scl)
            n += 1
    elif nd == 2:
        for n in range(tensor.shape[0]):
            for m in range(tensor.shape[1]):
                tensor.values[n][m] = oper(tensor.values[n][m], op, scl)
    if isinstance(scl, float):
        tensor.updateType("<class 'float'>")
          
def Returnfew(func, tensor):
    nd = tensor.ndim
    if nd == 1:
        n = 0
        for i in tensor.values:
            tensor.values[n] = func(tensor.values[n])
            n += 1
    elif nd == 2:
        for n in range(tensor.shape[0]):
            for m in range(tensor.shape[1]):
                tensor.values[n][m] = func(tensor.values[n][m])
                if isinstance(tensor.values[n][m], float):
                    tensor.updateType("<class 'float'>")
                    

    
        