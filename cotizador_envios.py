# -*- coding: utf-8 -*-
"""
Created on Tue May  6 17:33:54 2025

@author: Maria Almeida Pizarr
"""

import streamlit as st
import pandas as pd
import math
from rapidfuzz import process
from fpdf import FPDF

# ======= CONFIGURACIÓN DE PRODUCTOS =======
PRECIO_LAMINA_UNIT = 8000
PROMO_LAMINA_12 = 90000
PESO_LAMINA = 0.1  # en kg
AREA_LAMINA = 0.7 * 0.77  # m²

PRECIO_ROLLO_UNIT = 35000
PROMO_ROLLO_3 = 100000
PESO_ROLLO = 0.5  # en kg
AREA_ROLLO = 10 * 0.45  # m²

# ======= CARGA DE DATOS =======
df_fletes = pd.read_excel("diccionario_fletes.xlsx")
ciudades = df_fletes["ciudad"].tolist()


def encontrar_ciudad(input_ciudad):
    input_ciudad = input_ciudad.strip().lower()
    ciudades_limpias = [c.lower().strip() for c in ciudades]
    match_data = process.extractOne(input_ciudad, ciudades_limpias, score_cutoff=60)
    
    if match_data:
        matched_ciudad = match_data[0]
        fila = df_fletes[df_fletes["ciudad"].str.lower().str.strip() == matched_ciudad].iloc[0]
        return fila["ciudad"], fila["valor_envio_base"], fila["valor_kilo_adicional"], fila["envio_a"]
    else:
        return None, None, None, None


def calcular_envio(peso_total, base, adicional):
    kilos = math.ceil(peso_total)
    if kilos <= 2:
        return base
    else:
        extra = kilos - 2
        return base + (extra * adicional)

def calcular_precio_laminas(cantidad):
    promos = cantidad // 12
    resto = cantidad % 12
    return promos * PROMO_LAMINA_12 + resto * PRECIO_LAMINA_UNIT

def calcular_precio_rollos(cantidad):
    promos = cantidad // 3
    resto = cantidad % 3
    return promos * PROMO_ROLLO_3 + resto * PRECIO_ROLLO_UNIT

def calcular_laminas_por_area(area_total):
    return math.ceil(area_total / AREA_LAMINA)

def calcular_rollos_por_area(area_total):
    return math.ceil(area_total / AREA_ROLLO)

# ======= PDF ==========
def generar_pdf(resumen):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for linea in resumen:
        pdf.cell(200, 10, txt=linea, ln=True)
    nombre = "cotizacion_decorabot.pdf"
    pdf.output(nombre)
    return nombre

# ======= INTERFAZ =======
st.title("Cotizador Decorabot")

producto = st.selectbox("¿Qué producto deseas cotizar?", ["Láminas", "Rollos"])
modo = st.radio("¿Cómo deseas cotizar?", ["Por cantidad", "Por medidas"])

# Recolección de datos
cantidad_total = 0
peso_total = 0
precio_total = 0
area_total = 0

if modo == "Por cantidad":
    cantidad = st.number_input("Cantidad:", min_value=1, step=1)
    ciudad_input = st.text_input("Ciudad de destino:")
    if st.button("Cotizar"):
        ciudad, base, adicional, envio_a = encontrar_ciudad(ciudad_input)
        if ciudad:
            if producto == "Láminas":
                precio_total = calcular_precio_laminas(cantidad)
                peso_total = cantidad * PESO_LAMINA
            else:
                precio_total = calcular_precio_rollos(cantidad)
                peso_total = cantidad * PESO_ROLLO
            valor_envio = calcular_envio(peso_total, base, adicional)
            total = precio_total + valor_envio

            st.success(f"Ciudad detectada: {ciudad} ({envio_a})")
            st.write(f"Precio producto: ${precio_total:,.0f}")
            st.write(f"Peso total: {peso_total:.2f} kg")
            st.write(f"Envío: ${valor_envio:,.0f}")
            st.markdown(f"### Total: ${total:,.0f} COP")

            resumen = [
                f"Producto: {producto}",
                f"Cantidad: {cantidad}",
                f"Precio producto: ${precio_total:,.0f}",
                f"Peso total: {peso_total:.2f} kg",
                f"Ciudad: {ciudad}",
                f"Tipo de envío: {envio_a}",
                f"Costo de envío: ${valor_envio:,.0f}",
                f"Total a pagar: ${total:,.0f} COP"
            ]

            if envio_a == "consultar":
                st.warning("El tipo de envío es 'consultar'. Verificar con logística.")

            if st.button("Descargar PDF"):
                archivo = generar_pdf(resumen)
                st.success(f"Cotización guardada como {archivo}")

elif modo == "Por medidas":
    num_paredes = st.number_input("¿Cuántas paredes quieres cotizar?", min_value=1, step=1)
    for i in range(int(num_paredes)):
        st.markdown(f"**Pared {i+1}**")
        alto = st.number_input(f"Alto (m) pared {i+1}", min_value=0.1, step=0.1, key=f"alto_{i}")
        ancho = st.number_input(f"Ancho (m) pared {i+1}", min_value=0.1, step=0.1, key=f"ancho_{i}")
        area_total += alto * ancho

    ciudad_input = st.text_input("Ciudad de destino:")

    if st.button("Cotizar"):
        ciudad, base, adicional, envio_a = encontrar_ciudad(ciudad_input)
        if ciudad:
            if producto == "Láminas":
                cantidad_total = calcular_laminas_por_area(area_total)
                precio_total = calcular_precio_laminas(cantidad_total)
                peso_total = cantidad_total * PESO_LAMINA
            else:
                cantidad_total = calcular_rollos_por_area(area_total)
                precio_total = calcular_precio_rollos(cantidad_total)
                peso_total = cantidad_total * PESO_ROLLO

            valor_envio = calcular_envio(peso_total, base, adicional)
            total = precio_total + valor_envio

            st.success(f"Ciudad detectada: {ciudad} ({envio_a})")
            st.write(f"Área total: {area_total:.2f} m²")
            st.write(f"{producto} necesarios: {cantidad_total}")
            st.write(f"Precio producto: ${precio_total:,.0f}")
            st.write(f"Peso total: {peso_total:.2f} kg")
            st.write(f"Envío: ${valor_envio:,.0f}")
            st.markdown(f"### Total: ${total:,.0f} COP")

            resumen = [
                f"Producto: {producto}",
                f"Área total: {area_total:.2f} m²",
                f"Cantidad requerida: {cantidad_total}",
                f"Precio producto: ${precio_total:,.0f}",
                f"Peso total: {peso_total:.2f} kg",
                f"Ciudad: {ciudad}",
                f"Tipo de envío: {envio_a}",
                f"Costo de envío: ${valor_envio:,.0f}",
                f"Total a pagar: ${total:,.0f} COP"
            ]

            if envio_a == "consultar":
                st.warning("El tipo de envío es 'consultar'. Verificar con logística.")

            if st.button("Descargar PDF"):
                archivo = generar_pdf(resumen)
                st.success(f"Cotización guardada como {archivo}")

