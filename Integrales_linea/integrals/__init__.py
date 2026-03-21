# Exporta lo útil
from .contours import CircleContour, PolygonContour
from .engine import integrate_by_residues
from .param_integrator import integrate_parametric

__all__ = [
    'CircleContour',
    'PolygonContour',
    'integrate_by_residues',
    'integrate_parametric'
]