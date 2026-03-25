# utilidades compartidas
#from .core. report import #, format_kv_block
from .core.parsing import parse_expr_math, parse_number_math
from .core.exporter import export_to_latex

# integrales complejas
from .integrals.contours import CircleContour, PolygonContour
from .integrals.engine import integrate_by_residues, integrate_parametric, param_segment, param_arc
from .integrals.integrals_plotter import plot_complex_contour
from .integrals.integrals_report import format_report

#Series de Fourier
from .fourier.coefficients import compute_coefficients
from .fourier.engine import compute_fourier
from .fourier.fourier_report import format_fourier_report
from .fourier.fourier_plotter import plot_fourier_result
from .fourier.signals import SignalSpec
from .fourier.types import FourierResult

__all__ = [
    'parse_expr_math', 'parse_number_math',
    'export_to_latex',
    'CircleContour', 'PolygonContour',
    'integrate_by_residues', 'integrate_parametric', 'param_segment', 'param_arc',
    'plot_complex_contour',
    'format_report',
    'compute_coefficients',
    'compute_fourier',
    'format_fourier_report',
    'plot_fourier_result',
    'SignalSpec',
    'FourierResult'
]