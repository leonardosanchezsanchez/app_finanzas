import streamlit as st
st.title("App Mis gastos")
opcion = st.selectbox("En que gastas tu dinero",('Transporte','Comida','Ropa','Diversion'))
#st.write(opcion)
ingreso = st.number_input("Cual es tu ingreso semanal: ",value=0.0)
gastos = st.number_input("Cuanto gastas a la semana: ",value=0.0)
st.divider()
if st.button("Hacer balance"):
    b = ingreso - gastos
    st.success(f"seleccionaste: {opcion}")
    st.info(f"El balance es: {b}" )