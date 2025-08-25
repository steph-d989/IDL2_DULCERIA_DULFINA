""" from services.product_service import validate_and_create
from data.product_repository import save_product

def create_product(nombre: str, precio, categorias: list, en_venta_label: str):
    product = validate_and_create(nombre, precio, categorias, en_venta_label)
    save_product(product)
    return product
 """

from typing import List, Optional
import pandas as pd

from services.product_service import build_product, validate
from data.product_repository import (
    list_products_df, insert_product, update_product, delete_product, get_product_by_id
)
from models.product import Product

# CREATE
def create_product(nombre: str, precio, categorias: List[str], en_venta_label: str) -> Product:
    product = build_product(nombre, precio, categorias, en_venta_label)
    insert_product(product)
    return product

# READ (lista para UI)
def list_products() -> pd.DataFrame:
    return list_products_df()

# UPDATE
def edit_product(
    id_: int, nombre: str, precio, categorias: List[str], en_venta_label: str
) -> None:
    err = validate(nombre, precio, categorias)
    if err:
        raise ValueError(err)
    en_venta = (en_venta_label == "Sí") if isinstance(en_venta_label, str) else bool(en_venta_label)
    update_product(id_, nombre, float(precio), categorias, en_venta)

# DELETE
def remove_product(id_: int) -> None:
    delete_product(id_)

# READ (uno)
def get_product(id_: int) -> Optional[Product]:
    return get_product_by_id(id_)
