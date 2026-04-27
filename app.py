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
    if st.button("Volver", key="btn_login_regresar"):
        st.session_state.pagina = 'bienvenida'
        st.rerun()

    st.title("Acceso a Ledgerly")
    
    tab1, tab2 = st.tabs(["Iniciar Sesion", "Registrarme"])

    with tab1:
        st.subheader("Bienvenido de nuevo")
        user_login = st.text_input("Usuario", key="login_user_input")
        pass_login = st.text_input("Contrasena", type="password", key="login_pass_input")
        
        if st.button("Entrar", key="btn_validar_login"):
            if user_login and pass_login:
                from base_de_datos import validar_login
                usuario_valido = validar_login(user_login, pass_login)
                
                if usuario_valido:
                    st.session_state.usuario_id = usuario_valido[0]
                    st.session_state.usuario_actual = usuario_valido[1]
                    st.success(f"Hola de nuevo, {user_login}")
                    st.session_state.pagina = 'formulario_inicial'
                    st.rerun()
                else:
                    st.error("Usuario o contrasena incorrectos.")
            else:
                st.warning("Escribe tus datos para entrar.")

    with tab2:
        st.subheader("Crea tu cuenta")
        st.write("Registra un usuario unico para empezar a trackear tus gastos.")
        
        nuevo_usuario = st.text_input("Elige un nombre de usuario", key="reg_user_input")
        nueva_password = st.text_input("Crea una contrasena", type="password", key="reg_pass_input")
        
        if st.button("Registrarme", key="btn_crear_cuenta"):
            if nuevo_usuario and nueva_password:
                from base_de_datos import registrar_usuario
                if registrar_usuario(nuevo_usuario, nueva_password):
                    st.success("Usuario creado con exito. Ahora ve a la pestana de Iniciar Sesion.")
                else:
                    st.error("Ese nombre de usuario ya esta ocupado.")
            else:
                st.warning("Por favor rellena todos los campos.")

elif st.session_state.pagina == 'formulario_inicial':
    st.title("Configuracion de Perfil Financiero")
    st.write(f"Hola {st.session_state.usuario_actual}, responde esto para personalizar tu experiencia.")

    nombre_real = st.text_input("¿Cual es tu nombre?", key="form_nombre")
    periodo = st.selectbox("¿Cada cuanto recibes dinero?", ["Semanal", "Quincenal", "Mensual"], key="form_periodo")
    monto_ingreso = st.number_input(f"¿Cuanto recibes de forma {periodo}?", min_value=0.0, step=50.0, key="form_monto")
    
    fuentes = st.multiselect("¿Como recibes ese dinero?", 
                             ["Mesada / Apoyo familiar", "Trabajo", "Beca", "Otros"], key="form_fuentes")
    
    st.subheader("Tus Gastos")
    categorias = st.multiselect("¿En que gastas mas dinero?", 
                                ["Transporte", "Comida", "Ropa", "Entretenimiento", "Belleza", "Gasolina", "Otros"], key="form_cats")
    
    gastos_estimados = {}
    for cat in categorias:
        gastos_estimados[cat] = st.number_input(f"¿Cuanto gastas aproximadamente en {cat}?", min_value=0.0, key=f"gasto_{cat}")

    st.subheader("Estado Actual")
    saldo_cartera = st.number_input("¿Cuanto dinero tienes actualmente en tu cartera?", min_value=0.0, key="form_saldo")
    dias_para_pago = st.number_input("¿Cuantos dias faltan para tu proximo pago?", min_value=0, max_value=31, key="form_dias")

    ahorra = st.radio("¿Ahorras dinero?", ["No", "Si"], key="form_ahorra")
    meta_ahorro = ""
    monto_ahorro = 0.0

    if ahorra == "Si":
        meta_ahorro = st.text_input("¿Para que estas ahorrando?", key="form_meta")
        monto_ahorro = st.number_input("¿Cuanto de tu ingreso destinas al ahorro?", min_value=0.0, key="form_monto_ahorro")

    # ESTO VA AL FINAL DE TU FORMULARIO
    if st.button("Finalizar Registro y Ver Análisis", key="btn_finalizar_todo"):
        if nombre_real and fuentes:
            # --- 1. CÁLCULOS LÓGICOS ---
            total_gastos_fijos = sum(gastos_estimados.values())
            balance_disponible = monto_ingreso - total_gastos_fijos - monto_ahorro
            
            # Cálculo de supervivencia diaria
            # Usamos los días que faltan para el pago que el usuario puso antes
            presupuesto_diario = round(balance_disponible / dias_para_pago, 2) if dias_para_pago > 0 else 0

            # Proyección a 6 meses: (Ahorro actual + un 20% extra del ingreso) * 6 meses
            ahorro_extra_sugerido = monto_ingreso * 0.20
            total_6_meses = (monto_ahorro + ahorro_extra_sugerido) * 6

            # --- 2. EL ANÁLISIS COMPLEJO (VISUAL) ---
            st.divider()
            st.header(f"📈 Reporte de Inteligencia Financiera para {nombre_real}")

            # Bloque de Gasto Diario
            st.subheader("🚀 Guía de Gastos de Supervivencia")
            if balance_disponible > 0:
                st.info(f"""
                **Tu Presupuesto Diario:** Para llegar con dinero a tu próximo pago en **{dias_para_pago} días**, 
                te recomendamos no gastar más de **${presupuesto_diario}** diarios en gustos o extras.
                """)
            else:
                st.error(f"🚨 **Cuidado:** Tus compromisos superan tus ingresos por ${abs(balance_disponible)}. No tienes presupuesto diario disponible.")

            # Bloque de Proyección
            st.subheader("💰 ¿Qué pasaría si ahorras un 20% más?")
            col_a, col_b = st.columns(2)
            col_a.metric("Ahorro Actual", f"${monto_ahorro}")
            col_b.metric("Meta Sugerida (20%)", f"+${ahorro_extra_sugerido:,.0f}")
            
            st.write(f"Si haces este ajuste, en **6 meses** habrás acumulado **${total_6_meses:,.2f}**. "
                     f"Esto sería clave para tu meta de: *{meta_ahorro if meta_ahorro else 'tu futuro'}*.")

            # --- 3. GRÁFICA (LA QUE YA TE GUSTÓ) ---
            import plotly.express as px
            datos_pie = {
                "Concepto": list(gastos_estimados.keys()) + ["Ahorro", "Libre"],
                "Monto": list(gastos_estimados.values()) + [monto_ahorro, max(0, balance_disponible)]
            }
            fig = px.pie(datos_pie, values='Monto', names='Concepto', hole=0.5, 
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)

            # --- 4. DIAGNÓSTICO DE MEJORA ---
            st.subheader("🏥 Diagnóstico y Mejora")
            porcentaje_fijos = (total_gastos_fijos / monto_ingreso) * 100

            if porcentaje_fijos <= 50:
                st.success("**Situación: Excelente.** Tienes un control muy bueno.")
                st.write("👉 **Mejora:** Podrías invertir ese excedente en un fondo de inversión o adelantar pagos de deudas si las tienes.")
            elif 50 < porcentaje_fijos <= 80:
                st.warning("**Situación: Estable pero en riesgo.**")
                # Buscamos la categoría donde más gasta para darle el consejo
                cat_mayor = max(gastos_estimados, key=gastos_estimados.get) if gastos_estimados else "N/A"
                st.write(f"👉 **Mejora:** Intenta reducir un 10% en **{cat_mayor}**. Eso liberará flujo de caja para tus ahorros.")
            else:
                st.error("**Situación: Crítica.** Estás viviendo al límite.")
                st.write("👉 **Mejora:** Es urgente recortar suscripciones o gastos variables. Tu prioridad debe ser bajar tus gastos fijos al 70%.")

            # --- 5. PREGUNTA FINAL DE INTENCIÓN ---
            st.divider()
            st.subheader("🎯 Ahora, ¿cómo quieres que trabajemos?")
            objetivo = st.selectbox(
                "Selecciona tu prioridad para este ciclo:",
                ["Solo registrar gastos (Control)", 
                 "Administrar para mi meta (Ahorro)", 
                 "Ayuda para no quedarme sin dinero (Supervivencia)"]
            )

            if st.button("🚀 Confirmar Plan e Ir a mi Registro Diario"):
                # Guardamos todo para el Dashboard
                st.session_state.perfil_completo = {
                    "nombre": nombre_real,
                    "presupuesto_diario": presupuesto_diario,
                    "objetivo": objetivo,
                    "balance_libre": balance_disponible
                }
                st.session_state.pagina = 'dashboard'
                st.rerun()