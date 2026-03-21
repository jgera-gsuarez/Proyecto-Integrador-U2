import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations,
    implicit_multiplication_application, convert_xor
)

_TRANSFORMS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)

def normalize_math_input(s: str) -> str:
    s = s.strip()
    s = s.replace("−", "-")  # por si pegan signo raro
    return s

def parse_expr_math(expr_str: str, local_dict=None):
    """
    Parseo de expresiones matemáticas a SymPy.
    Soporta: ^, multiplicación implícita, pi, E, sin/cos/exp/log, abs, etc.
    """
    expr_str = normalize_math_input(expr_str)
    if local_dict is None:
        local_dict = {}

    # Variables típicas
    local_dict = dict(local_dict)

    #Complejos
    local_dict.setdefault("i", sp.I)
    local_dict.setdefault("I", sp.I)
    local_dict.setdefault("j", sp.I)

    local_dict.setdefault("pi", sp.pi)
    local_dict.setdefault("E", sp.E)
    local_dict.setdefault("e", sp.E)  # opcional

    # Funciones comunes
    local_dict.setdefault("sin", sp.sin)
    local_dict.setdefault("cos", sp.cos)
    local_dict.setdefault("tan", sp.tan)
    local_dict.setdefault("exp", sp.exp)
    local_dict.setdefault("log", sp.log)
    local_dict.setdefault("abs", sp.Abs)
    local_dict.setdefault("sqrt", sp.sqrt)

    #Para Fourier
    local_dict.setdefault("x", sp.Symbol('x', real=True))
    local_dict.setdefault("n", sp.Symbol('n', integer=True, positive=True))

    return parse_expr(expr_str, transformations=_TRANSFORMS, local_dict=local_dict)

def parse_number_math(num_str: str):
    """
    Parsea un número (a,b) o constante: pi, 2*pi, 0.5, etc.
    Retorna expresión SymPy (exacta si se puede).
    """
    return parse_expr_math(num_str)