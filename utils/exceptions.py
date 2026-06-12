"""Excepciones personalizadas del dominio."""


class AppError(Exception):
    """Base para todas las excepciones del sistema."""


class ValidationError(AppError):
    """Se lanza cuando un dato ingresado no cumple las reglas de validación."""

    def __init__(self, mensaje: str):
        super().__init__(f"Error de validación: {mensaje}")


class NotFoundError(AppError):
    """Se lanza cuando no se encuentra un producto por ID."""

    def __init__(self, id_producto: int):
        super().__init__(f"Producto con ID {id_producto} no encontrado")
