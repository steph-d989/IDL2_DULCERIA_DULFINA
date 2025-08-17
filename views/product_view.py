import streamlit as st
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
