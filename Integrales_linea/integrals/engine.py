import sympy as sp
from typing import Tuple

from matplotlib.cbook import pts_to_midstep

from .types import IntegralResult
from .singularities import candidate_singularities, classify_points

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

    if residues:
        sum_res = sp.simplify(sp.Add(*[r for _, r in residues]))
    else:
        sum_res = sp.sympify(0)

    # 4) integral = 2πi * suma * orientación
    integral = sp.simplify(contour.orientation * 2 * sp.pi * sp.I * sum_res)

    rep = {
        "status": "ok",
        "method": "residues",
        "function": f_expr,
        "candidates": cand,
        "inside": inside,
        "outside": outside,
        "on_boundary": boundary,
        "residues": residues,
        "sum_residues": sum_res,
        "orientation": contour.orientation,
        "integral": integral,
        "contour_obj": contour
    }

    return IntegralResult(integral, rep)

def integrate_parametric(f_expr, z_symbol, z_t, t_symbol, t_start, t_end) -> IntegralResult:
    """
    Calcula la integral de línea de f(z) sobre una curva parametrizada z(t).

    Parámetros:
    - f_expr: Expresión de SymPy para f(z).
    - z_symbol: El símbolo z usado en f_expr (ej. sp.Symbol('z')).
    - z_t: Expresión de SymPy que define la curva z(t).
    - t_symbol: El símbolo t usado como parámetro (ej. sp.Symbol('t', real=True)).
    - t_start: Límite inferior de integración para t.
    - t_end: Límite superior de integración para t.
    """

    # 1. Sustituir z por z(t) en la función
    f_zt = f_expr.subs(z_symbol, z_t)

    # 2. Calcular el diferencial dz = z'(t) dt
    dz_dt = sp.diff(z_t, t_symbol)

    # 3. Construir el integrando: f(z(t)) * z'(t)
    integrando = sp.simplify(f_zt * dz_dt)

    # 4. Integrar respecto a t
    resultado = sp.integrate(integrando, (t_symbol, t_start, t_end))

    #Lógica para la Gráfica
    #Generamos 100 puntos evaluando z(t) para que el plotte pueda dibujarlos
    t_vals = [t_start + (t_end-t_start) * i/99 for i in range(100)]
    z_points = [complex(sp.N(z_t.subs(t_symbol, tv))) for tv in t_vals]

    class ParametricPath:
        def __init__(self, pts): self.pts = pts
        def get_plot_points(self): return self.pts
        def bounds(self):
            x = [p.real for p in self.pts]; y = [p.imag for p in self.pts]
            return min(x), max(x), min(y), max(y)

    rep = {
        "status": "ok",
        "method": "parametric",
        "function": f_expr,
        "integral": resultado,
        "parametrization": z_t,
        "limits": (t_start, t_end),
        "integrand_t": integrando,
        "contour_obj": ParametricPath(z_points)
    }

    return IntegralResult(sp.simplify(resultado), rep)


# --- Funciones de ayuda para parametrizaciones comunes ---

def param_segment(z1: complex, z2: complex, t_symbol) -> Tuple[sp.Expr, float, float]:
    """
    Devuelve la parametrización de un segmento de línea recta desde z1 hasta z2.
    El parámetro t va de 0 a 1.
    """
    # z(t) = z1 + t*(z2 - z1)
    z_t = z1 + t_symbol * (z2 - z1)
    return z_t, 0.0, 1.0


def param_arc(center: complex, radius: float, angle_start: float, angle_end: float, t_symbol) -> Tuple[
    sp.Expr, float, float]:
    """
    Devuelve la parametrización de un arco de circunferencia.
    Los ángulos deben estar en radianes.
    """
    # z(t) = centro + radio * e^(i*t)
    z_t = center + radius * sp.exp(sp.I * t_symbol)
    return z_t, angle_start, angle_end