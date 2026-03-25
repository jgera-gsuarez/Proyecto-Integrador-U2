from typing import List, Optional, Tuple
import sympy as sp

def compute_coefficients(
    x: sp.Symbol,
    a: sp.Expr,
    b: sp.Expr,
    n_harmonics: int,
    expr: Optional[sp.Expr] = None,
)-> Tuple[sp.Expr, List[sp.Expr], List[sp.Expr]]:
    """
    Calcula a0, an, bn para una expresión de SymPy en el intervalo [a, b]
    """
    if expr is None:
        # Si no hay expresión (señal de librería), retornamos ceros para evitar errores
        return sp.sympify(0), [sp.sympify(0)]*n_harmonics, [sp.sympify(0)]*n_harmonics

    #Definir parámetros básicos
    _T = sp.simplify(b - a)
    w0 = 2*sp.pi/_T
    n = sp.Symbol('n', integer=True, positive=True)

    if _T == 0:
        raise ValueError("Periodo T=b-a no puede ser 0")

    # 2. Cálculo de a0 (Componente DC)
    # Formula: (1/T) * integral(f(x), a, b)
    a0_int = sp.integrate(expr, (x, a, b))
    a0 = a0_int / _T

    an_list = []
    bn_list = []

    # 3. Cálculo de an y bn
    # Intentamos la integración simbólica general para obtener una fórmula en términos de 'n'
    try:
        # an = (2/T) * integral(f(x) * cos(n * w0 * x), a, b)
        term_an = (2 / _T) * sp.integrate(expr * sp.cos(n * w0 * x), (x, a, b))
        # bn = (2/T) * integral(f(x) * sin(n * w0 * x), a, b)
        term_bn = (2 / _T) * sp.integrate(expr * sp.sin(n * w0 * x), (x, a, b))

        for i in range(1, n_harmonics+1):
            # Evaluamos la n en la fórmula general
            an_list.append(sp.simplify(term_an.subs(n, i)))
            bn_list.append(sp.simplify(term_bn.subs(n, i)))

    except (sp.PoleError, TypeError, ValueError, RuntimeError):
        # Si la integración simbólica general falla, integramos numéricamente cada término
        for i in range(1, n_harmonics + 1):
            an_val = (2 / _T) * sp.integrate(expr * sp.cos(i * w0 * x), (x, a, b))
            bn_val = (2 / _T) * sp.integrate(expr * sp.sin(i * w0 * x), (x, a, b))
            an_list.append(sp.simplify(an_val))
            bn_list.append(sp.simplify(bn_val))

    return sp.simplify(a0), an_list, bn_list