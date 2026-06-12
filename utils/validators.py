"""Funciones de validación y formateo de entradas."""

from .exceptions import ValidationError

CATEGORIAS_VALIDAS = ["electronico", "libro"]


def validar_numero(
    valor: str,
    tipo: type = float,
    min_val: float = 0,
    max_val: float | None = None,
) -> float | int:
    """Convierte y valida un valor numérico dentro de un rango."""
    try:
        num = tipo(valor)
        if num < min_val or (max_val is not None and num > max_val):
            raise ValidationError(f"Valor fuera de rango: {min_val}-{max_val}")
        return num
    except ValueError:
        raise ValidationError(f"Formato numérico inválido: '{valor}'")


def validar_texto(valor: str, campo: str = "campo") -> str:
    """Valida que un texto no esté vacío."""
    texto = valor.strip()
    if not texto:
        raise ValidationError(f"El {campo} no puede estar vacío")
    return texto


def validar_categoria(categoria: str) -> str:
    """Valida y normaliza la categoría del producto."""
    cat = categoria.strip().lower()
    if cat not in CATEGORIAS_VALIDAS:
        raise ValidationError(
            f"Categoría inválida: '{categoria}'. Use: {', '.join(CATEGORIAS_VALIDAS)}"
        )
    return cat


def formatear_precio(precio: float) -> str:
    """Devuelve el precio formateado en soles."""
    return f"S/ {precio:,.2f}"
