#encoding: utf-8
"""Засоби перетворення Python-функцій у рівняння SymPy та формули LaTeX та засоби символьного розв'язування рівнянь, ліва частина яких є Python-функцією"""

import sympy, inspect

def T_o(L, n, s):
    """Основний час для точіння, розточування, свердління
де
*l* - довжина робочого ходу
*n* - частота обертів
*s* - подача"""
    return L/(n*s)

def fn2sympy(f, **args):
    """Намагається перетворити функцію f в рівняння SymPy
args - необов'язкові аргументи функції f
Приклад:
def f(x, a):
    return a*x**2+1
>>> fn2sympy(f)
Eq(f, a*x**2 + 1)
>>> fn2sympy(f, a=2)
Eq(f, 2*x**2 + 1)
"""
    name=f.__name__
    fargs=inspect.getfullargspec(f).args
    fargs=[sympy.Symbol(x) for x in fargs]
    #fargs=sympy.symbols(", ".join(fargs))
    return sympy.Eq(sympy.S(name), sympy.S(f(*fargs)).subs(args))

def fn2latex(f, **args):
    """Намагається перетворити функцію f в формулу LaTeX"""
    return sympy.latex(fn2sympy(f, **args))

def fndoc(f):
    "Розширена документація по функції з формулою LaTeX"
    return f.__doc__ + "\n$" + fn2latex(f)+"$"

def fn_solve(f, v, **args):
    """Розв'язує f(x,args)=v та повертає список значень x з елементами sympy
Приклад:
def f(x, a):
    return a*x**2+1
>>> fn_solve(f, 5, a=2)
[-1.41421356237310, 1.41421356237310]
>>> fn_solve(f, 5, a=sympy.S("a"))
[-2.0*(1/a)**0.5, 2.0*(1/a)**0.5]
"""
    name=f.__name__
    fargs=set(inspect.getfullargspec(f).args)
    root=fargs-args.keys()
    sol=sympy.solve(fn2sympy(f).subs(args), root)
    sol=[s.subs({name:v}).evalf() for s in sol]
    return sol

if __name__=="__main__":
    fn2sympy(T_o)
    fn2sympy(T_o, n=2)
    fn2latex(T_o)
    fndoc(T_o)
    fn_solve(T_o, 5, L=10, s=2)
    fn_solve(T_o, 5, L=10, s=sympy.S("s"))