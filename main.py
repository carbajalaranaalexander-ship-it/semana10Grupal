#!/usr/bin/env python3
"""Orquestador CLI del Sistema de Gestión de Productos - IS093A Semana 10."""

from models.producto import Electronico, Libro
from utils.validators import validar_numero, validar_texto, validar_categoria, formatear_precio
from utils.exceptions import ValidationError, NotFoundError


# ─────────────────────────────────────────────
# Menú
# ─────────────────────────────────────────────
def menu() -> str:
    print("\n=== GESTIÓN DE PRODUCTOS (CLI) ===")
    print("1. Agregar Producto")
    print("2. Listar Productos")
    print("3. Calcular Precio Final")
    print("4. Eliminar Producto")
    print("5. Salir")
    return input("Opción > ").strip()


# ─────────────────────────────────────────────
# Helpers de entrada
# ─────────────────────────────────────────────
def _pedir(prompt: str) -> str:
    return input(prompt).strip()


def _agregar_electronico(inventario: dict, contador_id: int) -> int:
    nombre = validar_texto(_pedir("  Nombre: "), "nombre")
    precio = validar_numero(_pedir("  Precio base (S/): "), float, min_val=0.01)
    stock = validar_numero(_pedir("  Stock: "), int, min_val=0)
    garantia = validar_numero(_pedir("  Garantía (meses, 1-120): "), int, min_val=1, max_val=120)
    descuento_raw = _pedir("  Descuento (0.0-1.0, Enter=0): ") or "0"
    descuento = validar_numero(descuento_raw, float, min_val=0.0, max_val=1.0)

    producto = Electronico(nombre, precio, stock, garantia, descuento)
    inventario[contador_id] = producto
    print(f"✅ Electrónico agregado con ID {contador_id}.")
    return contador_id + 1


def _agregar_libro(inventario: dict, contador_id: int) -> int:
    nombre = validar_texto(_pedir("  Nombre: "), "nombre")
    precio = validar_numero(_pedir("  Precio base (S/): "), float, min_val=0.01)
    stock = validar_numero(_pedir("  Stock: "), int, min_val=0)
    autor = validar_texto(_pedir("  Autor: "), "autor")
    es_texto_raw = _pedir("  ¿Es libro de texto? (s/n): ").lower()
    es_texto = es_texto_raw in ("s", "si", "sí", "yes", "y")
    descuento_raw = _pedir("  Descuento (0.0-1.0, Enter=0): ") or "0"
    descuento = validar_numero(descuento_raw, float, min_val=0.0, max_val=1.0)

    producto = Libro(nombre, precio, stock, autor, es_texto, descuento)
    inventario[contador_id] = producto
    print(f"✅ Libro agregado con ID {contador_id}.")
    return contador_id + 1


# ─────────────────────────────────────────────
# Acciones del menú
# ─────────────────────────────────────────────
def accion_agregar(inventario: dict, contador_id: int) -> int:
    categoria = validar_categoria(_pedir("  Categoría (electronico/libro): "))
    if categoria == "electronico":
        return _agregar_electronico(inventario, contador_id)
    return _agregar_libro(inventario, contador_id)


def accion_listar(inventario: dict) -> None:
    if not inventario:
        print("⚠️  Inventario vacío.")
        return
    print(f"\n{'ID':<5} {'Descripción'}")
    print("-" * 70)
    for id_p, producto in inventario.items():
        print(f"{id_p:<5} {producto}")


def accion_precio_final(inventario: dict) -> None:
    id_raw = _pedir("  ID del producto: ")
    id_p = validar_numero(id_raw, int, min_val=1)
    if id_p not in inventario:
        raise NotFoundError(id_p)
    producto = inventario[id_p]
    precio = producto.calcular_precio_final()
    print(f"💰 Precio final de '{producto.nombre}': {formatear_precio(precio)}")


def accion_eliminar(inventario: dict) -> None:
    id_raw = _pedir("  ID a eliminar: ")
    id_p = validar_numero(id_raw, int, min_val=1)
    if id_p not in inventario:
        raise NotFoundError(id_p)
    nombre = inventario[id_p].nombre
    del inventario[id_p]
    print(f"🗑  Producto '{nombre}' (ID {id_p}) eliminado.")


# ─────────────────────────────────────────────
# Orquestador principal
# ─────────────────────────────────────────────
def main() -> None:
    inventario: dict = {}   # {id: objeto_producto}
    contador_id = 1

    while True:
        try:
            opcion = menu()

            if opcion == "1":
                contador_id = accion_agregar(inventario, contador_id)

            elif opcion == "2":
                accion_listar(inventario)

            elif opcion == "3":
                accion_precio_final(inventario)

            elif opcion == "4":
                accion_eliminar(inventario)

            elif opcion == "5":
                print("👋 Cerrando sistema...")
                break

            else:
                raise ValidationError("Opción inválida. Elija entre 1 y 5.")

        except ValidationError as e:
            print(f"⚠️  {e}")

        except NotFoundError as e:
            print(f"🔍 {e}")

        except Exception as e:
            print(f"❌ Error inesperado: {e}")

        finally:
            # Cleanup / log opcional por iteración
            pass


if __name__ == "__main__":
    main()
