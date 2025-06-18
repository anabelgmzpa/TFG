import streamlit as st
import Analisis.helpers as h

def main():
    # Configuración de la página
    st.set_page_config(page_title="Selección de características de la empresa")

    # Menu de navegación
    paginas = {
        "Selección de indicadores": h.menu1(),
        "Selección de características de la empresa": h.menu2(),
        "Confirmar selección": "3️⃣"
    }
    for pag, icono in paginas.items():
        if st.sidebar.button(f"{pag}", icon= icono):
            st.session_state["pag_actual"] = pag
            st.rerun()
    st.sidebar.divider()
    if st.session_state["user_act"] != "Anonimo":
        out= "Cerrar Sesión"
        if st.sidebar.button("Inicio", icon="🏠"):
            st.session_state["pag_actual"] = "Home"
            st.rerun()
    else:
        out= "Salir"
    if st.sidebar.button(f":red[{out}]", icon="❌"):
        st.session_state["pag_actual"] = "Inicio"
        st.rerun()

    # Logo de la aplicación
    st.logo("Paginas/Logo.png", size="large")

    # Título de la página
    st.markdown("<style>.block-container {padding-top: 1.8rem;}</style>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Selección de características de la empresa</h1>", unsafe_allow_html=True)

    # Variable local auxiliar
    aux_sector = None
    aux_tamaño = None
    aux_tipo = None
    aux_ambito = None
    aux_importacion = None
    aux_exportacion = None
    aux_sostenibilidad = None
    aux_sexo = None
    aux_edad = None
    aux_creencias = None

    with st.container(height= 450):
        # Característca SECTOR  
        sectores= ["Agricultura, ganadería, silvicultura y pesca",
                    "Audiovisual",
                    "Comercio al por mayor y al por menor",
                    "Construcción",
                    "Defensa",
                    "Educación",
                    "Energía",
                    "Industrial",
                    "Sanidad",
                    "Servicios financieros",
                    "Tecnología",
                    "Transporte (también público) y logística",
                    "Turismo y ocio"]
        if st.session_state["sector_emp"] != None:
            aux_sector= st.pills("Sector:", sectores, selection_mode="single", default= st.session_state["sector_emp"]) 
        else:
            aux_sector= st.pills("Sector:", sectores, selection_mode="single")

        # Característca TAMAÑO 
        tamaños= ["PyME (<250 empleados)",
                "Grande (>250 empleados)"]
        if st.session_state["tamaño_emp"] != None:
            aux_tamaño= st.pills("Tamaño:", tamaños, selection_mode="single", default=st.session_state["tamaño_emp"], key="tamaño_pills_seleccionado")
        else:
            aux_tamaño= st.pills("Tamaño:", tamaños, selection_mode="single", key="tamaño_pills")

        # Característca PROPIEDAD DEL CAPITAL
        tipos= ["Pública",
                "Privada"]
        if st.session_state["tipo_emp"] != None:
            aux_tipo= st.pills("Propiedad del capital:", tipos, selection_mode="single", default= st.session_state["tipo_emp"], key="tipo_pills_seleccionado")
        else:
            aux_tipo= st.pills("Propiedad del capital:", tipos, selection_mode="single", key="tipo_pills")

        # Característca ÁMBITO GEOGRÁFICO
        ambitos= ["Nacional",
                "Internacional"]
        if st.session_state["ambito_emp"] != None:
            aux_ambito= st.pills("Ámbito geográfico:", ambitos, selection_mode="single", default= st.session_state["ambito_emp"], key="ambito_pills_seleccionado")
        else:
            aux_ambito= st.pills("Ámbito geográfico:", ambitos, selection_mode="single", key="ambito_pills")

        # Característca NECESIDAD DE IMPORTACIÓN
        importacion= ["Nada",
                    "Baja",
                    "Alta"]
        if st.session_state["importacion_emp"] != None:
            aux_importacion = st.pills("Necesidad de importación:", importacion, selection_mode="single", default= st.session_state["importacion_emp"], key="importacion_pills_seleccionado")
        else:
            aux_importacion = st.pills("Necesidad de importación:", importacion, selection_mode="single", key="importacion_pills")

        # Característca CAPACIDAD DE EXPORTACIÓN
        exportacion= ["Nada",
                    "Baja",
                    "Alta"]
        if st.session_state["exportacion_emp"] != None:
            aux_exportacion = st.pills("Capacidad de exportación:", exportacion, selection_mode="single", default= st.session_state["exportacion_emp"], key="exportacion_pills_seleccionado")
        else:
            aux_exportacion = st.pills("Capacidad de exportación:", exportacion, selection_mode="single", key="exportacion_pills")

        # Característca SOSTENIBILIDAD
        sostenibilidad= ["Baja",
                        "Alta"]
        if st.session_state["sostenibilidad_emp"] != None:
            aux_sostenibilidad = st.pills("Sostenibilidad:", sostenibilidad, selection_mode="single", default= st.session_state["sostenibilidad_emp"], key="sostenibilidad_pills_seleccionado")
        else:
            aux_sostenibilidad = st.pills("Sostenibilidad:", sostenibilidad, selection_mode="single", key="sostenibilidad_pills")

        # Característca CLIENTE OBJETIVO
        st.write(" ")
        st.write("**Cliente objetivo**")
        # Sexo
        sexo= ["Irrelevante",
                        "Masculino",
                        "Femenino"]
        if st.session_state["sexo_emp"] != None:
            aux_sexo = st.pills("Sexo:", sexo, selection_mode="single", default= st.session_state["sexo_emp"], key="sexo_pills_seleccionado")
        else:
            aux_sexo = st.pills("Sexo:", sexo, selection_mode="single", key="sexo_pills")
        # Edad
        edad = ["Irrelevante",
            "-18 años",
            "18 - 24 años",
            "25 - 49 años",
            "50 - 64 años",
            "+65 años"]
        if st.session_state["edad_emp"] != None:
            aux_edad = st.pills("Edad:", edad, selection_mode="single", default=st.session_state["edad_emp"], key="edad_pills_seleccionado")
        else:
            aux_edad = st.pills("Edad:", edad, selection_mode="single", key="edad_pills")
        # Creencias
        creencias = ["Irrelevante",
                "Ateos",
                "Cristianos",
                "Musulmanes"]
        if st.session_state["creencias_emp"] != None:
            aux_creencias = st.pills("Creencias:", creencias, selection_mode="single", default=st.session_state["creencias_emp"], key="creencias_pills_seleccionado")
        else:
            aux_creencias = st.pills("Creencias:", creencias, selection_mode="single", key="creencias_pills")


    # Botón para guardar la selección de indicadores 
    col1, col2 = st.columns([2, 1], vertical_alignment="center")
    with col1:
        container_error = st.container()
    with col2:
        if st.button("Guardar selección", type="primary"):
            if aux_sector != None and aux_tamaño != None and aux_tipo != None and aux_ambito != None and aux_importacion != None and aux_exportacion != None and aux_sostenibilidad != None and aux_sexo != None and aux_edad != None and aux_creencias != None:
                st.session_state["sector_emp"] = aux_sector
                st.session_state["tamaño_emp"] = aux_tamaño
                st.session_state["tipo_emp"] = aux_tipo
                st.session_state["ambito_emp"] = aux_ambito
                st.session_state["importacion_emp"] = aux_importacion
                st.session_state["exportacion_emp"] = aux_exportacion
                st.session_state["sostenibilidad_emp"] = aux_sostenibilidad
                st.session_state["sexo_emp"] = aux_sexo
                st.session_state["edad_emp"] = aux_edad
                st.session_state["creencias_emp"] = aux_creencias

                st.session_state["pag_actual"] = "Confirmar selección"  # Cambiar la página
                st.session_state["ok_caracteristicas"] = True
                st.rerun()
            else:
                with container_error:
                    st.error("Debes seleccionar una opción de cada característica")
        
