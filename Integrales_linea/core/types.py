import sympy as sp

def format_kv_block(title: str, kv: dict) -> str:
    lines = [f"=== {title} ==="]
    for k, v in kv.items():
        try:
            v = sp.simplify(v)
        except Exception:
            pass
        lines.append(f"{k}: {v}")
    return "\n".join(lines)

#ef convert_latex_to_pdf():
