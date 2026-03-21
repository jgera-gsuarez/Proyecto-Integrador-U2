# Integrales_linea/fourier/series.py
from __future__ import annotations
from typing import Callable, List
import sympy as sp
import math


def build_series_callable(
    a0: sp.Expr,
    an: List[sp.Expr],
    bn: List[sp.Expr],
    a: sp.Expr,
    _T: sp.Expr
) -> Callable[[float], float]:
    """
    Devuelve S_N(x) como función numérica.
    Convierte coeficientes (posiblemente simbólicos) a float usando N().
    """
    a_float = float(sp.N(a))
    _T_float = float(sp.N(_T))

    a0f = float(sp.N(a0))
    anf = [float(sp.N(v)) for v in an]
    bnf = [float(sp.N(v)) for v in bn]
    _N = len(anf)

    def S(x: float) -> float:
        s = a0f
        for n in range(1, _N + 1):
            w = 2 * math.pi * n * (x - a_float) / _T_float
            s += anf[n - 1] * math.cos(w) + bnf[n - 1] * math.sin(w)
        return s

    return S


def build_series_expr(
    x: sp.Symbol,
    a0: sp.Expr,
    an: List[sp.Expr],
    bn: List[sp.Expr],
    a: sp.Expr,
    _T: sp.Expr
) -> sp.Expr:
    """
    Devuelve S_N(x) como expresión SymPy (útil si los coeficientes son simbólicos).
    """
    expr = a0
    for n, (A, B) in enumerate(zip(an, bn), start=1):
        w = 2 * sp.pi * n * (x - a) / _T
        expr += A * sp.cos(w) + B * sp.sin(w)
    return sp.simplify(expr)