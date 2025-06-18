import streamlit as st
import queue as q
import uuid
import Paginas.inicio as inicio
import Paginas.indicadores as indicadores
import Paginas.empresas as empresas
import Paginas.seleccionados as seleccionados
import Paginas.perfil as perfil
import Paginas.home as home
import Paginas.ver_perfil as ver_perfil


# Variables necesarias
# Cambiar de pagina
if "pag_actual" not in st.session_state:
    st.session_state["pag_actual"] = "Inicio"
# Usuario que lo está usando
if "user_act" not in st.session_state:
    st.session_state["user_act"] = "Anonimo"
# Marcar que se han elegido los indicadores
if "ok_indicadores" not in st.session_state:
    st.session_state["ok_indicadores"] = False
# Marcar que se han elegido los indicadores
if "ok_caracteristicas" not in st.session_state:
    st.session_state["ok_caracteristicas"] = False
# Para guardar las caraterísticas de las empresas
if "sector_emp" not in st.session_state:
    st.session_state["sector_emp"] = []
if "tamaño_emp" not in st.session_state:
    st.session_state["tamaño_emp"] = []
if "tipo_emp" not in st.session_state:
    st.session_state["tipo_emp"] = []
if "ambito_emp" not in st.session_state:
    st.session_state["ambito_emp"] = []
if "importacion_emp" not in st.session_state:
    st.session_state["importacion_emp"] = []
if "exportacion_emp" not in st.session_state:
    st.session_state["exportacion_emp"] = []
if "sostenibilidad_emp" not in st.session_state:
    st.session_state["sostenibilidad_emp"] = []
if "sexo_emp" not in st.session_state:
    st.session_state["sexo_emp"] = []
if "edad_emp" not in st.session_state:
    st.session_state["edad_emp"] = []
if "creencias_emp" not in st.session_state:
    st.session_state["creencias_emp"] = []
if "cliente_obj" not in st.session_state:
    st.session_state["cliente_obj"] = None
# Guardar los indicadores que se han seleccionado
if "inds_seleccionados" not in st.session_state:
    st.session_state["inds_seleccionados"] = []
# Saber si guardar todos los indicadores o aactualizar
if "primera_carga" not in st.session_state:
    st.session_state["primera_carga"] = False
# Saber si se han cargado los datos de los indicadores en segundo plano
if "inds_cargados" not in st.session_state:
    st.session_state["inds_cargados"] = True
if "cola_cargados" not in st.session_state:
    st.session_state["cola_cargados"] = q.Queue()
# Saber si se ha verificado el correo y comprobar que no lo cambie
if "cmp_correo" not in st.session_state:
    st.session_state["cmp_correo"] = False
# Guardar el correo para comparar  si hay cambio
if "correo_aux" not in st.session_state:
    st.session_state["correo_aux"] = None
# Saber si se ha enviado el correo de verificación
if "enviado_ok" not in st.session_state:
    st.session_state["enviado_ok"] = False
# Saber si se han metido todos los datos correctamente
if "todo_ok" not in st.session_state:
    st.session_state["todo_ok"] = True
# Saber si el código es correcto 
if "cod_ok" not in st.session_state:
    st.session_state["cod_ok"] = False
# Saber si se ha comprobado el codigo
if "cod_conf" not in st.session_state:
    st.session_state["cod_conf"] = False
# Saber si se ha guardado el perfil que se acaba de hacer
if "perfil_guardado" not in st.session_state:
    st.session_state["perfil_guardado"]= False
# Guardar el perfil para verlo
if "perfil_para_ver" not in st.session_state:
    st.session_state["perfil_para_ver"]= None
# Guardar el perfil para compararlo
if "perfil_comp" not in st.session_state:
    st.session_state["perfil_comp"]= None
# Generar claves para inputs vacíos
st.session_state["key_aux"] = str(uuid.uuid4())

# Mostrar la página actual
match st.session_state["pag_actual"]:
    case "Inicio":
        inicio.main()
    case "Selección de indicadores":
        indicadores.main()
    case "Selección de características de la empresa":
        empresas.main()
    case "Confirmar selección":
        seleccionados.main()
    case "Perfil estrategico":
        perfil.main()
    case "Home":
        home.main()
    case "Ver perfil":
        ver_perfil.main()