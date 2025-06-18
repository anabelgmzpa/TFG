import streamlit as st
import queue as q

# Función para saber si un indicador está seleccionado
# ind = id
def esta_seleccionado(indicador, lista):
    for ind in lista:
        if ind == indicador:
            return True
    return False



# Función para saber si se han seleccionado los indicadores para el tick del menu
def menu1():
    if st.session_state["ok_indicadores"]== False:
        return "1️⃣"
    else:
        return "✅"
    


# Función para saber si se han seleccionado los indicadores para el tick del menu
def menu2():
    if st.session_state["ok_caracteristicas"] == False:
        return "2️⃣"
    else:
        return "✅"
        


# Función para borrar las selecciones cuando se reinicia la cración del perfil
def reiniciar_selecciones_crearPerfil():
    st.session_state["ok_indicadores"] = False
    st.session_state["ok_caracteristicas"] = False
    st.session_state["inds_seleccionados"] = []
    st.session_state["sector_emp"] = None
    st.session_state["tamaño_emp"] = None
    st.session_state["tipo_emp"] = None
    st.session_state["ambito_emp"] = None
    st.session_state["importacion_emp"] = None
    st.session_state["exportacion_emp"] = None
    st.session_state["sostenibilidad_emp"] = None
    st.session_state["sexo_emp"] = None
    st.session_state["edad_emp"] = None
    st.session_state["creencias_emp"] = None
    st.session_state["cliente_obj"] = None
    st.session_state["primera_carga"] = False
    st.session_state["inds_cargados"] = None
    st.session_state["cola_cargados"] = q.Queue()
    st.session_state["perfil_guardado"]= False

# Función para borrar las selecciones cuando se registra el usuario
def reiniciar_selecciones_registrarUser():
    st.session_state["cmp_correo"] = False
    st.session_state["correo_aux"] = None
    st.session_state["enviado_ok"] = False
    st.session_state["todo_ok"] = True
    st.session_state["cod_ok"] = False
    

# Saber el valor de las letras del perfil
def valor_letras(l):
    if l=="MN":
        return "Muy negativo"
    elif l=="N":
        return "Negativo"
    elif l=="E":
        return "Neutro"
    elif l=="P":
        return "Positivo"
    elif l=="MP":
        return "Muy positivo"
