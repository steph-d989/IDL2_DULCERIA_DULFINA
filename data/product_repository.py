import os
import pandas as pd
from models.product import Product

DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "products.csv")

def ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def load_products() -> pd.DataFrame:
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH, encoding="utf-8")
    return pd.DataFrame(columns=["nombre", "precio", "categorias", "en_venta", "ts"])

def save_product(product: Product):
    ensure_dir()
    df = load_products()
    new_row = {
        "nombre": product.nombre,
        "precio": product.precio,
        "categorias": ",".join(product.categorias),
        "en_venta": product.en_venta,
        "ts": product.ts
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(CSV_PATH, index=False, encoding="utf-8")
