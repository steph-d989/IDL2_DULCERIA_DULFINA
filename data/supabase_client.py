import os
from typing import Any
try:
    import streamlit as st
except Exception:
    st = None  # permite usar fuera de Streamlit

from supabase import create_client, Client

def get_env(name: str, default: str = "") -> str:
    # Intenta leer de st.secrets y luego de variables de entorno
    if st is not None:
        try:
            val = st.secrets[name]
            if val:
                return val
        except Exception:
            pass
    return os.getenv(name, default)

_SUPABASE_URL = get_env("SUPABASE_URL")
_SUPABASE_KEY = get_env("SUPABASE_KEY")

if not _SUPABASE_URL or not _SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL / SUPABASE_KEY no configurados en secrets o variables de entorno.")

def get_client() -> Client:
    return create_client(_SUPABASE_URL, _SUPABASE_KEY)
