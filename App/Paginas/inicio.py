import streamlit as st
import Analisis.helpers as h
from BD.gestor_inds import Indicador as i
from BD.gestor_users import Usuario as u

def main():
    # Configuración de la página
    st.set_page_config(page_title="Inicio")

    st.markdown("<style>.block-container {padding-top: 1.8rem;}</style>", unsafe_allow_html=True)
    col1, col2= st.columns([1,5], vertical_alignment="bottom")
    with col1:
        st.image("Paginas/Logo.png", width= 150)
    with col2:
        # Título de la página
        st.markdown("<h1 style='text-align: center;'>CREACIÓN DE UN PERFIL ESTRATÉGICO</h1>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.write("")


    col1, col2, col3 = st.columns([5, 1, 3], vertical_alignment="center")
    with col1:
        # Descripción
        st.write("""
        Con esta aplicación podrás crear un perfil estratégico para tu empresa.\n
        Es una herramienta muy útil que permite interpretar diferentes indicadores y ver cómo afectan a tu empresa dependiendo de sus características.
        """)
        st.write("")
        # Pasos
        st.subheader("Pasos a seguir")
        st.write("""
        1º Selecciona los indicadores que te interesen.\n
        2º Selecciona las características de tu empresa.\n
        3º Genera el perfil estratégico.
                """)
    # Para iniciar sesión
    with col3:
        with st.container(height=300, border=True):
            st.write(" ")
            st.write(" ")
            st.markdown("<div style='text-align: center;'>Inicia sesión para poder guardar y comparar tus perfiles estratégicos.</div>", unsafe_allow_html=True)
            st.write(" ")
            st.write(" ")
            if st.button(label="Registrarse", type="primary", use_container_width=True):
                h.reiniciar_selecciones_registrarUser()
                registrarse()
            if st.button(label="Iniciar sesión",  type="primary", use_container_width=True):
                iniciar_sesion()


    # Botón para navegar a la página de indicadores, centrado
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.write("")
        st.write("")
        st.write("")
        if st.button("Continuar sin iniciar sesión"):
            st.session_state["user_act"] = "Anonimo"
            st.session_state["pag_actual"] = "Selección de indicadores"
            # Reiniciar selecciones y BD
            h.reiniciar_selecciones_crearPerfil()
            i.borrar_seleccionados()
            st.rerun()







@st.dialog("Regístrate en EstrategIApp")
def registrarse():
    k = st.session_state["key_aux"]
    mnsj=""
    # Entradas
    username = st.text_input("Nombre de usuario", key=f"username1_{k}")
    pwd = st.text_input("Contraseña (mín. 6 caracteres, 1 mayúscula y 1 número)", key=f"pwd1_{k}", type="password")
    correo = st.text_input("Correo electrónico (@gmail.com)", key=f"email_{k}")


    # Botón: Verificar correo
    if st.button("Verificar correo"):
        if not correo:
            st.error("Debes rellenar el correo")
        elif st.session_state["cod_conf"]:
            st.error("Ya has verificado el correo")
        else:
            ok_correo, error_correo = u.email_ok(correo)
            if ok_correo:
                enviado_ok, cod_enviado = u.mandar_email(correo)
                st.session_state["enviado_ok"] = enviado_ok
                st.session_state["cod_enviado"] = cod_enviado
                st.session_state["correo_aux"] = correo
                st.session_state["cmp_correo"] = True
                if enviado_ok:
                    st.info(f"Código enviado a {correo}")
                else:
                    st.error("No se pudo mandar el código")
            else:
                st.error(error_correo)

    # Código de verificación
    col1, col2 = st.columns([5, 2], vertical_alignment="bottom")
    with col1:
        codigo = st.text_input("Introduzca el código enviado a su correo electrónico", key=f"cod_{k}")
    with col2:
        if st.button("Comprobar código"):
            if not st.session_state["enviado_ok"]:
                mnsj="noCod"
            elif not codigo:
                mnsj="vacio"
            elif codigo == st.session_state["cod_enviado"]:
                mnsj="ok"
                st.session_state["cod_conf"] = True
                st.session_state["cod_ok"] = True
            else:
                st.session_state["cod_ok"] = False
                mnsj="noOk"
    if mnsj=="noCod":
        st.error("Primero debes solicitar el código con 'Verificar correo'")
    elif mnsj=="vacio":
        st.error("No has introducido ningún código")
    elif mnsj=="noOk":
        st.error("Código incorrecto")
    elif mnsj=="ok":
        st.success("Código correcto")

    # Botón: Registrarse
    if st.button("Registrarse", type="primary"):
        st.session_state["todo_ok"] = True  # Presuponemos que todo va bien

        # Paso 1: Todos los campos deben estar llenos
        if not username or not pwd or not correo:
            st.session_state["todo_ok"] = False
            st.error("Debes rellenar todos los campos superiores")

        # Paso 2: Validar username y contraseña
        if st.session_state["todo_ok"]:
            errores = False
            if u.username_existe(username):
                st.error("El nombre de usuario ya existe")
                errores = True
            ok_pwd, error_pwd = u.contraseña_valida(pwd)
            if not ok_pwd:
                st.error(error_pwd)
                errores = True
            if errores:
                st.session_state["todo_ok"] = False

        # Paso 3: Verificación de correo realizada
        if st.session_state["todo_ok"] and not st.session_state["enviado_ok"]:
            st.session_state["todo_ok"] = False
            st.error("Debes verificar tu correo electrónico")

        # Paso 4: Código verificado correctamente
        if st.session_state["todo_ok"] and not st.session_state["cod_ok"]:
            st.session_state["todo_ok"] = False
            st.error("Debes comprobar el código que se te ha mandado al correo")

        # Paso 5: Que no se haya cambiado el correo
        if st.session_state["todo_ok"] and st.session_state["correo_aux"] != correo:
            st.session_state["todo_ok"] = False
            st.error("El correo no es el que se ha verificado")

        # Crear usuario si todo está correcto
        if st.session_state["todo_ok"]:
            u.crear_usuario(username, pwd, correo)
            st.success("Usuario creado correctamente, ya puedes iniciar sesión")

        
         

# Pantalla para iniciar sesión
@st.dialog("Inicia sesión en EstrategIApp")
def iniciar_sesion():
    k = st.session_state["key_aux"]
    mnsj= ""
    username = st.text_input("Nombre de usuario", key=f"username_{k}")
    pwd = st.text_input("Contraseña (mín. 6 caracteres, 1 mayúscula  y 1 número)", key=f"pwd_{k}", type="password")
    if st.button("Iniciar sesión", type="primary"):
        if username and pwd:
            res, error= u.inicio_ok(username, pwd)
            if res:
                st.session_state["user_act"] = username
                st.session_state["pag_actual"]= "Home"
                st.rerun()
            else:
                st.error(error)
        else:
            st.error("Debes rellenar todos los campos superiores")
    with st.expander("Recuperar contraseña"):
        col1, col2= st.columns([2,1], vertical_alignment="center")
        with col1:
            correo= st.text_input("Correo electrónico (@gmail.com)", key=f"email1_{k}")
        with col2:
            if st.button("Enviar nueva contraseña"):
                if correo:
                    if u.email_existe(correo):
                        ok= u.mandar_pwd(correo)
                        if ok:
                            mnsj= "ok"
                        else:
                            mnsj= "error"
                    else:
                        mnsj="noExiste"
                else:
                    mnsj="vacio"
        if mnsj=="noExiste":
            st.error("No existe ningún usuario con este correo electrónico")
        elif mnsj=="vacio":
            st.error("Debes escribir tu correo electrónico")
        elif mnsj=="error":
            st.error("No se pudo mandar el código")
        elif mnsj=="ok":
            st.info(f"Nueva contraseña enviada a {correo}")