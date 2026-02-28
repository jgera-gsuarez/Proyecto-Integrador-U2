# Integrales_linea/fourier/engine.py
from __future__ import annotations
from typing import Dict, Any, Optional, Callable
import sympy as sp
import numpy as np

from ..core.parsing import parse_expr_math, parse_number_math
from ..core.types import FourierResult

from Integrales_linea.core.parsing import (
    #parse_piecewise_spec,
    parse_function_definition,
    parse_signal_call,
    PieceSpec
)
from .signals import SignalSpec, build_signal_callable
from .series import build_series_callable, build_series_expr
from .coefficients import compute_coefficients  # <-- tú lo crearás en fourier/coefficients.py


def _make_piecewise_base_callable(x: sp.Symbol, pieces: list[PieceSpec]) -> Callable[[float], float]:
    """
    Crea un evaluador base f(x) sobre el intervalo [a,b] usando piezas.
    Para valores fuera de cualquier pieza, retorna 0. (puedes cambiarlo si quieres)
    """
    compiled = []
    for pc in pieces:
        fn = sp.lambdify(x, pc.expr, modules=["math"])
        x0f = float(sp.N(pc.x0))
        x1f = float(sp.N(pc.x1))
        compiled.append((x0f, x1f, fn))

    def f_base(val: float) -> float:
        xv = float(val)
        for x0, x1, fn in compiled:
            # para Fourier, endpoints no importan en integrales, pero para evaluación no molesta permitirlos
            if x0 <= xv <= x1:
                return float(fn(xv))
        return 0.0

    return f_base


def compute_fourier(
    input_spec: Dict[str, Any],
    interval: Dict[str, str],
    N: int,
    method: str = "auto",
    samples: int = 2000,
    tol: float = 1e-8,
    build_symbolic_series: bool = True
) -> FourierResult:
    """
    input_spec:
      {"type":"expr", "expr":"x"}
      {"type":"piecewise", "spec":"0 : -pi < x < 0; 1 : 0 < x < pi"}
      {"type":"signal", "signal":"square(A=1,duty=0.5,hi=1,lo=0)"}  # usando parse_signal_call()
      {"type":"signal", "name":"square", "params":{...}}            # alternativa directa

    interval:
      {"a":"-pi", "b":"pi"}
    """
    x = sp.Symbol("x", real=True)

    # -------- Parse intervalo --------
    try:
        a = parse_number_math(interval["a"])
        b = parse_number_math(interval["b"])
        T = sp.simplify(b - a)
        if float(sp.N(T)) <= 0:
            raise ValueError("Debe cumplirse b > a.")
    except Exception as e:
        return FourierResult(
            status="error", message=f"Error en intervalo: {e}",
            a=sp.nan, b=sp.nan, T=sp.nan, N=N, method_used="",
            a0=sp.nan, an=[], bn=[],
            f_callable=None, s_callable=None,
            plot_data=None, report={"status": "error"}
        )

    # -------- Construye fuente f(x) --------
    expr = None
    pieces = None
    f_base = None
    input_desc = {}

    try:
        typ = input_spec.get("type", "").lower()

        if typ == "expr":
            expr_str = input_spec["expr"]
            expr = parse_expr_math(expr_str, local_dict={str(x): x})
            f_base = sp.lambdify(x, expr, modules=["math"])
            input_desc = {"tipo": "expresión", "f(x)": expr_str}

        elif typ == "piecewise":
            spec_str = input_spec["spec"]
            pieces = parse_piecewise_spec(spec_str, x)
            f_base = _make_piecewise_base_callable(x, pieces)
            input_desc = {"tipo": "por tramos", "spec": spec_str}

        elif typ == "signal":
            # Dos formatos: "signal":"square(A=1,...)" o name+params
            if "signal" in input_spec:
                name, params = parse_signal_call(input_spec["signal"])
            else:
                name = input_spec["name"]
                params = input_spec.get("params", {})
            aa = float(sp.N(a))
            bb = float(sp.N(b))
            f_base = build_signal_callable(SignalSpec(name=name, params=params), aa, bb)
            input_desc = {"tipo": "señal", "señal": name, "params": params}

        elif typ == "definition":
            # si quieres aceptar entradas tipo: "f(x)=x en (-pi,pi)"
            kind, expr2, pieces2, interval2 = parse_function_definition(input_spec["text"], x)
            if interval2 is not None:
                a, b = interval2
                T = sp.simplify(b - a)
            if kind == "expr":
                expr = expr2
                f_base = sp.lambdify(x, expr, modules=["math"])
                input_desc = {"tipo": "definición", "f(x)": str(expr)}
            else:
                pieces = pieces2
                f_base = _make_piecewise_base_callable(x, pieces)
                input_desc = {"tipo": "definición por tramos", "spec": input_spec["text"]}

        else:
            raise ValueError("type debe ser 'expr', 'piecewise', 'signal' (o 'definition' si lo usas).")

    except Exception as e:
        return FourierResult(
            status="error", message=f"Error en la función: {e}",
            a=a, b=b, T=T, N=N, method_used="",
            a0=sp.nan, an=[], bn=[],
            f_callable=None, s_callable=None,
            plot_data=None, report={"status": "error"}
        )

    # -------- Calcula coeficientes --------
    try:
        a0, an, bn, T_used, method_used = compute_coefficients(
            x=x, a=a, b=b, N=N,
            expr=expr,
            pieces=pieces,
            f_callable=f_base,
            method=method,
            tol=tol
        )
    except Exception as e:
        return FourierResult(
            status="error", message=f"Error calculando coeficientes: {e}",
            a=a, b=b, T=T, N=N, method_used="",
            a0=sp.nan, an=[], bn=[],
            f_callable=f_base, s_callable=None,
            plot_data=None, report={"status": "error"}
        )

    # -------- Construye S_N --------
    S = build_series_callable(a0, an, bn, a, T_used)
    S_expr = None
    if build_symbolic_series:
        try:
            S_expr = build_series_expr(x, a0, an, bn, a, T_used)
        except Exception:
            S_expr = None

    # -------- Datos para graficar (en un periodo) --------
    aa = float(sp.N(a))
    bb = float(sp.N(b))
    xs = np.linspace(aa, bb, samples, endpoint=False)

    # Evitar evaluar exactamente en endpoints (ayuda en discontinuidades)
    eps = 1e-9 * (bb - aa)
    xs = np.clip(xs, aa + eps, bb - eps)

    ys_f = np.array([f_base(float(t)) for t in xs], dtype=float)
    ys_s = np.array([S(float(t)) for t in xs], dtype=float)
    err = ys_f - ys_s

    plot_data = {
        "x": xs,
        "f": ys_f,
        "S": ys_s,
        "err": err,
        "an_float": [float(sp.N(v)) for v in an],
        "bn_float": [float(sp.N(v)) for v in bn],
    }

    report = {
        "status": "ok",
        "entrada": input_desc,
        "intervalo": {"a": a, "b": b, "T": T_used},
        "N": N,
        "método": method_used,
        "a0": a0,
        "an": an,
        "bn": bn,
        "S_expr": S_expr,
        "nota": "Si hay discontinuidades (cuadrada, pulso, escalón), es normal ver Gibbs cerca de los saltos."
    }

    return FourierResult(
        status="ok", message="",
        a=a, b=b, T=T_used, N=N, method_used=method_used,
        a0=a0, an=an, bn=bn,
        f_callable=f_base, s_callable=S,
        plot_data=plot_data,
        report=report
    )


def format_fourier_report(fr: FourierResult) -> str:
    if fr.status != "ok":
        return f"[ERROR] {fr.message}"

    import sympy as sp

    lines = []
    lines.append("=== FOURIER (Reporte) ===")
    lines.append(f"Intervalo: [a,b] = [{sp.simplify(fr.a)}, {sp.simplify(fr.b)}],  T = {sp.simplify(fr.T)}")
    lines.append(f"N = {fr.N}, método = {fr.method_used}")
    lines.append("")
    lines.append("Entrada:")
    for k, v in fr.report.get("entrada", {}).items():
        lines.append(f"  - {k}: {v}")

    lines.append("\nCoeficientes:")
    lines.append(f"  a0 = {sp.simplify(fr.a0)}")
    for i, v in enumerate(fr.an, start=1):
        lines.append(f"  a{i} = {sp.simplify(v)}")
    for i, v in enumerate(fr.bn, start=1):
        lines.append(f"  b{i} = {sp.simplify(v)}")

    S_expr = fr.report.get("S_expr", None)
    if S_expr is not None:
        lines.append("\nSerie parcial S_N(x):")
        lines.append(f"  S_N(x) = {sp.simplify(S_expr)}")

    lines.append("\nNota:")
    lines.append("  " + fr.report.get("nota", ""))

    lines.append("=========================")
    return "\n".join(lines)