from typing import Callable, Tuple, Optional, List
import sympy as sp
import mpmath as mp


def try_symbolic_integral(expr: sp.Expr, x: sp.Symbol, a: sp.Expr, b: sp.Expr) -> Tuple[bool, sp.Expr]:
    """
    Intenta integral simbólica definida.
    Retorna (ok, value).
    ok=False si SymPy deja Integral(...) sin evaluar.
    """
    try:
        val = sp.integrate(expr, (x, a, b))
        if isinstance(val, sp.Integral):
            return False, val
        return True, sp.simplify(val)
    except Exception:
        return False, sp.nan


def numeric_integral(
    func: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-8,
    breakpoints: Optional[List[float]] = None
) -> float:
    """
    Integral numérica con mpmath.quad. Asume función real.
    Si breakpoints se proporciona, parte [a,b] en subintervalos para mejorar estabilidad
    (útil en discontinuidades).
    """
    if a == b:
        return 0.0
    if b < a:
        return -numeric_integral(func, b, a, tol=tol, breakpoints=breakpoints)

    # precisión decimal aproximada
    try:
        mp.mp.dps = max(30, int(-mp.log10(tol)) + 12)
    except Exception:
        mp.mp.dps = 50

    aa = mp.mpf(a)
    bb = mp.mpf(b)

    # Preparar nodos de corte
    cuts = []
    if breakpoints:
        for t in breakpoints:
            if a < t < b:
                cuts.append(float(t))
        cuts = sorted(set(cuts))

    # Si hay cortes, integrar por segmentos
    if cuts:
        nodes = [a] + cuts + [b]
        total = mp.mpf("0")
        for i in range(len(nodes) - 1):
            left = mp.mpf(nodes[i])
            right = mp.mpf(nodes[i + 1])
            # integrar cada tramo; mpmath acepta lista [left,right]
            total += mp.quad(lambda t: func(float(t)), [left, right])
        return float(total)

    # Sin cortes: integral directa
    val = mp.quad(lambda t: func(float(t)), [aa, bb])
    return float(val)