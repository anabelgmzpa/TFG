import streamlit as st
import Analisis.helpers as h
import queue as q
from BD.gestor_inds import Indicador as i
from BD.gestor_perfiles import Perfil as p

def main():
    # Configuración de la página
    st.set_page_config(page_title="Confirmar selección")

    # Reiniciar el perfil a comparar
    st.session_state["perfil_comp"]= None

    # Revisión del estado del thread
    try:
        msg = st.session_state["cola_cargados"].get_nowait()
        if msg == "cargado":
            st.session_state["inds_cargados"] = True
    except q.Empty:
        pass

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
    st.markdown("<h1 style='text-align: center;'>Resumen de tu selección</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Indicadores seleccionados:")
        with st.container(height= 400, border=False):
            inds_nombres= [i.get_name(indicador[0]) for indicador in st.session_state["inds_seleccionados"]]
            inds_nombres.sort()
            for ind_name in inds_nombres:
                st.write(ind_name)

    with col2:
        st.subheader("Características de tu empresa:")
        if st.session_state['sector_emp'] == None:
            st.write("**Sector:**")
        else:
           st.write(f"**Sector:** {st.session_state['sector_emp']}") 
        if st.session_state['tamaño_emp'] == None:
            st.write("**Tamaño:**")
        else:
            st.write(f"**Tamaño:** {st.session_state['tamaño_emp']}")
        if st.session_state['tipo_emp'] == None:
            st.write("**Propiedad del capital:**")
        else:
            st.write(f"**Propiedad del capital:** {st.session_state['tipo_emp']}")
        if st.session_state['ambito_emp'] == None:
            st.write("**Ámbito geográfico:**")
        else:
            st.write(f"**Ámbito geográfico:** {st.session_state['ambito_emp']}")
        if st.session_state['importacion_emp'] == None:
            st.write("**Importación:**")
        else:
            st.write(f"**Importación:** {st.session_state['importacion_emp']}")
        if st.session_state['exportacion_emp'] == None:
            st.write("**Exportación:**")
        else:
            st.write(f"**Exportación:** {st.session_state['exportacion_emp']}")
        if st.session_state['sostenibilidad_emp'] == None:
            st.write("**Sostenibilidad:**")
        else:   
            st.write(f"**Sostenibilidad:** {st.session_state['sostenibilidad_emp']}")
        if st.session_state["sexo_emp"]==None and st.session_state["edad_emp"]==None and st.session_state["creencias_emp"]==None:
            st.write("**Cliente objetivo:**")
        else:
            sexo = st.session_state['sexo_emp']
            edad = st.session_state['edad_emp']
            creencias = st.session_state['creencias_emp']
            # Filtrar los que no sean "Irrelevante"
            selecciones = [x for x in [sexo, edad, creencias] if x != "Irrelevante"]
            # Mostrar resultado
            if selecciones:
                st.write(f"**Cliente objetivo:** {', '.join(selecciones)}")
                st.session_state['cliente_obj']= f"{', '.join(selecciones)}"
            else:
                st.write("**Cliente objetivo:** Irrelevante")
                st.session_state['cliente_obj']= "Irrelevante"

    # Botón para confirmar indicadores y hacer el perfil
    col1, col2 = st.columns([2, 1], vertical_alignment="center")
    with col1:
        container_error = st.container()
    with col2:
        cargando_inds= False
        if st.session_state["inds_cargados"]==False:
            cargando_inds= True
            st.badge("Descargando información...", icon= "ℹ️", color="orange")
            if st.button(label="Actualizar estado de la descarga", icon="🔄", use_container_width=True):
                st.rerun()
        if st.button("Confirmar selección", type="primary", disabled= cargando_inds, use_container_width=True):
            if st.session_state["ok_indicadores"] == False:
                if st.session_state["ok_caracteristicas"] == False:
                    with container_error:
                        st.error("No has seleccionado ni los indicadores ni las características de la empresa")
                else:
                    with container_error:
                        st.error("No has seleccionado los indicadores")
            elif st.session_state["ok_caracteristicas"] == False:
                with container_error:
                    st.error("No has seleccionado las características de la empresa")
            else:
                st.session_state["pag_actual"] = "Perfil estrategico"
                if not p.obtener_perfiles_usuario(st.session_state["user_act"]):
                    st.rerun()
                else:
                    comparar_ind()


@st.dialog("¿Quieres añadir la comparación con alguno de tus perfiles?")
def comparar_ind():
    mnsj=""
    nombres_perfiles= [perfil[1] for perfil in p.obtener_perfiles_usuario(st.session_state["user_act"])]
    with st.container(height= 300):
        eleccion= st.radio("Elige tu perfil para compararlo", nombres_perfiles, index= None)
    col1, col2= st.columns(2)
    with col1:
        if st.button("Confirmar selección", type="primary"):
            if eleccion == None:
                mnsj= "error"
            else:
                st.session_state["perfil_comp"]= p.get_perfil(eleccion, st.session_state["user_act"])
                st.rerun()
    if mnsj== "error":
        st.error("No has seleccionado ningún perfil")
    with col2:
            if st.button("Continuar sin comparar"):
                st.rerun()
