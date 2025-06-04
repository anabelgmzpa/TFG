import streamlit as st 
from BD.gestor_inds import Indicador as i
import Analisis.helpers as h
import threading as t
DB_PATH = "BD/indicadores.db"



def main():
    # Configuración de la página
    st.set_page_config(page_title="Selección de indicadores")

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
    

    # Obtener indicadores de la base de datos
    indicadores = sorted(i.obtener_indicadores(DB_PATH), key=lambda x: x[1])

    # Variable local auxiliar
    seleccionados= []

    # Logo de la aplicación
    st.logo("Paginas/Logo.png", size="large")

    # Título de la página
    st.markdown("<style>.block-container {padding-top: 1.8rem;}</style>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Selección de los indicadores</h1>", unsafe_allow_html=True)
    

    # TABS DE INDICADORES
    # Tabs para cada categoría de indicadores
    tabP, tabE, tabS, tabT, tabE2= st.tabs(["Político-Legal", "Económico", "Social", "Tecnológico", "Ecológico"])

    # Indicadores políticos
    with tabP:
        with st.container(height= 450):
            for indicador in indicadores:
                if str(indicador[0]).startswith("1"):
                    info= f"""
                    **{indicador[2]}**\n
                    {indicador[4]}\n\n\n
                    *Unidades:* {indicador[5]}\n
                    *Periodicidad:* {indicador[7]}\n
                    *Fuente:* {indicador[8]}"""
                    id_inds_seleccionados=[indicador[0] for indicador in st.session_state["inds_seleccionados"]]
                    seleccionado= st.checkbox(indicador[1], value=h.esta_seleccionado(indicador[0], id_inds_seleccionados), help=info)
                    if seleccionado and not h.esta_seleccionado(indicador[0], st.session_state["inds_seleccionados"]):
                        seleccionados.append(indicador)
                    elif not seleccionado and h.esta_seleccionado(indicador[0], st.session_state["inds_seleccionados"]):
                        seleccionados.remove(indicador)

    # Indicadores económicos
    with tabE:
        with st.container(height= 450):
            for indicador in indicadores:
                if str(indicador[0]).startswith("2"):
                    info= f"""
                    **{indicador[2]}**\n
                    {indicador[4]}\n\n\n
                    *Unidades:* {indicador[5]}\n
                    *Periodicidad:* {indicador[7]}\n
                    *Fuente:* {indicador[8]}"""
                    id_inds_seleccionados=[indicador[0] for indicador in st.session_state["inds_seleccionados"]]
                    seleccionado= st.checkbox(indicador[1], value=h.esta_seleccionado(indicador[0], id_inds_seleccionados), help=info)
                    if seleccionado and not h.esta_seleccionado(indicador[0], st.session_state["inds_seleccionados"]):
                        seleccionados.append(indicador)
                    elif not seleccionado and h.esta_seleccionado(indicador[0], st.session_state["inds_seleccionados"]):
                        seleccionados.remove(indicador)

    # Indicadores sociales
    with tabS:
        with st.container(height= 450):
            for indicador in indicadores:
                if str(indicador[0]).startswith("3"):
                    info= f"""
                    **{indicador[2]}**\n
                    {indicador[4]}\n\n\n
                    *Unidades:* {indicador[5]}\n
                    *Periodicidad:* {indicador[7]}\n
                    *Fuente:* {indicador[8]}"""
                    id_inds_seleccionados=[indicador[0] for indicador in st.session_state["inds_seleccionados"]]
                    seleccionado= st.checkbox(indicador[1], value=h.esta_seleccionado(indicador[0], id_inds_seleccionados), help=info)
                    if seleccionado and not h.esta_seleccionado(indicador[0], st.session_state["inds_seleccionados"]):
                        seleccionados.append(indicador)
                    elif not seleccionado and h.esta_seleccionado(indicador[0], st.session_state["inds_seleccionados"]):
                        seleccionados.remove(indicador)
                
    # Indicadores tecnológicos            
    with tabT:      
        with st.container(height= 450):
            for indicador in indicadores:
                if str(indicador[0]).startswith("4"):
                    info= f"""
                    **{indicador[2]}**\n
                    {indicador[4]}\n\n\n
                    *Unidades:* {indicador[5]}\n
                    *Periodicidad:* {indicador[7]}\n
                    *Fuente:* {indicador[8]}"""
                    id_inds_seleccionados=[indicador[0] for indicador in st.session_state["inds_seleccionados"]]
                    seleccionado= st.checkbox(indicador[1], value=h.esta_seleccionado(indicador[0], id_inds_seleccionados), help=info)
                    if seleccionado and not h.esta_seleccionado(indicador[0], st.session_state["inds_seleccionados"]):
                        seleccionados.append(indicador)
                    elif not seleccionado and h.esta_seleccionado(indicador[0], st.session_state["inds_seleccionados"]):
                        seleccionados.remove(indicador)

    # Indicadores ecológicos            
    with tabE2:
        with st.container(height= 450):
            for indicador in indicadores:
                if str(indicador[0]).startswith("5"):
                    info= f"""
                    **{indicador[2]}**\n
                    {indicador[4]}\n\n\n
                    *Unidades:* {indicador[5]}\n
                    *Periodicidad:* {indicador[7]}\n
                    *Fuente:* {indicador[8]}"""
                    id_inds_seleccionados=[indicador[0] for indicador in st.session_state["inds_seleccionados"]]
                    seleccionado= st.checkbox(indicador[1], value=h.esta_seleccionado(indicador[0], id_inds_seleccionados), help=info)
                    if seleccionado and not h.esta_seleccionado(indicador[0], st.session_state["inds_seleccionados"]):
                        seleccionados.append(indicador)
                    elif not seleccionado and h.esta_seleccionado(indicador[0], st.session_state["inds_seleccionados"]):
                        seleccionados.remove(indicador)

    
    # Botón para guardar la selección de indicadores 
    col1, col2 = st.columns([2, 1], vertical_alignment="center")
    with col1:
        container_error = st.container()
    with col2:
        if st.button("Guardar selección", type="primary"):
            if len(seleccionados) < 5:
                with container_error:
                    st.error("Debes seleccionar mínimo 5 indicadores")
            else:
                # Scrap indicadores en segundo plano para no esperar
                ind_seleccionados= [indicador[0] for indicador in seleccionados]
                st.session_state["inds_cargados"]= False
                if not st.session_state["primera_carga"]:
                    t.Thread(target=i.intro_indicadores, args=(ind_seleccionados, st.session_state["cola_cargados"]), daemon=True).start()
                    st.session_state["inds_seleccionados"]= seleccionados
                    st.session_state["primera_carga"]= True
                else:
                    id_inds_seleccionados=[indicador[0] for indicador in st.session_state["inds_seleccionados"]]
                    t.Thread(target=i.act_indicadores, args=(id_inds_seleccionados, ind_seleccionados, st.session_state["cola_cargados"]), daemon=True).start()
                    st.session_state["inds_seleccionados"]= seleccionados
                    #i.act_indicadores(id_inds_seleccionados, ind_seleccionados)
                # Para saber a qué página ir
                if st.session_state["ok_caracteristicas"]:
                    st.session_state["pag_actual"] = "Confirmar selección"
                else:
                    st.session_state["pag_actual"] = "Selección de características de la empresa" 
                st.session_state["ok_indicadores"] = True
                st.rerun()