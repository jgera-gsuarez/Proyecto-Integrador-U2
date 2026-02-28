from dataclasses import dataclass
from typing import List, Dict, Any
import sympy as sp
from .singularities import candidate_singularities, classify_points

@dataclass
class IntegralResult:
    integral: sp.Expr
    report: Dict[str, Any]

def integrate_by_residues(f_expr, contour, z_symbol=None) -> IntegralResult:
    if z_symbol is None:
        z_symbol = sp.Symbol('z')

    # 1) singularidades candidatas
    cand = candidate_singularities(f_expr, z_symbol)
    inside, outside, boundary = classify_points(contour, cand)

    # 2) caso inválido: singularidad en el contorno
    if boundary:
        rep = {
            "status": "error",
            "reason": "Hay singularidades sobre el contorno; el teorema de residuos no aplica directamente.",
            "candidates": cand,
            "inside": inside,
            "outside": outside,
            "on_boundary": boundary
        }
        return IntegralResult(sp.nan, rep)

    # 3) calcular residuos
    residues = []
    for a in inside:
        r = sp.residue(f_expr, z_symbol, a)
        residues.append((a, sp.simplify(r)))

    sum_res = sp.simplify(sum(r for _, r in residues)) if residues else sp.Integer(0)

    # 4) integral = 2πi * suma * orientación
    integral = sp.simplify(contour.orientation * 2*sp.pi*sp.I * sum_res)

    rep = {
        "status": "ok",
        "function": f_expr,
        "candidates": cand,
        "inside": inside,
        "outside": outside,
        "on_boundary": boundary,
        "residues": residues,
        "sum_residues": sum_res,
        "orientation": contour.orientation,
        "integral": integral
    }
    return IntegralResult(integral, rep)