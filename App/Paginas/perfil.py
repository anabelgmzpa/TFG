import streamlit as st
from Analisis.pdf import PDF_logo
import Analisis.helpers as h
import pandas as pd
from BD.gestor_inds import Indicador as i
from BD.gestor_perfiles import Perfil as p
import plotly.graph_objects as go
import plotly.io as pio
import datetime
import os

def main():
    # Configuración de la página
    st.set_page_config(page_title="Perfil estrategico", layout="wide")

    # Menu de navegación
    paginas = {
        "Selección de indicadores": "↩️",
        "Selección de características de la empresa": "↩️"
    }
    for pag, icono in paginas.items():
        if st.sidebar.button(f"{pag}", icon= icono, use_container_width=True):
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
    st.markdown("<h1 style='text-align: center;'>Perfil estratégico</h1>", unsafe_allow_html=True)

    # Titulos perfil e información de indicadores
    coltit1, coltit2=  st.columns([1, 1], gap="Large", vertical_alignment="center")
    with coltit1:
        st.markdown("<h3 style='text-align: center;'>Información de indicadores</h3>", unsafe_allow_html=True)
    with coltit2:
        st.markdown("<h3 style='text-align: center;'>Gráfica del perfil estratégico</h3>", unsafe_allow_html=True)
        
    # Información indicadores y gráfica del perfil
    colI, col1, colM, col2, colD = st.columns([1, 3, 1, 3, 1], gap="large", vertical_alignment="top")
    with col1:
        st.write(" ")
        with st.container(height= 330, border=False):
            inds_nombres= [i.get_name(indicador[0]) for indicador in st.session_state["inds_seleccionados"]]
            inds_fuentes= [i.get_fuente(indicador[0]) for indicador in st.session_state["inds_seleccionados"]]
            fuentes= list(dict.fromkeys(inds_fuentes))
            inds_nombres.sort()
            for indicador in inds_nombres:
                indicador_info= i.get_Indicador_name(indicador)
                with st.popover(f"{indicador_info[1]}", use_container_width=True):
                    st.markdown("<div style='width: 300px'></div>", unsafe_allow_html=True)
                    if not st.session_state["perfil_comp"]:
                        tabInfo, tabJust, tabGraf, tabPron = st.tabs(["ℹ️", "❔", "📈","🧠Pronóstico"])
                    else:
                        tabInfo, tabJust, tabGraf, tabPron, tabComp = st.tabs(["ℹ️", "❔", "📈","🧠Pronóstico", "🔍Comparación"])
                    with tabJust:
                        l, just= i.valores_perfil(indicador_info[0], st.session_state["sector_emp"], st.session_state["tamaño_emp"], st.session_state["tipo_emp"], st.session_state["ambito_emp"], st.session_state["importacion_emp"], st.session_state["exportacion_emp"], st.session_state["sostenibilidad_emp"], st.session_state["sexo_emp"], st.session_state["edad_emp"], st.session_state["creencias_emp"])
                        if i.sube_o_baja(indicador_info[0]) == "Sube" or i.sube_o_baja(indicador_info[0]) == "Sube mucho":
                            st.write(f"{i.sube_o_baja(indicador_info[0])} -> {indicador_info[11]}")
                        elif i.sube_o_baja(indicador_info[0]) == "Baja" or i.sube_o_baja(indicador_info[0]) == "Baja mucho":
                            st.write(f"{i.sube_o_baja(indicador_info[0])} -> {indicador_info[13]}")
                        else:
                            st.write(f"{i.sube_o_baja(indicador_info[0])}")
                        st.write(f"**{h.valor_letras(l)} ({l})**")
                        st.write(just)
                    with tabInfo:
                        st.write(f"""
                        **{indicador_info[2]}**\n
                        {indicador_info[4]}\n\n\n
                        *Unidades:* {indicador_info[5]}\n
                        *Periodicidad:* {indicador_info[7]}\n
                        *Fuente:* {indicador_info[8]} - Disponibles el {datetime.date.today()}""")
                    with tabGraf:
                        graficas_indicadores(indicador_info[0])
                    with tabPron:
                        st.markdown("<h2 style='font-size:20px;'>Predicción del próximo año:</h2>", unsafe_allow_html=True)
                        v_futuro, evol, fiab= i.pronostico(indicador_info[0])
                        st.write(f"**Posible valor:** {v_futuro}{indicador_info[6]}")
                        st.write(f"**Evolución:** {evol}")
                        st.write(f"**Fiabilidad de la predicción:** {fiab}")
                        st.caption("Predicción realizada con el algoritmo RandomForestRegressor")
                    if st.session_state["perfil_comp"]:
                        with tabComp:
                            st.markdown(f"<h2 style='font-size:20px;'>Comparación con el perfil <i>'{st.session_state['perfil_comp'][1]}':</i></h2>", unsafe_allow_html=True)
                            if indicador_info[0] in p.get_inds(st.session_state['perfil_comp'][0]):
                                fecha_guardada, dato_guardado, fecha_nueva, dato_nuevo, txt= comparar_datos(indicador_info[0])
                                st.write(f"**Último valor guardado:** {dato_guardado:.3f} {indicador_info[6]} ({fecha_guardada})")
                                st.write(f"**Valor actual:** {dato_nuevo:.3f} {indicador_info[6]} ({fecha_nueva})")
                                st.write(f"**Comparación:** {txt}")
                            else:
                                st.badge(f"'{st.session_state['perfil_comp'][1]}' no analiza este indicador", icon="❌", color="red")

    with col2:
        with st.container(height= 330, border=False):
            st.plotly_chart(graf_perfil(st.session_state["inds_seleccionados"], st.session_state["sector_emp"], st.session_state["tamaño_emp"], st.session_state["tipo_emp"], st.session_state["ambito_emp"], st.session_state["importacion_emp"], st.session_state["exportacion_emp"], st.session_state["sostenibilidad_emp"], st.session_state["sexo_emp"], st.session_state["edad_emp"], st.session_state["creencias_emp"]), use_container_width=False, config={"displayModeBar": True})
    # Mensaje del perfil guardado
    cola, colb, colc= st.columns([1,5,1])
    with colb:
        if st.session_state["perfil_guardado"]:
            st.success("Perfil guardado correctamente")
    # Columnas para botones
    col0, colbtn1, colbtn2, colbtn3= st.columns([1,2,2,2], vertical_alignment="center")
    if st.session_state["user_act"] != "Anonimo":
        with colbtn1:
            if st.button("💾 Guardar perfil"):
                st.session_state["perfil_guardado"]= False
                guardar_perfil()
    # Para el boton de descargar informe
    with colbtn2:
        buffer_pdf= PDF_logo.crear_pdf(st.session_state["sector_emp"], st.session_state["tamaño_emp"], st.session_state["tipo_emp"], st.session_state["ambito_emp"], st.session_state["importacion_emp"], st.session_state["exportacion_emp"], st.session_state["sostenibilidad_emp"], st.session_state["sexo_emp"], st.session_state["edad_emp"], st.session_state["creencias_emp"], fuentes, st.session_state["cliente_obj"])
        st.download_button(
            label="⬇️ Descargar informe",
            data= buffer_pdf,
            file_name="Perfil estratégico.pdf",
            mime="text/plain"
            )
    with colbtn3:
        if st.button("Finalizar", type="primary"):
            os.remove("Graf_perfil.png")
            if st.session_state["user_act"] != "Anonimo":
                st.session_state["pag_actual"] = "Home"  # Cambiar la página
                st.rerun()
            else:
                st.session_state["pag_actual"] = "Inicio"  # Cambiar la página
                st.rerun()



@st.dialog("Guardar Perfil Estratégico")
def guardar_perfil():
    inds= [indicador[0] for indicador in st.session_state["inds_seleccionados"]]
    inds_str = ", ".join(str(num) for num in inds)
    k = st.session_state["key_aux"]
    nombre= st.text_input("Nombre del perfil",max_chars=30 ,key=f"username_{k}")
    st.write(f"**Fecha de creación:** {datetime.date.today()}")
    if st.button("Guardar", type="primary"):
        if nombre:
            if p.nombre_existe(nombre, st.session_state["user_act"]):
                st.error("Ya tienes un perfil con este nombre")
            else:
                p.guardar_perfil(nombre, str(datetime.date.today()), st.session_state["user_act"], inds_str, st.session_state["sector_emp"], st.session_state["tamaño_emp"], st.session_state["tipo_emp"], st.session_state["ambito_emp"], st.session_state["importacion_emp"], st.session_state["exportacion_emp"], st.session_state["sostenibilidad_emp"], st.session_state["sexo_emp"], st.session_state["edad_emp"], st.session_state["creencias_emp"])
                st.session_state["perfil_guardado"]= True
                st.rerun()
        else:
            st.error("No has introducido ningún nombre")

# Graficas para ver la evolucion de los indicadores seleccionados
def graficas_indicadores(indicador, perfil="", verPerfil=False):
    fechas, datos= i.fechas_datos(indicador, perfil, verPerfil)
    data= pd.DataFrame(datos, fechas)
    st.line_chart(data, y_label= i.get_uds(indicador))


# Grafica del perfil estrategico
def graf_perfil(indicadores, sector, tamaño, tipo, ambito, importacion, exportacion, sostenibilidad, sexo, edad, creencia, perfil="", verPerfil=False):
    nombres= []
    letras= []
    # Datos
    for indicador in indicadores:
        nombres.append(i.get_name(indicador[0]))
        l, just= i.valores_perfil(indicador[0], sector, tamaño, tipo, ambito, importacion, exportacion, sostenibilidad, sexo, edad, creencia, False, perfil, verPerfil)                       
        letras.append(l)
    dicc= dict(zip(nombres, letras))
    nombres.sort()
    nombres.reverse()
    y = [wrap_label(nombre) for nombre in nombres]
    x = [dicc[nombre] for nombre in nombres]
    
    # Crear gráfico Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Mi línea'))
    # Asegurar que todos los valores del eje x estén presentes
    for value in ["MN", "N", "E", "P", "MP"]:
        if value not in x:
            fig.add_trace(go.Scatter(x=[value], y=[None], mode='markers', marker=dict(opacity=0), showlegend=False))
    # Personalizar el texto emergente (hover) para que no muestre el nombre de la línea
    fig.update_traces(hovertemplate='<b>%{y}</b>: %{x}<extra></extra>')
    fig.update_layout(
        template='plotly_white',
        xaxis=dict(side='top', showgrid=True, categoryorder="array", categoryarray=["MN", "N", "E", "P", "MP"]),
        yaxis=dict(showgrid=True), 
        showlegend=False,
        height= 80 * len(indicadores),
    )
    #Guardar grafico en memoria
    pio.write_image(fig, "Graf_perfil.png", format='png')
    return fig

def wrap_label(label, max_width=20):
    words = label.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + " " + word) <= max_width:
            current_line += (" " if current_line else "") + word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return "<br>".join(lines)


def comparar_datos(indicador):
    fechas_guardado, datos_guardado= i.fechas_datos(indicador, st.session_state['perfil_comp'][0], True)
    last_fechas_guardado= fechas_guardado[-1]
    last_datos_guardado= datos_guardado[-1]
    fechas_nuevo, datos_nuevo= i.fechas_datos(indicador)
    last_fechas_nuevo = fechas_nuevo[-1]
    last_datos_nuevo = datos_nuevo[-1]
    if last_datos_guardado > last_datos_nuevo:
        porc= 100 - (last_datos_nuevo/last_datos_guardado*100)
        res= f"Ha bajado un {porc}%"
    elif last_datos_guardado < last_datos_nuevo:
        porc= 100 - (last_datos_guardado/last_datos_nuevo*100)
        res= f"Ha subido un {porc:.3f}%"
    else:
        res= "Se ha mantenido"
    return last_fechas_guardado, last_datos_guardado, last_fechas_nuevo, last_datos_nuevo, res