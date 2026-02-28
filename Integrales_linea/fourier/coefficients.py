from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple
import sympy as sp
import math

from .integrators import try_symbolic_integral, numeric_integral

@dataclass
class Piece:
    expr: sp.Expr
    x0: sp.Expr
    x1: sp.Expr

def _build_basis(x: sp.Symbol, a: sp.Expr, T: sp.Expr, n: int):
    w = 2*sp.pi*n*(x - a)/T
    return sp.cos(w), sp.sin(w)

def compute_coefficients(
    x: sp.Symbol,
    a: sp.Expr,
    b: sp.Expr,
    N: int,
    expr: Optional[sp.Expr] = None,
    pieces: Optional[List[Piece]] = None,
    f_callable: Optional[Callable[[float], float]] = None,
    method: str = "auto",
    tol: float = 1e-8
):
    """
    Calcula a0, an, bn. Si pieces está presente, integra por tramos.
    method: "auto" | "symbolic" | "numeric"
    """
    T = sp.simplify(b - a)
    if T == 0:
        raise ValueError("Periodo T=b-a no puede ser 0")

    def integral_symbolic(g_expr, aa, bb):
        ok, val = try_symbolic_integral(g_expr, x, aa, bb)
        return ok, val

    def integral_numeric(g_func, aa, bb):
        # aa, bb vienen como SymPy; los convertimos a float
        return numeric_integral(g_func, float(sp.N(aa)), float(sp.N(bb)), tol=tol)

    # Helper para integrar por piezas o completo
    def integrate_g(g_expr, g_func):
        if pieces:
            # suma por tramos
            sym_ok_all = True
            sym_sum = sp.Integer(0)
            num_sum = 0.0

            for pc in pieces:
                sub_expr = sp.simplify(pc.expr * (g_expr/expr)) if expr is not None and expr != 0 else None

            # Mejor: construir g_expr pieza a pieza (g depende de f)
            # Aquí lo haremos directamente construyendo g_expr_piece = pc.expr * basis
            # Se arma arriba en el bucle de n.
            raise RuntimeError("Integración por piezas se maneja en el bucle principal (ver abajo).")
        else:
            # integral única
            if method in ("symbolic", "auto") and g_expr is not None:
                ok, val = integral_symbolic(g_expr, a, b)
                if ok and method != "numeric":
                    return "symbolic", val
                if method == "symbolic":
                    return "symbolic", val  # aunque no ok, regresa lo que tenga
            # numérico
            return "numeric", sp.Float(integral_numeric(g_func, a, b))

    # a0
    if pieces:
        # a0 por tramos
        sym_ok = True
        sym_val = sp.Integer(0)
        num_val = 0.0

        for pc in pieces:
            g_expr_piece = pc.expr
            # callable pieza: evaluamos pc.expr con lambdify sólo en el intervalo
            g_func_piece = None
            if f_callable is not None:
                # si el usuario ya dio callable de toda la función base, úsalo y listo
                g_func_piece = f_callable
            else:
                g_func_piece = sp.lambdify(x, g_expr_piece, modules=["math"])

            if method in ("symbolic", "auto"):
                ok, val = try_symbolic_integral(g_expr_piece, x, pc.x0, pc.x1)
                sym_ok = sym_ok and ok
                if ok:
                    sym_val += val
                else:
                    # si falla y estamos en auto, haremos numérico
                    if method == "symbolic":
                        sym_val += val

            if method == "numeric" or (method == "auto" and not sym_ok):
                num_val = 0.0
                # recompute num sum from scratch to avoid mixing
                for pc2 in pieces:
                    g_expr_p2 = pc2.expr
                    g_func_p2 = f_callable if f_callable is not None else sp.lambdify(x, g_expr_p2, modules=["math"])
                    num_val += numeric_integral(g_func_p2, float(sp.N(pc2.x0)), float(sp.N(pc2.x1)), tol=tol)
                break

        if method == "numeric" or (method == "auto" and not sym_ok):
            a0_int = sp.Float(num_val)
            method_used = "numeric"
        else:
            a0_int = sp.simplify(sym_val)
            method_used = "symbolic"
    else:
        # a0 simple
        if f_callable is None:
            f_callable = sp.lambdify(x, expr, modules=["math"])
        if method in ("symbolic", "auto"):
            ok, val = try_symbolic_integral(expr, x, a, b)
            if ok and method != "numeric":
                a0_int = val
                method_used = "symbolic"
            elif method == "symbolic":
                a0_int = val
                method_used = "symbolic"
            else:
                a0_int = sp.Float(numeric_integral(f_callable, float(sp.N(a)), float(sp.N(b)), tol=tol))
                method_used = "numeric"
        else:
            a0_int = sp.Float(numeric_integral(f_callable, float(sp.N(a)), float(sp.N(b)), tol=tol))
            method_used = "numeric"

    a0 = sp.simplify((2/T) * a0_int)

    an = []
    bn = []

    for n in range(1, N+1):
        cosn, sinn = _build_basis(x, a, T, n)

        if pieces:
            # integrar por tramos
            sym_ok = True
            sym_cos = sp.Integer(0)
            sym_sin = sp.Integer(0)

            # Para numérico
            num_cos = 0.0
            num_sin = 0.0

            for pc in pieces:
                gcos = sp.simplify(pc.expr * cosn)
                gsin = sp.simplify(pc.expr * sinn)

                if method in ("symbolic", "auto"):
                    ok1, v1 = try_symbolic_integral(gcos, x, pc.x0, pc.x1)
                    ok2, v2 = try_symbolic_integral(gsin, x, pc.x0, pc.x1)
                    sym_ok = sym_ok and ok1 and ok2
                    if ok1: sym_cos += v1
                    else:
                        if method == "symbolic": sym_cos += v1
                    if ok2: sym_sin += v2
                    else:
                        if method == "symbolic": sym_sin += v2

            if method == "numeric" or (method == "auto" and not sym_ok):
                # recompute numeric sums
                for pc2 in pieces:
                    # build callable for each integrand
                    # prefer lambdify of sympy expression gcos/gsin for correctness
                    gcos2 = sp.simplify(pc2.expr * cosn)
                    gsin2 = sp.simplify(pc2.expr * sinn)
                    fcos = sp.lambdify(x, gcos2, modules=["math"])
                    fsin = sp.lambdify(x, gsin2, modules=["math"])
                    num_cos += numeric_integral(fcos, float(sp.N(pc2.x0)), float(sp.N(pc2.x1)), tol=tol)
                    num_sin += numeric_integral(fsin, float(sp.N(pc2.x0)), float(sp.N(pc2.x1)), tol=tol)
                int_cos = sp.Float(num_cos)
                int_sin = sp.Float(num_sin)
                method_used = "numeric"
            else:
                int_cos = sp.simplify(sym_cos)
                int_sin = sp.simplify(sym_sin)
                method_used = "symbolic"

        else:
            # integral única
            gcos = sp.simplify(expr * cosn)
            gsin = sp.simplify(expr * sinn)
            fcos = sp.lambdify(x, gcos, modules=["math"])
            fsin = sp.lambdify(x, gsin, modules=["math"])

            if method in ("symbolic", "auto"):
                ok1, v1 = try_symbolic_integral(gcos, x, a, b)
                ok2, v2 = try_symbolic_integral(gsin, x, a, b)
                if ok1 and ok2 and method != "numeric":
                    int_cos, int_sin = v1, v2
                    method_used = "symbolic"
                elif method == "symbolic":
                    int_cos, int_sin = v1, v2
                    method_used = "symbolic"
                else:
                    int_cos = sp.Float(numeric_integral(fcos, float(sp.N(a)), float(sp.N(b)), tol=tol))
                    int_sin = sp.Float(numeric_integral(fsin, float(sp.N(a)), float(sp.N(b)), tol=tol))
                    method_used = "numeric"
            else:
                int_cos = sp.Float(numeric_integral(fcos, float(sp.N(a)), float(sp.N(b)), tol=tol))
                int_sin = sp.Float(numeric_integral(fsin, float(sp.N(a)), float(sp.N(b)), tol=tol))
                method_used = "numeric"

        an.append(sp.simplify((2/T) * int_cos))
        bn.append(sp.simplify((2/T) * int_sin))

    return a0, an, bn, sp.simplify(T), method_used