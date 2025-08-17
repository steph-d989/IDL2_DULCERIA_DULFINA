from datetime import datetime
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
