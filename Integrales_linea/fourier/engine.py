from __future__ import annotations
import sympy as sp

from .types import FourierResult

from .signals import SignalSpec, build_signal_callable
from .series import build_series_callable, build_series_expr
from .coefficients import compute_coefficients

def compute_fourier(signal: SignalSpec, n_harmonics: int) -> FourierResult:
    """
    Motor principal que coordina el cálculo de coeficientes y la creación de lsa funciones evaluables para la serie
    """
    # 1. Extraer o inferir datos del intervalo y símbolos
    # Si vienen de una fórmula matemática en el main:
    try:
        a = signal.lower_limit if signal.lower_limit is not None else sp.sympify(0)
        b = signal.upper_limit if signal.upper_limit is not None else sp.sympify(1)
        x = signal.symbol if signal.symbol is not None else sp.Symbol('x')

        _T_used = sp.simplify(b - a)

        # 2. Calcular Coeficientes (usando tu módulo coefficients.py)
        # Pasamos la expresión si existe (para integración simbólica/numérica)

        res = compute_coefficients(
            x=x, a=a, b=b, n_harmonics=n_harmonics,
            expr=signal.expression
        )
        a0, an, bn = res[0], res[1], res[2]
        # 3. Generar funciones evaluables para el Plotter y el Main
        # f_base es la función original periódica
        af, bf = float(sp.N(a)), float(sp.N(b))
        f_base = build_signal_callable(signal, af, bf)

        # s_math es la suma de la serie S_N(x)
        s_math = build_series_callable(a0, an, bn, a, _T_used)

        # 4. Preparar el reporte para el objeto FourierResult
        report = {
            "entrada": {
                "f(x)": str(signal.expression) if signal.expression else signal.name,
                "Límites": f"[{a}, {b}]",
                "Armónicos": n_harmonics
            },
            "a0": a0,
            "an": an,
            "bn": bn,
            "S_expr": build_series_expr(x, a0, an, bn, a, _T_used)
        }

        return FourierResult(
            status="ok", message="",
            a=a, b=b, T=_T_used, n_harmonics=n_harmonics,
            method_used="auto",
            a0=a0, an=an, bn=bn,
            f_callable=f_base, s_callable=s_math,
            plot_data=None,  # Se llena en el plotter si es necesario
            report=report
        )

    except Exception as e:
        return FourierResult(
            status="error", message=f"Error en intervalo: {str(e)}",
            a=sp.nan, b=sp.nan, T=sp.nan, n_harmonics=n_harmonics,
            method_used="none", a0=sp.nan, an=[], bn=[],
            f_callable=None, s_callable=None, plot_data=None, report={}
        )