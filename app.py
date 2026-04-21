import streamlit as st
from base_de_datos import inicializar_db
import pandas as pd

# 1. INICIALIZACION
inicializar_db()

# Configuración de página (Debe ir al principio)
st.set_page_config(page_title="Ledgerly - Analisis Financiero", layout="centered")

# 2. GESTION DE NAVEGACION
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'bienvenida'

# --- LOGICA DE PANTALLAS ---

if st.session_state.pagina == 'bienvenida':
    st.title("Ledgerly")
    st.write("Herramienta de Diagnostico y Analisis de Gastos Estudiantiles")
    st.write("---")
    st.subheader("Bienvenido")
    st.write("¿Como deseas utilizar la aplicacion hoy?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Usar como Invitado", use_container_width=True):
            st.session_state.pagina = 'invitado'
            st.rerun()
    with col2:
        if st.button("Iniciar Sesion / Registro", use_container_width=True):
            st.session_state.pagina = 'login'
            st.rerun()

elif st.session_state.pagina == 'invitado':
    # BOTON PARA REGRESAR
    if st.button("Volver al inicio"):
        st.session_state.pagina = 'bienvenida'
        st.rerun()

    # --- AQUI EMPIEZA TU CODIGO ORIGINAL ---
    st.title("Modo Invitado")
    st.caption("Nota: Los datos no se guardaran al cerrar la sesion.")

    # --- SECCION 1: PERFIL GENERAL ---
    with st.container(border=True):
        st.header("1. Datos Generales")
        nombre = st.text_input("Ingresa tu nombre para el reporte:", placeholder="Ej. Leonardo Sanchez")
        st.write("")
        tipo_ingreso = st.multiselect(
            "¿De donde viene tu dinero?", 
            ["Trabajo", "Mesada/Apoyo familiar", "Beca", "Emprendimiento propio"]
        )
        st.write("")
        monto_aprox = st.selectbox(
            "¿Cuanto dinero recibes aproximadamente al mes?", 
            ["$0-500", "$500-1000", "$1000-2000", "+$2000"]
        )
        st.write("")
        saldo_actual = st.number_input("Dinero que tienes disponible justo ahora (MXN):", min_value=0.0, step=10.0)
        st.write("")
        frecuencia = st.selectbox("¿Cada cuanto recibes dinero?", ["Semanal", "Quincenal", "Mensual"])
        st.write("")
        registra_gasto = st.radio("¿Llevas un registro de lo que vas gastando?", ["Siempre", "A veces", "Nunca"], horizontal=True)
        st.write("")
        dias_faltantes = st.number_input("Dias que te faltan para volver a recibir dinero:", min_value=1, step=1)

    # --- SECCION 2: ANALISIS DE GASTOS ---
    with st.container(border=True):
        st.header("2. Tus Gastos Principales")
        st.write("Elige las categorias donde mas se te va el dinero:")
        categorias = st.multiselect(
            "Categorias:", 
            ["Comida", "Transporte", "Entretenimiento", "Ropa", "Material Escolar","Gasolina","Otros"]
        )
        diccionario_gastos = {}
        if categorias:
            st.write("---")
            st.write("Escribe cuanto gastas al mes en cada una:")
            cols_g = st.columns(len(categorias))
            for i, cat in enumerate(categorias):
                with cols_g[i]:
                    diccionario_gastos[cat] = st.number_input(f"{cat}:", min_value=0.0, step=10.0)

    # --- SECCION 3: HABITOS DE AHORRO ---
    with st.container(border=True):
        st.header("3. Cultura de Ahorro")
        se_queda_sin_dinero = st.selectbox(
            "¿Te pasa que te quedas sin un peso antes de que termine la semana o el mes?", 
            ["Siempre", "A veces", "Nunca"]
        )
        st.write("")
        ahorra = st.radio("¿Sueles guardar dinero para el futuro?", ["Si", "A veces", "No"], horizontal=True)
        if ahorra != "No":
            st.write("")
            para_que_ahorra = st.selectbox(
                "¿Cual es el objetivo de ese ahorro?", 
                ["Emergencias", "Comprar algo especial", "Viajes", "Inversion/Otro"]
            )
        else:
            st.caption("No se reporta ningun habito de ahorro actualmente.")

    # --- SECCION 4: RESULTADOS Y ANALISIS ---
    if st.button("GENERAR MI ANALISIS", use_container_width=True):
        st.divider()
        st.subheader(f"Reporte Financiero Personal: {nombre}")
        total_gastos = sum(diccionario_gastos.values())
        valores_ingreso = {"$0-500": 500, "$500-1000": 1000, "$1000-2000": 2000, "+$2000": 3000}
        ingreso_num = valores_ingreso[monto_aprox]
        presupuesto_diario = saldo_actual / dias_faltantes if dias_faltantes > 0 else 0
        
        st.write("### Graficas de tu situacion")
        g1, g2, g3 = st.columns(3)
        with g1:
            st.write("**En que gastas**")
            if diccionario_gastos:
                df_gastos = pd.DataFrame(list(diccionario_gastos.items()), columns=['Categoria', 'Monto'])
                st.bar_chart(data=df_gastos, x='Categoria', y='Monto')
        with g2:
            st.write("**Gasto vs Disponible**")
            datos_resumen = pd.DataFrame({
                'Estado': ['Gastos', 'Disponible'],
                'Monto': [total_gastos, max(0, ingreso_num - total_gastos)]
            })
            st.bar_chart(data=datos_resumen, x='Estado', y='Monto')
        with g3:
            st.write("**Meta Ahorro (20%)**")
            ahorro_mensual_ideal = ingreso_num * 0.20
            meses = ["Mes 1", "Mes 2", "Mes 3", "Mes 4", "Mes 5", "Mes 6"]
            progreso = [ahorro_mensual_ideal * i for i in range(1, 7)]
            st.line_chart(pd.DataFrame(progreso, index=meses))

        st.write("---")
        st.write("### Revision de tu Situacion Financiera")
        st.write(f"Segun lo que nos contaste, tienes **${presupuesto_diario:.2f}** para gastar cada dia.")
        
        if total_gastos > ingreso_num:
            st.write("Ojo aqui: tus gastos mensuales son mas altos que lo que estas recibiendo.")
        else:
            porcentaje_disponible = ((ingreso_num - total_gastos) / ingreso_num) * 100
            st.write(f"Te queda un margen libre del **{porcentaje_disponible:.1f}%**.")

        if se_queda_sin_dinero in ["Siempre", "A veces"]:
            st.write("El hecho de que te quedes sin dinero antes de tiempo indica falta de orden.")
        
        if registra_gasto == "Nunca":
            st.write("Al no anotar tus gastos, es probable que tengas gastos hormiga.")

        st.write("### Recomendaciones para mejorar")
        st.write(f"Intenta gastar maximo **${presupuesto_diario * 0.8:.2f}** al dia.")
        st.write(f"Intenta ahorrar al menos **${ingreso_num * 0.10:.2f}** cada mes.")

elif st.session_state.pagina == 'login':
    if st.button("Volver"):
        st.session_state.pagina = 'bienvenida'
        st.rerun()
    st.title("Acceso a Ledgerly")
    st.write("Aqui desarrollaremos el sistema de registro pronto.")