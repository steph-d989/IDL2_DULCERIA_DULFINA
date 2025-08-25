""" from datetime import datetime
from models.product import Product

ALLOWED_CATEGORIES = [
    "Chocolates", "Caramelos", "Mashmelos", "Galletas", "Salados", "Gomas de mascar"
]

def validate_and_create(nombre: str, precio, categorias: list, en_venta_label: str) -> Product:
    # nombre
    if len(nombre.strip()) == 0 or len(nombre.strip()) > 20:
        raise ValueError("El nombre no puede estar vacío ni superar 20 caracteres.")

    # precio
    if precio is None:
        raise ValueError("Por favor verifique el campo del precio")
    try:
        p = float(precio)
    except Exception:
        raise ValueError("Por favor verifique en campo precio")
    if not (0 < p < 999):
        raise ValueError("El precio debe ser mayor a 0 y menor a 999.")

    # categorías
    if not categorias:
        raise ValueError("Debe elegir al menos una categoría.")
    for c in categorias:
        if c not in ALLOWED_CATEGORIES:
            raise ValueError(f"Categoría inválida: {c}")

    # en venta
    if en_venta_label not in ["Sí", "No"]:
        raise ValueError("Valor inválido para ¿está en venta?")

    return Product(
        nombre=nombre.strip(),
        precio=round(p, 2),
        categorias=sorted(list(set(categorias))),
        en_venta=(en_venta_label == "Sí"),
        ts=datetime.now()
    )
 """

from datetime import datetime
from typing import List, Optional
from models.product import Product

ALLOWED_CATEGORIES = [
    "Chocolates", "Caramelos", "Mashmelos", "Galletas", "Salados", "Gomas de mascar"
]

def validate(nombre: str, precio, categorias: List[str]) -> Optional[str]:
    # nombre
    if not nombre or len(nombre.strip()) == 0 or len(nombre.strip()) > 20:
        return "El nombre es obligatorio y debe tener ≤ 20 caracteres."

    # precio
    try:
        p = float(precio)
    except Exception:
        return "Por favor verifique el campo precio."
    if not (0 < p < 999):
        return "El precio debe ser mayor a 0 y menor a 999."

    # categorías
    if not categorias:
        return "Debe elegir al menos una categoría."
    for c in categorias:
        if c not in ALLOWED_CATEGORIES:
            return f"Categoría inválida: {c}"

    return None

def build_product(nombre: str, precio, categorias: List[str], en_venta_label: str) -> Product:
    err = validate(nombre, precio, categorias)
    if err:
        raise ValueError(err)

    return Product(
        id=None,
        nombre=nombre.strip(),
        precio=round(float(precio), 2),
        categorias=sorted(list(set(categorias))),
        en_venta=(en_venta_label == "Sí") if isinstance(en_venta_label, str) else bool(en_venta_label),
        ts=datetime.utcnow()
    )
