import streamlit as st
from Paginas import perfil
from BD.gestor_inds import Indicador as ind
import datetime
import Analisis.helpers as h
from Analisis.pdf import PDF_logo
import os

def main():
    # Configuración de la página
    st.set_page_config(page_title="Ver perfil", layout="wide")

    # Coger los datos del perfil
    inds= st.session_state["perfil_para_ver"][4]
    indicadores_num= [int(x.strip()) for x in inds.split(", ")]
    indicadores= [ind.get_Indicador(indi) for indi in indicadores_num]
    sector= st.session_state["perfil_para_ver"][5]
    tamaño= st.session_state["perfil_para_ver"][6]
    tipo= st.session_state["perfil_para_ver"][7]
    ambito= st.session_state["perfil_para_ver"][8]
    importacion= st.session_state["perfil_para_ver"][9]
    exportacion= st.session_state["perfil_para_ver"][10]
    sostenibilidad= st.session_state["perfil_para_ver"][11]
    sexo= st.session_state["perfil_para_ver"][12]
    edad= st.session_state["perfil_para_ver"][13]
    creencia= st.session_state["perfil_para_ver"][14]
    # Filtrar los que no sean "Irrelevante"
    selecciones = [x for x in [sexo, edad, creencia] if x != "Irrelevante"]

    # Crear variable cliente_obj según selección
    if selecciones:
        cliente_obj = ", ".join(selecciones)
    else:
        cliente_obj = "Irrelevante"

     # Logo de la aplicación
    st.logo("Paginas/Logo.png", size="large")

    # Título de la página
    st.markdown("<style>.block-container {padding-top: 2.5rem;}</style>", unsafe_allow_html=True)
    st.markdown(
    f"""
    <div style='text-align: center; line-height: 1.1;'>
        <span style='font-size: 2.5em; font-weight: bold; margin-right: 10px;'>{st.session_state['perfil_para_ver'][1]}</span>
        <span style='font-size: 1.5em;'>(Creado el {st.session_state['perfil_para_ver'][2]})</span>
    </div>
    """,
    unsafe_allow_html=True
)




    # Titulos perfil e información de indicadores
    coltit1, coltit2=  st.columns([1, 1], gap="Large", vertical_alignment="center")
    with coltit1:
        st.write(" ")
        st.markdown("<h3 style='text-align: center;'>Información de indicadores</h3>", unsafe_allow_html=True)
    with coltit2:
        st.write(" ")
        st.markdown("<h3 style='text-align: center;'>Gráfica del perfil estratégico</h3>", unsafe_allow_html=True)
        
    # Información indicadores y gráfica del perfil
    colI, col1, colM, col2, colD = st.columns([1, 3, 1, 3, 1], gap="large", vertical_alignment="top")
    with col1:
        st.write(" ")
        with st.container(height= 350, border=False):
            inds_nombres= [ind.get_name(indicador[0]) for indicador in indicadores]
            inds_fuentes= [ind.get_fuente(indicador[0]) for indicador in indicadores]
            fuentes= list(dict.fromkeys(inds_fuentes))
            inds_nombres.sort()
            for indicador in inds_nombres:
                indicador_info= ind.get_Indicador_name(indicador)
                with st.popover(f"{indicador_info[1]}", use_container_width=True):
                    st.markdown("<div style='width: 300px'></div>", unsafe_allow_html=True)
                    tabInfo, tabJust, tabGraf, tabPron = st.tabs(["ℹ️", "❔", "📈","🧠Pronóstico"])
                    with tabJust:
                        l, just= ind.valores_perfil(indicador_info[0], sector, tamaño, tipo, ambito, importacion, exportacion, sostenibilidad, sexo, edad, creencia, False, st.session_state["perfil_para_ver"][0], True)
                        if ind.sube_o_baja(indicador_info[0], st.session_state["perfil_para_ver"][0], True) == "Sube" or ind.sube_o_baja(indicador_info[0], st.session_state["perfil_para_ver"][0], True) == "Sube mucho":
                            st.write(f"{ind.sube_o_baja(indicador_info[0], st.session_state['perfil_para_ver'][0], True)} -> {indicador_info[11]}")
                        elif ind.sube_o_baja(indicador_info[0], st.session_state["perfil_para_ver"][0], True) == "Baja" or ind.sube_o_baja(indicador_info[0], st.session_state["perfil_para_ver"][0], True) == "Baja mucho":
                            st.write(f"{ind.sube_o_baja(indicador_info[0], st.session_state['perfil_para_ver'][0], True)} -> {indicador_info[13]}")
                        else:
                            st.write(f"{ind.sube_o_baja(indicador_info[0], st.session_state['perfil_para_ver'][0], True)}")
                        st.write(f"**{h.valor_letras(l)} ({l})**")
                        st.write(just)
                    with tabInfo:
                        st.write(f"""
                        **{indicador_info[2]}**\n
                        {indicador_info[4]}\n\n\n
                        *Unidades:* {indicador_info[5]}\n
                        *Periodicidad:* {indicador_info[7]}\n
                        *Fuente:* {indicador_info[8]} - Disponibles el {st.session_state["perfil_para_ver"][2]}""")
                    with tabGraf:
                        perfil.graficas_indicadores(indicador_info[0], st.session_state["perfil_para_ver"][0], True)
                    with tabPron:
                        st.markdown("<h2 style='font-size:20px;'>Predicción del próximo año:</h2>", unsafe_allow_html=True)
                        v_futuro, evol, fiab= ind.pronostico(indicador_info[0], st.session_state["perfil_para_ver"][0], True)
                        st.write(f"**Posible valor:** {v_futuro}{indicador_info[6]}")
                        st.write(f"**Evolución:** {evol}")
                        st.write(f"**Fiabilidad de la predicción:** {fiab}")
                        st.caption("Predicción realizada con el algoritmo RandomForestRegressor")
    with col2:
        with st.container(height= 350, border=False):
            st.plotly_chart(perfil.graf_perfil(indicadores, sector, tamaño, tipo, ambito, importacion, exportacion, sostenibilidad, sexo, edad, creencia, st.session_state["perfil_para_ver"][0], True), use_container_width=False, config={"displayModeBar": True})
    col0, colbtn1, colbtn2= st.columns([1,2,2], vertical_alignment="center")
    # Para el boton de descargar informe
    with colbtn1:
        buffer_pdf= PDF_logo.crear_pdf(sector, tamaño, tipo, ambito, importacion, exportacion, sostenibilidad, sexo, edad, creencia, fuentes, cliente_obj, st.session_state["perfil_para_ver"][2], st.session_state["perfil_para_ver"][0], True, st.session_state["perfil_para_ver"][1])
        st.download_button(
            label="⬇️ Descargar informe",
            data= buffer_pdf,
            file_name="Perfil estratégico.pdf",
            mime="text/plain"
            )
    with colbtn2:
        if st.button("Volver al inicio", type="primary"):
            os.remove("Graf_perfil.png")
            st.session_state["pag_actual"] = "Home"  # Cambiar la página
            st.session_state["perfil_para_ver"]= None
            st.rerun()