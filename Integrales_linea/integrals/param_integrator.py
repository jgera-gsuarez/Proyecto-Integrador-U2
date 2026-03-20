import sympy as sp
#t = sp.Symbol('t', real=True)

import sympy as sp
from typing import Tuple


def integrate_parametric(f_expr, z_symbol, z_t, t_symbol, t_start, t_end) -> sp.Expr:
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

    return sp.simplify(resultado)


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