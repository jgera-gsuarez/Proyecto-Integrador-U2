# Integrales_linea/fourier/signals.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional
import sympy as sp
import math


def _wrap_to_period(x: float, a: float, t: float) -> float:
    """Mapea x a [a, a+T)."""
    return a + ((x - a) % t)


@dataclass
class SignalSpec:
    """Para funciones matemáticas puras de SymPy"""
    expression: Optional[sp.Expr] = None
    symbol: Optional[sp.Symbol] = None
    lower_limit: Optional[sp.Expr] = None
    upper_limit: Optional[sp.Expr] = None

    #Señales predefinidas
    name: str = "custom"
    params: Dict[str, float] = field(default_factory=dict)


def available_signals() -> list[str]:
    return [
        "square", "triangle", "sawtooth", "pulse",
        "sine", "rectified_sine", "fórmula matemática"
    ]


def build_signal_callable(spec: SignalSpec, a: float, b: float) -> Callable[[float], float]:
    """
    Devuelve f(x) periódica con periodo T=b-a (aplicada sobre el intervalo base [a, b]).
    Parámetros comunes:
      A (amplitud), offset (DC), phase (desplazamiento en x)
    """
    _T = b - a
    if _T <= 0:
        raise ValueError("El intervalo debe cumplir b > a")

    if spec.expression is not None and spec.symbol is not None:
        f_numeric = sp.lambdify(spec.symbol, spec.expression, modules=["numpy", "math"])
        return lambda x: float(f_numeric(_wrap_to_period(x, a, _T)))

    name = spec.name.lower()
    p = spec.params

    _A = float(p.get("A", 1.0))
    offset = float(p.get("offset", 0.0))
    phase = float(p.get("phase", 0.0))  # desplazamiento horizontal

    def u_of(x: float) -> float:
        # u en [0,1)
        xx = _wrap_to_period(x - phase, a, _T)
        return (xx - a) / _T

    if name in ("sin", "seno"):
        w = 2 * math.pi
        return lambda x: offset + _A * math.sin(w * u_of(x))

    '''rectified_sine:
      mode="half" o "full"'''
    if name in ("rectified_sin", "seno_rectificado"):
        mode = str(p.get("mode", "full")).lower()  # "half" o "full"
        w = 2 * math.pi
        if mode.startswith("h"):
            return lambda x: offset + max(0.0, _A * math.sin(w * u_of(x)))
        else:
            return lambda x: offset + abs(_A * math.sin(w * u_of(x)))

    '''square:
      duty (0..1), hi, lo'''
    if name in ("square", "cuadrada"):
        duty = float(p.get("duty", 0.5))
        hi = float(p.get("hi", _A))
        lo = float(p.get("lo", -_A))
        return lambda x: offset + (hi if u_of(x) < duty else lo)

    '''pulse:
      width (0..1), start (0..1), hi, lo'''
    if name in ("pulse", "pulso"):
        width = float(p.get("width", 0.1))
        start = float(p.get("start", 0.0))
        hi = float(p.get("hi", _A))
        lo = float(p.get("lo", 0.0))

        def f(x: float) -> float:
            if width <= 0:
                return offset + lo
            u = u_of(x)
            end = (start + width) % 1.0
            if start < end:
                on = (start <= u < end)
            else:
                on = (u >= start or u < end)
            return offset + (hi if on else lo)

        return f

    '''sawtooth:
      rampa de -A a A'''
    if name in ("sawtooth", "diente", "diente_de_sierra"):
        # rampa de -A a A
        return lambda x: offset + (2 * _A * u_of(x) - _A)

    '''triangle:
      triangular en [-A, A]'''
    if name in ("triangle", "triangular"):
        def tri(x: float) -> float:
            u = u_of(x)
            if u < 0.5:
                y = 4 * _A * u - _A
            else:
                y = -4 *_A * u + 3 * _A
            return offset + y
        return tri

    raise ValueError(f"Señal no soportada: {spec.name}")