# Integrales_linea/fourier/signals.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict
import math


def _wrap_to_period(x: float, a: float, T: float) -> float:
    """Mapea x a [a, a+T)."""
    return a + ((x - a) % T)


@dataclass
class SignalSpec:
    name: str
    params: Dict[str, float]


def available_signals() -> list[str]:
    return [
        "square", "triangle", "sawtooth", "pulse",
        "sine", "rectified_sine"
    ]


def build_signal_callable(spec: SignalSpec, a: float, b: float) -> Callable[[float], float]:
    """
    Devuelve f(x) periódica con periodo T=b-a (aplicada sobre el intervalo base [a,b]).
    Parámetros comunes:
      A (amplitud), offset (DC), phase (desplazamiento en x)

    square:
      duty (0..1), hi, lo

    pulse:
      width (0..1), start (0..1), hi, lo

    sawtooth:
      rampa de -A a A

    triangle:
      triangular en [-A, A]

    rectified_sine:
      mode="half" o "full"
    """
    T = b - a
    if T <= 0:
        raise ValueError("El intervalo debe cumplir b > a")

    name = spec.name.lower()
    p = spec.params

    A = float(p.get("A", 1.0))
    offset = float(p.get("offset", 0.0))
    phase = float(p.get("phase", 0.0))  # desplazamiento horizontal

    def u_of(x: float) -> float:
        # u en [0,1)
        xx = _wrap_to_period(x - phase, a, T)
        return (xx - a) / T

    if name in ("sine", "sin", "seno"):
        w = 2 * math.pi
        return lambda x: offset + A * math.sin(w * u_of(x))

    if name in ("rectified_sine", "seno_rectificado"):
        mode = str(p.get("mode", "full")).lower()  # "half" o "full"
        w = 2 * math.pi
        if mode.startswith("h"):
            return lambda x: offset + max(0.0, A * math.sin(w * u_of(x)))
        else:
            return lambda x: offset + abs(A * math.sin(w * u_of(x)))

    if name in ("square", "cuadrada"):
        duty = float(p.get("duty", 0.5))
        hi = float(p.get("hi", A))
        lo = float(p.get("lo", -A))
        return lambda x: offset + (hi if u_of(x) < duty else lo)

    if name in ("pulse", "pulso"):
        width = float(p.get("width", 0.1))
        start = float(p.get("start", 0.0))
        hi = float(p.get("hi", A))
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

    if name in ("sawtooth", "diente", "diente_de_sierra"):
        # rampa de -A a A
        return lambda x: offset + (2 * A * u_of(x) - A)

    if name in ("triangle", "triangular"):
        def tri(x: float) -> float:
            u = u_of(x)
            if u < 0.5:
                y = 4 * A * u - A
            else:
                y = -4 * A * u + 3 * A
            return offset + y
        return tri

    raise ValueError(f"Señal no soportada: {spec.name}")