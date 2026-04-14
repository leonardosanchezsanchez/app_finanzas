import streamlit as st

# Configuración básica de la página
st.set_page_config(page_title="Diagnostico Financiero", layout="centered")

st.title("Diagnostico de Finanzas Estudiantiles")
st.write("Complete la siguiente informacion para calcular su presupuesto.")

# SECCION 1: IDENTIFICACION
st.header("Datos del Estudiante")
nombre = st.text_input("Nombre completo:")
localidad = st.text_input("Localidad de procedencia:")
edad = st.number_input("Edad:", min_value=12, max_value=25, value=16, step=1)

# SECCION 2: ENTRADAS FINANCIERAS
st.header("Ingresos y Calendario")
ingreso_total = st.number_input("Monto total de tu beca o ingreso mensual:", min_value=0.0, step=100.0)
beca_disponible = st.number_input("Dinero que te queda HOY en la cartera/cuenta:", min_value=0.0, step=10.0)
dias_restantes = st.number_input("¿Cuantos dias faltan para tu proximo pago?", min_value=1, step=1)

st.subheader("Gastos Diarios Estimados")
gasto_transporte = st.number_input("Gasto diario en transporte:", min_value=0.0, step=1.0)
gasto_alimentos = st.number_input("Gasto diario en alimentos y otros:", min_value=0.0, step=1.0)
# SECCION 3: PROCESAMIENTO Y RESULTADOS
if st.button("Calcular Diagnostico"):
    if beca_disponible > 0:
        # Calculos logicos
        gasto_diario_total = gasto_transporte + gasto_alimentos
        presupuesto_diario_maximo = beca_disponible / dias_restantes
        diferencia = presupuesto_diario_maximo - gasto_diario_total
        
        st.divider()
        st.header("Resultados del Analisis")
        
        # Mostrar resultados en columnas
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Estudiante:** {nombre}")
            st.write(f"**Origen:** {localidad}")
            st.metric("Gasto Diario Actual", f"${gasto_diario_total}")

        with col2:
            st.write(f"**Dias a cubrir:** {dias_restantes}")
            st.metric("Limite Diario Permitido", f"${presupuesto_diario_maximo:.2f}")

        st.divider()

        # Logica de decision (Diagnostico)
        if gasto_diario_total > presupuesto_diario_maximo:
            st.error("Diagnostico: Deficit Financiero")
            st.write(f"Atencion {nombre}, sus gastos diarios exceden su limite por ${abs(diferencia):.2f}. Su dinero se agotara antes de lo previsto.")
        else:
            st.success("Diagnostico: Salud Financiera Estable")
            st.write(f"Felicidades {nombre}, su nivel de gasto actual le permite cubrir los {dias_restantes} dias restantes.")
    else:
        st.warning("Por favor, ingrese un monto de beca valido para realizar el calculo.")