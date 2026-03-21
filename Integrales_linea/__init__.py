# utilidades compartidas
from .integrals.integrals_report import format_report#, format_kv_block
from .core.types import FourierResult
from .core.parsing import parse_expr_math, parse_number_math

# integrales complejas
from .integrals.contours import CircleContour, PolygonContour
from .integrals.engine import integrate_by_residues  # y luego integrate() si lo agregas
from .integrals.param_integrator import integrate_parametric, param_segment, param_arc

#Series de Fourier
from .fourier.coefficients import compute_coefficients
from .fourier.engine import compute_fourier
from .fourier.fourier_report import format_fourier_report
from .fourier.fourier_plotter import plot_fourier_result
from .fourier.signals import SignalSpec

__all__ = [
    'format_report',
    'FourierResult',
    'parse_expr_math',
    'parse_number_math',
    'CircleContour',
    'PolygonContour',
    'integrate_by_residues',
    'integrate_parametric',
    'param_segment',
    'param_arc',
    'compute_coefficients',
    'compute_fourier',
    'format_fourier_report',
    'plot_fourier_result',
    'SignalSpec'
]