from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Product:
    id: Optional[int]
    nombre: str
    precio: float
    categorias: List[str]
    en_venta: bool
    ts: datetime
