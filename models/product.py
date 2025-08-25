""" from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Product:
    nombre: str
    precio: float
    categorias: List[str]
    en_venta: bool
    ts: datetime
 """

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
