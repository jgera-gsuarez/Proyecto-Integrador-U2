# Integrales_linea/fourier/series.py
from __future__ import annotations
from typing import Callable, List, Optional
import sympy as sp
import math


def build_series_callable(
    a0: sp.Expr,
    an: List[sp.Expr],
    bn: List[sp.Expr],
    a: sp.Expr,
    T: sp.Expr
) -> Callable[[float], float]:
    """
    Devuelve S_N(x) como función numérica.
    Convierte coeficientes (posiblemente simbólicos) a float usando N().
    """
    a_float = float(sp.N(a))
    T_float = float(sp.N(T))

    a0f = float(sp.N(a0))
    anf = [float(sp.N(v)) for v in an]
    bnf = [float(sp.N(v)) for v in bn]
    N = len(anf)

    def S(x: float) -> float:
        s = 0.5 * a0f
        for n in range(1, N + 1):
            w = 2 * math.pi * n * (x - a_float) / T_float
            s += anf[n - 1] * math.cos(w) + bnf[n - 1] * math.sin(w)
        return s

    return S


def build_series_expr(
    x: sp.Symbol,
    a0: sp.Expr,
    an: List[sp.Expr],
    bn: List[sp.Expr],
    a: sp.Expr,
    T: sp.Expr
) -> sp.Expr:
    """
    Devuelve S_N(x) como expresión SymPy (útil si los coeficientes son simbólicos).
    """
    expr = sp.Rational(1, 2) * a0
    for n, (A, B) in enumerate(zip(an, bn), start=1):
        w = 2 * sp.pi * n * (x - a) / T
        expr += A * sp.cos(w) + B * sp.sin(w)
    return sp.simplify(expr)