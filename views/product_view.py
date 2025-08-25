""" import streamlit as st
from services.product_service import ALLOWED_CATEGORIES
from controllers.product_controller import create_product

def render_form():
    st.title("Confitería Dulcino - Registro de productos")

    with st.form("form-producto", clear_on_submit=True):
        col1, col2 = st.columns([2,1])
        with col1:
            nombre = st.text_input("Nombre del producto")
        with col2:
            precio = st.number_input("Precio (S/)", min_value=0.0, max_value=998.99, step=0.10, format="%.2f")

        categorias = st.multiselect("Categorias", ALLOWED_CATEGORIES)
        en_venta_label = st.radio("¿El producto está en venta?", options=["Sí", "No"], horizontal=True)

        submitted = st.form_submit_button("Guardar")

        if submitted:
            try:
                product = create_product(nombre, precio, categorias, en_venta_label)
                st.success("Felicidades su producto se agregó.")
            except Exception as e:
                if "precio" in str(e).lower():
                    st.error("Por favor verifique el campo del precio.")
                else:
                    st.error("Lo sentimos no pudo crear este producto.")
 """

import streamlit as st
from controllers.product_controller import (
    create_product, list_products, edit_product, remove_product, get_product
)
from services.product_service import ALLOWED_CATEGORIES

def render_form():
    st.title("Confitería Dulcino - Registro de productos")

    # -------- Crear Producto --------
    st.header("Agregar Producto")
    with st.form("form-add", clear_on_submit=True):
        c1, c2 = st.columns([2,1])
        with c1:
            nombre = st.text_input("Nombre de producto")
        with c2:
            precio = st.number_input("Precio (S/)", min_value=0.01, max_value=998.99, step=0.10, format="%.2f")

        categorias = st.multiselect("Categorías", ALLOWED_CATEGORIES)
        en_venta_label = st.radio("¿En venta?", ["Sí", "No"], horizontal=True)

        submitted = st.form_submit_button("Guardar")

    if submitted:
        try:
            create_product(nombre, precio, categorias, en_venta_label)
            st.success("Felicidades, su producto se agregó.")
            st.rerun()
        except Exception as e:
            msg = str(e)
            if "precio" in msg.lower():
                st.error("Por favor verifique el campo precio.")
            else:
                st.error("Lo sentimos, no se pudo crear este producto.")
            st.info(msg)

    st.divider()

    # -------- Listar / Editar / Borrar --------
    st.header("Productos registrados")
    df = list_products()
    if df.empty:
        st.info("No hay productos aún.")
        return

    st.dataframe(df, use_container_width=True)

    # Selector para edición
    opciones = {
        f"{r['nombre']} - S/ {r['precio']} (id:{int(r['id'])})": int(r["id"])
        for _, r in df.iterrows()
    }
    etiqueta = st.selectbox("Selecciona para editar/eliminar", list(opciones.keys()))
    producto_id = int(opciones[etiqueta])

    fila = df[df["id"] == producto_id].iloc[0]

    with st.form("form-edit"):
        c1, c2 = st.columns([2,1])
        with c1:
            ed_nombre = st.text_input("Nombre", value=str(fila["nombre"]))
        with c2:
            ed_precio = st.number_input(
                "Precio (S/)",
                value=float(fila["precio"]),
                min_value=0.01, max_value=998.99, step=0.10, format="%.2f"
            )

        default_cats = list(fila["categorias"]) if isinstance(fila["categorias"], list) else []
        ed_categorias = st.multiselect("Categorías", ALLOWED_CATEGORIES, default=default_cats)

        ed_en_venta_label = st.radio(
            "¿En venta?", ["Sí", "No"],
            index=0 if bool(fila["en_venta"]) else 1,
            horizontal=True
        )

        colu1, colu2 = st.columns(2)
        with colu1:
            btn_update = st.form_submit_button("Guardar Cambios")
        with colu2:
            btn_delete = st.form_submit_button("Eliminar", type="primary")

        if btn_update:
            try:
                edit_product(producto_id, ed_nombre, ed_precio, ed_categorias, ed_en_venta_label)
                st.success("Producto actualizado.")
                st.rerun()
            except Exception as e:
                msg = str(e)
                if "precio" in msg.lower():
                    st.error("Por favor verifique el campo precio.")
                else:
                    st.error("Lo sentimos, no se pudo actualizar este producto.")
                st.info(msg)

        if btn_delete:
            try:
                remove_product(producto_id)
                st.success("Producto eliminado.")
                st.rerun()
            except Exception as e:
                st.error("No se pudo eliminar el producto.")
                st.info(str(e))
