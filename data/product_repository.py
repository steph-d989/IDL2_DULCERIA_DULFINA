""" import os
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
 """

from typing import List, Optional
from datetime import datetime
import pandas as pd
from models.product import Product
from data.supabase_client import get_client

_TABLE = "products"

def _to_df(rows: List[dict]) -> pd.DataFrame:
    return pd.DataFrame(rows or [])

def list_products_df() -> pd.DataFrame:
    """DataFrame para UI (ordenado por ts desc)."""
    sb = get_client()
    res = sb.table(_TABLE).select("*").order("ts", desc=True).execute()
    df = _to_df(res.data)
    return df

def insert_product(p: Product) -> None:
    sb = get_client()
    payload = {
        "nombre": p.nombre,
        "precio": p.precio,
        "categorias": p.categorias,   # text[] en Postgres
        "en_venta": p.en_venta,
        "ts": p.ts.isoformat()
    }
    sb.table(_TABLE).insert(payload).execute()

def update_product(
    id_: int, nombre: str, precio: float, categorias: List[str], en_venta: bool
) -> None:
    sb = get_client()
    payload = {
        "nombre": nombre.strip(),
        "precio": round(float(precio), 2),
        "categorias": sorted(list(set(categorias))),
        "en_venta": bool(en_venta),
    }
    sb.table(_TABLE).update(payload).eq("id", id_).execute()

def delete_product(id_: int) -> None:
    sb = get_client()
    sb.table(_TABLE).delete().eq("id", id_).execute()

def get_product_by_id(id_: int) -> Optional[Product]:
    sb = get_client()
    res = sb.table(_TABLE).select("*").eq("id", id_).single().execute()
    row = res.data
    if not row:
        return None
    return Product(
        id=row["id"],
        nombre=row["nombre"],
        precio=float(row["precio"]),
        categorias=list(row["categorias"] or []),
        en_venta=bool(row["en_venta"]),
        ts=datetime.fromisoformat(row["ts"].replace("Z","")) if isinstance(row["ts"], str) else row["ts"]
    )
