from dataclasses import dataclass
from typing import List, Tuple
import numpy as np
import sympy as sp

DEFAULT_TOL = 1e-9

def to_complex(z_sympy: sp.Expr) -> complex:
    # evalf() -> float aproximado, luego a complex
    zc = complex(z_sympy.evalf())
    return zc

@dataclass(frozen=True)
class CircleContour:
    center_sym: sp.Expr  # SymPy expr
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
        return (c.real - self.radius, c.real + self.radius,
                c.imag - self.radius, c.imag + self.radius)

    def get_plot_points(self, n=200):
        #Genera puntos para el plotter
        t = np.linspace(0, 2*np.pi,n)
        c = self.center()
        # Si la orientación es negativa, invertimos el orden de los puntos
        if self.orientation == -1:
            t = np.flip(t)
        return c + self.radius * (np.cos(t) + 1j * np.sin(t))

@dataclass(frozen=True)
class PolygonContour:
    vertices_sym: List[sp.Expr]  # list of SymPy complex
    orientation: int = +1
    tol: float = DEFAULT_TOL

    def vertices(self) -> List[complex]:
        return [to_complex(v) for v in self.vertices_sym]

    def bounds(self) -> Tuple[float, float, float, float]:
        vs = self.vertices()
        xs = [v.real for v in vs]
        ys = [v.imag for v in vs]
        return min(xs), max(xs), min(ys), max(ys)

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

    def get_plot_points(self, n_per_segment=50):
        #Genera puntos conectando los vértices
        vs = self.vertices()
        if not vs: return np.array([])

        # Cerramos el polígono volviendo al primer vértice
        v_ext = vs + [vs[0]]
        if self.orientation == -1:
            v_ext = list(reversed(v_ext))

        points = []
        for i in range(len(v_ext) - 1):
            segment = np.linspace(v_ext[i], v_ext[i + 1], n_per_segment)
            points.extend(segment[:-1])
        points.append(v_ext[-1])
        return np.array(points)

def _point_on_segment(p: complex, a: complex, b: complex, tol: float) -> bool:
    # Lógica de distancia punto a segmento
    cross_product = (p.imag - a.imag) * (b.real - a.real) - (p.real - a.real) * (b.imag - a.imag)
    if abs(cross_product) > tol: return False
    dot_product = (p.real - a.real) * (b.real - a.real) + (p.imag - a.imag) * (b.imag - a.imag)
    if dot_product < 0: return False
    squared_length = (b.real - a.real) ** 2 + (b.imag - a.imag) ** 2
    if dot_product > squared_length: return False
    return True