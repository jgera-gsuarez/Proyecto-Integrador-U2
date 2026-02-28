"""
Esto te deja un MVP sólido para funciones racionales / meromorfas con denominador “resoluble”.
Luego extendemos el caso infinito (1/sin(z)) con enumeración según los bounds del contorno.
"""
from typing import List, Tuple
import sympy as sp

def candidate_singularities(f_expr, z_symbol) -> List[sp.Expr]:
    """
    Intenta obtener singularidades candidatas (principalmente polos)
    a partir del denominador de f.
    """
    f_simpl = sp.together(f_expr)
    num, den = sp.fraction(f_simpl)

    # Si den es 1, no hay polos por este método
    if den == 1:
        return []

    # Resolver den = 0
    sol = sp.solveset(sp.Eq(den, 0), z_symbol, domain=sp.S.Complexes)

    # Caso finito
    if isinstance(sol, sp.FiniteSet):
        return list(sol)

    # Caso infinito o no resuelto: devolvemos vacío por ahora
    # (Luego puedes extender con patrones: sin(z)=0, cos(z)=0, exp(z)-1=0, etc.)
    return []

def classify_points(contour, points: List[sp.Expr]):
    inside, outside, boundary = [], [], []
    for p in points:
        if contour.on_boundary(p):
            boundary.append(p)
        elif contour.contains(p):
            inside.append(p)
        else:
            outside.append(p)
    return inside, outside, boundary
