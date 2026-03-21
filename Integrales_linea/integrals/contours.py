from dataclasses import dataclass
from typing import List, Tuple
import numpy as np

DEFAULT_TOL = 1e-9

def to_complex(z_sympy) -> complex:
    # evalf() -> float aproximado, luego a complex
    zc = complex(z_sympy.evalf())
    return zc

@dataclass(frozen=True)
class CircleContour:
    center_sym: object  # SymPy expr
    radius: float
    orientation: int = +1  # +1 anticlockwise, -1 clockwise
    tol: float = DEFAULT_TOL

    def center(self) -> complex:
        return to_complex(self.center_sym)

    def contains(self, z_sym) -> bool:
        z = to_complex(z_sym)
        c = self.center()
        return abs(z - c) < (self.radius - self.tol)

    def on_boundary(self, z_sym) -> bool:
        z = to_complex(z_sym)
        c = self.center()
        return abs(abs(z - c) - self.radius) <= self.tol

    def bounds(self) -> Tuple[float, float, float, float]:
        c = self.center()
        return (c.real - self.radius, c.real + self.radius, c.imag - self.radius, c.imag + self.radius)


@dataclass(frozen=True)
class PolygonContour:
    vertices_sym: List[object]  # list of SymPy complex
    orientation: int = +1
    tol: float = DEFAULT_TOL

    def vertices(self) -> List[complex]:
        return [to_complex(v) for v in self.vertices_sym]

    def bounds(self) -> Tuple[float, float, float, float]:
        vs = self.vertices()
        xs = [v.real for v in vs]
        ys = [v.imag for v in vs]
        return (min(xs), max(xs), min(ys), max(ys))

    def on_boundary(self, z_sym) -> bool:
        # chequeo por distancia a segmentos (aprox)
        z = to_complex(z_sym)
        vs = self.vertices()
        n = len(vs)
        for i in range(n):
            a = vs[i]
            b = vs[(i+1) % n]
            if _point_on_segment(z, a, b, self.tol):
                return True
        return False

    def contains(self, z_sym) -> bool:
        # Ray casting (punto en polígono). Frontera se maneja aparte.
        z = to_complex(z_sym)
        x, y = z.real, z.imag
        vs = self.vertices()
        inside = False
        n = len(vs)
        for i in range(n):
            x1, y1 = vs[i].real, vs[i].imag
            x2, y2 = vs[(i+1) % n].real, vs[(i+1) % n].imag
            # check cruce con rayo horizontal a la derecha
            intersects = ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1 + 0.0) + x1)
            if intersects:
                inside = not inside
        return inside

def _point_on_segment(p: complex, a: complex, b: complex, tol: float) -> bool:
    # distancia de p al segmento ab
    ax, ay = a.real, a.imag
    bx, by = b.real, b.imag
    px, py = p.real, p.imag
    abx, aby = bx-ax, by-ay
    apx, apy = px-ax, py-ay
    ab2 = abx*abx + aby*aby
    if ab2 == 0:
        return abs(p-a) <= tol
    t = (apx*abx + apy*aby) / ab2
    t = max(0.0, min(1.0, t))
    closest = complex(ax + t*abx, ay + t*aby)
    return abs(p - closest) <= tol

#def param_pieces()