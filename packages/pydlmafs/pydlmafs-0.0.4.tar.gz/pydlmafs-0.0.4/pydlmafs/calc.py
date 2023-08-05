#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def uni_deriv(func, x):
    
    """
    Retorna a aproximação da derivada da função de uma 
    variável func no ponto x.
    ____________________________________________________
    
    Entrada:
        func: função matemática
        x: ponto no eixo x
    Retorno:
        ->float: derivada obtida
    """
    
    h = 1e-9
    return float('%.17f'%((func(x+h)-func(x-h)) /  (2*h)))

def uni_integral(func, lower, upper, n=1e10):
    
    """
    Retorna a aproximação da integral da função de uma 
    variável func no ponto x.
    ____________________________________________________
    
    Entrada:
        func: função matemática
        x: ponto no eixo x
    Retorno:
        ->float: integral obtida
    """
    
    dx = ((upper - lower) / n)
    cumul = 0
    x = lower
    while x <= upper:
        t = ((func(x)+func(x+dx)) / 2 ) * dx
        cumul += t
        x += dx
    return float('%.17f'%(cumul))
