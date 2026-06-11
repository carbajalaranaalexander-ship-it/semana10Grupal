"""Modelos del dominio: Producto, Electronico, Libro, DescuentoMixin."""

from __future__ import annotations
from typing import override

from utils.exceptions import ValidationError


# ─────────────────────────────────────────────
# Mixin de descuento (herencia múltiple opcional)
# ─────────────────────────────────────────────
class DescuentoMixin:
    """Añade capacidad de aplicar un porcentaje de descuento a cualquier producto."""

    _descuento: float = 0.0  # porcentaje, ej. 0.10 = 10 %

    @property
    def descuento(self) -> float:
        return self._descuento

    @descuento.setter
    def descuento(self, valor: float) -> None:
        if not (0.0 <= valor <= 1.0):
            raise ValidationError("El descuento debe estar entre 0.0 y 1.0")
        self._descuento = valor

    def aplicar_descuento(self, precio: float) -> float:
        return round(precio * (1 - self._descuento), 2)


# ─────────────────────────────────────────────
# Clase base
# ─────────────────────────────────────────────
class Producto:
    """Clase base abstracta para todos los productos."""

    def __init__(self, nombre: str, precio_base: float, stock: int) -> None:
        # Delegamos asignación a los setters para que disparen validaciones
        self.nombre = nombre          # usa @property → _nombre
        self.precio_base = precio_base  # usa @property → _precio_base
        self.stock = stock            # usa @property → _stock

    # ── nombre ──────────────────────────────
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        valor = valor.strip()
        if not valor:
            raise ValidationError("El nombre no puede estar vacío")
        self._nombre = valor

    # ── precio_base ─────────────────────────
    @property
    def precio_base(self) -> float:
        return self._precio_base

    @precio_base.setter
    def precio_base(self, valor: float) -> None:
        if valor <= 0:
            raise ValidationError("El precio base debe ser mayor a 0")
        self._precio_base = round(float(valor), 2)

    # ── stock ───────────────────────────────
    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if valor < 0:
            raise ValidationError("El stock no puede ser negativo")
        self._stock = int(valor)

    # ── métodos ─────────────────────────────
    def calcular_precio_final(self) -> float:
        raise NotImplementedError("Las subclases deben implementar este método")

    def __str__(self) -> str:
        from utils.validators import formatear_precio
        return (
            f"[{self.__class__.__name__}] {self.nombre} | "
            f"Base: {formatear_precio(self.precio_base)} | "
            f"Final: {formatear_precio(self.calcular_precio_final())} | "
            f"Stock: {self.stock}"
        )

    def __del__(self) -> None:
        print(f"🗑  Destruyendo instancia: {self._nombre}")


# ─────────────────────────────────────────────
# Clase derivada: Electronico
# ─────────────────────────────────────────────
class Electronico(DescuentoMixin, Producto):
    """Producto electrónico con garantía e IGV (18 %).
    MRO: Electronico → DescuentoMixin → Producto → object
    """

    IGV = 0.18

    def __init__(
        self,
        nombre: str,
        precio_base: float,
        stock: int,
        garantia_meses: int,
        descuento: float = 0.0,
    ) -> None:
        super().__init__(nombre, precio_base, stock)  # sigue MRO (llega a Producto)
        self.garantia_meses = garantia_meses          # @property protegido
        self.descuento = descuento                     # setter del Mixin

    # ── garantia_meses ──────────────────────
    @property
    def garantia_meses(self) -> int:
        return self._garantia_meses

    @garantia_meses.setter
    def garantia_meses(self, valor: int) -> None:
        if not (1 <= int(valor) <= 120):
            raise ValidationError("La garantía debe estar entre 1 y 120 meses")
        self._garantia_meses = int(valor)

    @override
    def calcular_precio_final(self) -> float:
        """Precio base + IGV (18 %). Si stock > 50 aplica descuento adicional del 5 %."""
        precio = self._precio_base * (1 + self.IGV)
        if self._stock > 50:
            precio *= 0.95
        precio = self.aplicar_descuento(precio)   # DescuentoMixin
        return round(precio, 2)

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | Garantía: {self.garantia_meses} meses"


# ─────────────────────────────────────────────
# Clase derivada: Libro
# ─────────────────────────────────────────────
class Libro(DescuentoMixin, Producto):
    """Libro con autor. Si es libro de texto aplica 10 % de descuento."""

    def __init__(
        self,
        nombre: str,
        precio_base: float,
        stock: int,
        autor: str,
        es_texto: bool = False,
        descuento: float = 0.0,
    ) -> None:
        super().__init__(nombre, precio_base, stock)
        self.__autor = self._validar_autor(autor)   # atributo privado (name-mangling)
        self._es_texto = es_texto
        self.descuento = descuento

    @staticmethod
    def _validar_autor(autor: str) -> str:
        autor = autor.strip()
        if not autor:
            raise ValidationError("El autor no puede estar vacío")
        return autor

    @property
    def autor(self) -> str:
        return self.__autor

    @override
    def calcular_precio_final(self) -> float:
        """Precio base - 10 % si es libro de texto, luego descuento opcional."""
        precio = self._precio_base
        if self._es_texto:
            precio *= 0.90
        precio = self.aplicar_descuento(precio)
        return round(precio, 2)

    def __str__(self) -> str:
        base = super().__str__()
        tipo = "Texto" if self._es_texto else "General"
        return f"{base} | Autor: {self.__autor} | Tipo: {tipo}"
