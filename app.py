import streamlit as st
import pandas as pd

# CONFIGURACION DE PAGINA
st.set_page_config(page_title="Ledgerly - Analisis Financiero", layout="centered")

# TITULO PRINCIPAL
st.title("Ledgerly")
st.write("Herramienta de Diagnostico y Analisis de Gastos Estudiantiles")
st.write("")

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

st.write("")

# --- SECCION 2: ANALISIS DE GASTOS ---
with st.container(border=True):
    st.header("2. Tus Gastos Principales")
    st.write("Elige las categorias donde mas se te va el dinero:")
    categorias = st.multiselect(
        "Categorias:", 
        ["Comida", "Transporte", "Entretenimiento", "Ropa", "Material Escolar", "Otros"]
    )
    
    diccionario_gastos = {}
    
    if categorias:
        st.write("---")
        st.write("Escribe cuanto gastas al mes en cada una:")
        cols_g = st.columns(len(categorias))
        for i, cat in enumerate(categorias):
            with cols_g[i]:
                diccionario_gastos[cat] = st.number_input(f"{cat}:", min_value=0.0, step=10.0)

st.write("")

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

st.write("")

# --- SECCION 4: RESULTADOS Y ANALISIS ---
if st.button("GENERAR MI ANALISIS", use_container_width=True):
    st.divider()
    st.subheader(f"Reporte Financiero Personal: {nombre}")
    
    # CALCULOS TECNICOS
    total_gastos = sum(diccionario_gastos.values())
    valores_ingreso = {"$0-500": 500, "$500-1000": 1000, "$1000-2000": 2000, "+$2000": 3000}
    ingreso_num = valores_ingreso[monto_aprox]
    presupuesto_diario = saldo_actual / dias_faltantes if dias_faltantes > 0 else 0
    
    # VISUALIZACION DE DATOS
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

    # --- ANALISIS DETALLADO ---
    st.write("---")
    st.write("### Revision de tu Situacion Financiera")
    
    # Evaluacion Cuantitativa
    st.write("**Revision de tus numeros:**")
    st.write(f"Segun lo que nos contaste, tienes **${presupuesto_diario:.2f}** para gastar cada dia y poder aguantar los {dias_faltantes} dias que te faltan para volver a tener dinero.")
    
    if total_gastos > ingreso_num:
        st.write("Ojo aqui: tus gastos mensuales son mas altos que lo que estas recibiendo. Esto es una señal de alerta porque significa que estas usando dinero que no tienes o que estas pidiendo prestado para cubrir el mes.")
    else:
        porcentaje_disponible = ((ingreso_num - total_gastos) / ingreso_num) * 100
        st.write(f"Te queda un margen libre del **{porcentaje_disponible:.1f}%** de tus ingresos. Esto es bueno porque significa que tu nivel de vida es sostenible con lo que ganas actualmente.")

    st.write("")
    
    # Diagnostico de Comportamiento
    st.write("**Analisis de tus habitos:**")
    if se_queda_sin_dinero in ["Siempre", "A veces"]:
        st.write("El hecho de que te quedes sin dinero antes de tiempo indica que no hay un orden real entre lo que ganas y lo que consumes. Parece que estas gastando mas en cosas variables antes de asegurar los gastos que realmente importan.")
    
    if registra_gasto == "Nunca":
        st.write("Al no anotar en que se te va el dinero, es muy probable que tengas 'gastos hormiga' que estan vaciando tu cartera sin que te des cuenta. Sin un registro, es casi imposible saber por donde se esta escapando tu capital.")

    st.write("")
    
    # Propuesta de Optimización
    st.write("### Recomendaciones para mejorar")
    
    st.write("**Plan de gasto diario:**")
    st.write(f"Te recomendamos que intentes gastar maximo **${presupuesto_diario * 0.8:.2f}** al dia. Ese 20% de diferencia que te sobra usalo como un colchon de seguridad por si surge algun imprevisto en la escuela o con tus amigos.")
    
    st.write("**Meta de ahorro sugerida:**")
    st.write(f"Para que tus finanzas esten sanas, intenta ahorrar al menos **${ingreso_num * 0.10:.2f}** cada mes. El truco es separar este dinero en cuanto lo recibas, asi no sentiras la tentacion de gastartelo en cosas innecesarias.")

    if "Comida" in diccionario_gastos or "Transporte" in diccionario_gastos:
        st.write("**Sobre tus gastos fuertes:** Como tus gastos mas grandes estan en comida o transporte, te conviene checar si puedes cocinar mas en casa o buscar rutas mas baratas. Cualquier ahorro pequeño en estas categorias hara una gran diferencia al final de la semana.")