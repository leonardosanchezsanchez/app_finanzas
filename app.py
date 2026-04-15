import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analizador Financiero Estudiantil", layout="wide")

st.title("Sistema de Diagnostico Financiero")
st.write("Analisis de habitos de consumo y salud economica estudiantil")

# --- SECCION 1: PERFIL DEL ESTUDIANTE ---
with st.container():
    st.header("1. Perfil General")
    nombre = st.text_input("Ingresa tu nombre:")
    
    col_perfil1, col_perfil2, col_perfil3 = st.columns(3)
    with col_perfil1:
        tipo_ingreso = st.selectbox("¿Recibes ingresos propios?", 
                                   ["No", "Si (trabajo)", "Si (mesada/apoyo familiar)"])
        frecuencia = st.selectbox("¿Con que frecuencia recibes dinero?", 
                                 ["Diario", "Semanal", "Quincenal", "Mensual", "No recibo"])
    with col_perfil2:
        monto_aprox = st.selectbox("¿Cuanto dinero recibes aproximadamente al mes?", 
                                  ["$0-500", "$500-1000", "$1000-2000", "+$2000"])
        registra_gasto = st.radio("¿Sueles registrar en que gastas tu dinero?", 
                                 ["Siempre", "Aveces", "Nunca"], horizontal=True)
    with col_perfil3:
        saldo_actual = st.number_input("Monto disponible al dia de hoy:", min_value=0.0, step=10.0)
        dias_faltantes = st.number_input("Dias restantes para el proximo ingreso:", min_value=1, step=1)

# --- SECCION 2: DESGLOSE DE GASTOS (Dinamico) ---
st.header("2. Analisis de Gastos")
categorias = st.multiselect("Selecciona las categorias de mayor gasto:", 
                           ["Comida", "Transporte", "Entretenimiento", "Ropa", "Material Escolar", "Otros"])

diccionario_gastos = {}
if categorias:
    st.write("Desglose de gastos mensuales por concepto:")
    cols_g = st.columns(len(categorias))
    for i, cat in enumerate(categorias):
        with cols_g[i]:
            diccionario_gastos[cat] = st.number_input(f"Mensual en {cat}:", min_value=0.0, step=10.0)

# --- SECCION 3: HABITOS Y AHORRO ---
st.header("3. Habitos de Ahorro")
col_ahorro1, col_ahorro2 = st.columns(2)

with col_ahorro1:
    se_queda_sin_dinero = st.selectbox("¿Te quedas sin dinero antes de que termine el periodo?", 
                                      ["Siempre", "Aveces", "Nunca"])
    ahorra = st.radio("¿Sueles ahorrar dinero?", ["Si", "Aveces", "No"], horizontal=True)

with col_ahorro2:
    if ahorra != "No":
        para_que_ahorra = st.selectbox("Finalidad del ahorro:", 
                                      ["Emergencias", "Comprar algo especifico", "Viajes", "Otro"])
    else:
        st.write("Actualmente no se reporta cultura de ahorro.")

# --- SECCION 4: DIAGNOSTICO, GRAFICAS Y ANALISIS ---
if st.button("Generar Analisis"):
    st.divider()
    st.subheader(f"Reporte Financiero: {nombre}")
    
    total_gastos = sum(diccionario_gastos.values())
    valores_ingreso = {"$0-500": 500, "$500-1000": 1000, "$1000-2000": 2000, "+$2000": 3000}
    ingreso_num = valores_ingreso[monto_aprox]
    presupuesto_diario = saldo_actual / dias_faltantes if dias_faltantes > 0 else 0
    
    # --- VISUALIZACION ---
    st.write("### Graficas de Comportamiento")
    g1, g2, g3 = st.columns(3)

    with g1:
        st.write("Distribucion de Gastos")
        if diccionario_gastos:
            df_gastos = pd.DataFrame(list(diccionario_gastos.items()), columns=['Categoria', 'Monto'])
            st.bar_chart(data=df_gastos, x='Categoria', y='Monto')
    
    with g2:
        st.write("Balance Ingresos vs Gastos")
        datos_resumen = pd.DataFrame({
            'Estado': ['Gastos', 'Disponible'],
            'Monto': [total_gastos, max(0, ingreso_num - total_gastos)]
        })
        st.area_chart(datos_resumen.set_index('Estado'))

    with g3:
        st.write("Proyeccion de Ahorro Acumulado")
        ahorro_mensual_ideal = ingreso_num * 0.15
        meses = ["Mes 1", "Mes 2", "Mes 3", "Mes 4", "Mes 5", "Mes 6"]
        progreso = [ahorro_mensual_ideal * i for i in range(1, 7)]
        st.line_chart(pd.DataFrame(progreso, index=meses))

    # --- SECCION DE ANALISIS COMPLEJO ---
    st.divider()
    st.header("Analisis de Situacion Financiera")
    
    analisis_col1, analisis_col2 = st.columns(2)
    
    with analisis_col1:
        st.write("### Evaluacion Cuantitativa")
        st.write(f"A partir de los datos proporcionados, se observa que el usuario cuenta con una liquidez diaria de **${presupuesto_diario:.2f}** para cubrir sus necesidades durante los proximos **{dias_faltantes}** dias.")
        
        # Logica de analisis de solvencia
        if total_gastos > ingreso_num:
            st.write("Se detecta un deficit financiero: los gastos mensuales reportados superan el ingreso promedio. Esta situacion sugiere una dependencia de prestamos o una subestimacion de los ingresos reales.")
        else:
            porcentaje_disponible = ((ingreso_num - total_gastos) / ingreso_num) * 100
            st.write(f"El usuario mantiene un margen de solvencia del **{porcentaje_disponible:.1f}%** sobre su ingreso mensual. Este excedente es positivo, pero su gestion dependera de la disciplina en los gastos variables.")

    with analisis_col2:
        st.write("### Diagnostico de Comportamiento")
        if se_queda_sin_dinero == "Siempre" or se_queda_sin_dinero == "Aveces":
            st.write("Existe una falta de correlacion entre el flujo de efectivo y el consumo. El hecho de agotar el capital antes de finalizar el periodo indica que no se estan priorizando los gastos fijos sobre los variables.")
        
        if registra_gasto == "Nunca":
            st.write("La ausencia de registros financieros impide la identificacion de fugas de capital o 'gastos hormiga', lo que dificulta la planeacion a mediano plazo.")

    # --- CONSEJOS DERIVADOS DEL ANALISIS ---
    st.header("Propuesta de Optimizacion")
    
    cons_col1, cons_col2 = st.columns(2)
    
    with cons_col1:
        st.write("**Estrategia de flujo de efectivo:**")
        st.write(f"Se recomienda ajustar el gasto diario a un maximo de **${presupuesto_diario * 0.8:.2f}**, reservando el 20% restante como fondo de maniobra para imprevistos escolares o personales.")
        
        st.write("**Gestion de categorias:**")
        st.write("Si el gasto en transporte o comida es elevado, se sugiere buscar alternativas de consumo local o rutas de transporte optimizadas para reducir el impacto en la liquidez semanal.")

    with cons_col2:
        st.write("**Plan de Ahorro:**")
        st.write(f"Para estabilizar las finanzas, se propone un ahorro objetivo de **${ingreso_num * 0.10:.2f}** mensuales (10% del ingreso). Este capital deberia ser depositado en un fondo separado inmediatamente al recibir el ingreso para evitar la tentacion de consumo.")
        
        st.write("**Control de presupuesto:**")
        st.write("Es indispensable implementar una bitacora de egresos. Identificar y reducir los gastos en entretenimiento o ropa durante periodos de baja liquidez permitira llegar al final del ciclo con saldo positivo.")