from services.product_service import validate_and_create
from data.product_repository import save_product

def create_product(nombre: str, precio, categorias: list, en_venta_label: str):
    product = validate_and_create(nombre, precio, categorias, en_venta_label)
    save_product(product)
    return product
