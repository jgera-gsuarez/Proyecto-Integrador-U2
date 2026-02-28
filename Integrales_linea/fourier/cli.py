# Integrales_linea/fourier/cli.py
from __future__ import annotations
from typing import Dict, Any, Tuple

def _ask(prompt: str, default: str | None = None) -> str:
    s = input(prompt).strip()
    return s if s else (default if default is not None else "")

def _ask_int(prompt: str, default: int | None = None) -> int:
    while True:
        s = _ask(prompt, str(default) if default is not None else None)
        try:
            return int(s)
        except ValueError:
            print("  [!] Ingresa un entero válido.")

def _ask_float(prompt: str, default: float | None = None) -> float:
    while True:
        s = _ask(prompt, str(default) if default is not None else None)
        try:
            return float(s)
        except ValueError:
            print("  [!] Ingresa un número válido (ej. 0.5).")

def _ask_choice(prompt: str, choices: Dict[str, str], default_key: str) -> str:
    """
    choices: {"1":"square", "2":"triangle", ...}
    retorna el value (ej. "square")
    """
    while True:
        s = _ask(prompt, default_key)
        if s in choices:
            return choices[s]
        print(f"  [!] Opción inválida. Elige una de: {', '.join(choices.keys())}")

def _ask_yes_no(prompt: str, default_yes: bool = True) -> bool:
    d = "s" if default_yes else "n"
    s = _ask(prompt + f" [s/n] ({d}): ", d).lower()
    return s.startswith("s")

def ask_interval() -> Dict[str, str]:
    print("\nIntervalo base [a, b] (se extiende periódicamente con T=b-a)")
    a = _ask("  a = ", "-pi")
    b = _ask("  b = ", "pi")
    return {"a": a, "b": b}

def ask_method() -> str:
    print("\nMétodo de integración para coeficientes:")
    print("  1) auto (simbólico si se puede; si no numérico)  [recomendado]")
    print("  2) symbolic (solo simbólico)")
    print("  3) numeric (solo numérico)")
    ch = _ask_choice("Elige (1/2/3): ", {"1": "auto", "2": "symbolic", "3": "numeric"}, "1")
    return ch

def ask_signal_menu() -> Dict[str, Any]:
    """
    Retorna input_spec listo para compute_fourier():
      {"type":"signal", "name":..., "params":{...}}
    """
    print("\n=== Señales disponibles ===")
    print("  1) Cuadrada")
    print("  2) Triangular")
    print("  3) Diente de sierra")
    print("  4) Pulso")
    print("  5) Seno")
    print("  6) Seno rectificado")

    name = _ask_choice(
        "Elige señal (1..6): ",
        {
            "1": "square",
            "2": "triangle",
            "3": "sawtooth",
            "4": "pulse",
            "5": "sine",
            "6": "rectified_sine"
        },
        "1"
    )

    params: Dict[str, Any] = {}

    # Parámetros comunes
    # Nota: en tu signals.py se usan A, offset y phase en varias señales.
    def ask_common(include_A: bool = True):
        if include_A:
            params["A"] = _ask_float("  Amplitud A: ", 1.0)
        params["offset"] = _ask_float("  Offset (DC): ", 0.0)
        params["phase"] = _ask_float("  Phase (desplazamiento en x): ", 0.0)

    if name == "square":
        # Para cuadrada es más intuitivo hi/lo/duty
        params["hi"] = _ask_float("  Valor alto (hi): ", 1.0)
        params["lo"] = _ask_float("  Valor bajo (lo): ", 0.0)
        params["duty"] = _ask_float("  Duty (0..1): ", 0.5)

    elif name == "pulse":
        params["hi"] = _ask_float("  Valor alto (hi): ", 1.0)
        params["lo"] = _ask_float("  Valor bajo (lo): ", 0.0)
        params["start"] = _ask_float("  Inicio (start) en fracción del periodo [0..1): ", 0.0)
        params["width"] = _ask_float("  Ancho (width) en fracción del periodo (0..1): ", 0.1)

    elif name == "triangle":
        ask_common(include_A=True)

    elif name == "sawtooth":
        ask_common(include_A=True)

    elif name == "sine":
        ask_common(include_A=True)

    elif name == "rectified_sine":
        ask_common(include_A=True)
        print("  Modo rectificado:")
        print("    1) half  (media onda: max(0, sin))")
        print("    2) full  (onda completa: abs(sin))")
        mode = _ask_choice("  Elige (1/2): ", {"1": "half", "2": "full"}, "2")
        params["mode"] = mode

    return {"type": "signal", "name": name, "params": params}

def ask_expr_or_piecewise() -> Dict[str, Any]:
    print("\nTipo de función:")
    print("  1) Expresión (ej. x, abs(x), sin(x))")
    print("  2) Por tramos (ej. 0 : -pi < x < 0; 1 : 0 < x < pi)")
    ch = _ask_choice("Elige (1/2): ", {"1": "expr", "2": "piecewise"}, "1")
    if ch == "expr":
        expr = _ask("  f(x) = ", "x")
        return {"type": "expr", "expr": expr}
    else:
        spec = _ask("  Tramos = ", "0 : -pi < x < 0; 1 : 0 < x < pi")
        return {"type": "piecewise", "spec": spec}

def run_fourier_menu() -> Tuple[Dict[str, Any], Dict[str, str], int, str, int]:
    """
    Retorna: (input_spec, interval, N, method, samples)
    """
    print("\n=== Módulo Fourier (CLI) ===")
    print("  El usuario define [a,b]. Periodo T=b-a.")
    print("  Variable: x")

    interval = ask_interval()
    N = _ask_int("\nNúmero de términos N: ", 10)
    method = ask_method()
    samples = _ask_int("\nPuntos para graficar (samples): ", 2000)

    print("\nFuente de la función:")
    print("  1) Función (expresión o por tramos)")
    print("  2) Señal (menú)")
    src = _ask_choice("Elige (1/2): ", {"1": "func", "2": "signal"}, "1")

    if src == "signal":
        input_spec = ask_signal_menu()
    else:
        input_spec = ask_expr_or_piecewise()

    return input_spec, interval, N, method, samples