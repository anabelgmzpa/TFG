import streamlit as st
from BD.gestor_perfiles import Perfil as p
from BD.gestor_users import Usuario as u
import Analisis.helpers as h
from BD.gestor_inds import Indicador as i

def main():
    # Configuración de la página
    st.set_page_config(page_title="Home")

    # Logo de la aplicación
    st.logo("Paginas/Logo.png", size="large")

    # Título de la página
    st.markdown("<style>.block-container {padding-top: 1.8rem;}</style>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center;'>Bienvenid@, {st.session_state['user_act']}</h1>", unsafe_allow_html=True)

    col1, colM, col2 = st.columns([5, 1, 3], vertical_alignment="top")

    with col1:
        st.subheader("Tus perfiles estratégicos:")
        with st.container(height= 400, border=True):
            if not p.obtener_perfiles_usuario(st.session_state["user_act"]):
                st.badge("No tienes ningún perfil guardado.", color="red")
            else:
                for perfil in p.obtener_perfiles_usuario(st.session_state["user_act"]):
                    col11, col12, col13= st.columns([3,1,1], vertical_alignment="center")
                    with col11:
                        st.write(perfil[1])
                        st.caption(f"Creado el {perfil[2]}")
                    with col12:
                        if st.button("Ver", key=f"ver_{perfil[1]}"):
                            st.session_state["perfil_para_ver"]= perfil
                            st.session_state["pag_actual"]= "Ver perfil"
                            st.rerun()
                    with col13:
                        if st.button("🗑️", key=f"borrar_{perfil[1]}"):
                            borrar_perfil(perfil)
                    st.divider()
    with col2:
        st.subheader("Tu perfil:")
        st.text_input("**Nombre de usuario:**", value=st.session_state['user_act'], disabled=True)
        st.text_input("**Correo electrónico:**", value=u.get_email(st.session_state['user_act']), disabled=True)
        st.text_input("**Contraseña:**", value=u.get_pwd(st.session_state['user_act']), type="password", disabled=True)
        col21, col22, col23= st.columns([2,3,1])
        with col22:
            if st.button("Editar"):
                st.session_state["enviado_ok"]= False
                editar_perfil(st.session_state["user_act"])
        

    st.write(" ")
    st.write(" ")
    col1, colM, col2 = st.columns([5, 1, 3])
    with col1:
        # Botón para hacer el perfil estratégico
        if st.button("Crear un nuevo Perfil Estratégico", type="primary"):
            # Reiniciar selecciones y BD
            h.reiniciar_selecciones_crearPerfil()
            i.borrar_seleccionados()
            st.session_state["pag_actual"]= "Selección de indicadores"
            st.rerun()
    with col2:
        # Botón para salir
        if st.button(":red[Cerrar sesión]", icon="❌"):
            st.session_state["user_act"] = "Anonimo"
            st.session_state["pag_actual"]= "Inicio"
            st.rerun()


@st.dialog("Edita tu perfil")
def editar_perfil(usuario):
    k = st.session_state["key_aux"]
    st.write("El nombre de usuario no se puede cambiar")
    st.divider()
    # Cambiar el email
    new_email= st.text_input("**Nuevo correo electrónico (@gmail.com):**", key=f"email_edit_{k}")
    if st.button("Verificar correo"):
        if new_email:
            if new_email==u.get_email(usuario):
                st.error("Debes escribir un correo diferente al actual")
            else:
                ok_correo, error_correo = u.email_ok(new_email)
                if ok_correo:
                    enviado_ok, cod_enviado = u.mandar_email(new_email)
                    st.session_state["enviado_ok"] = enviado_ok
                    st.session_state["cod_enviado"] = cod_enviado
                    if enviado_ok:
                        st.info(f"Código enviado a {new_email}")
                    else:
                        st.error("No se pudo mandar el código")
                else:
                    st.error(error_correo)
        else:
            st.error("No se ha escrito un nuevo correo electrónico")
    # Comprobar el código
    codigo = st.text_input("Introduzca el código enviado a su correo electrónico", key=f"cod_{k}")
    if st.button("Comprobar código y cambiar correo", type="primary"):
        if not st.session_state["enviado_ok"]:
            st.error("Primero debes solicitar el código con 'Verificar correo'")
        elif not codigo:
            st.error("No has introducido ningún código")
        elif codigo == st.session_state["cod_enviado"]:
            u.set_email(new_email, usuario)
            st.success("Código correcto, correo electrónico cambiado correctamente")
        else:
            st.error("Código incorrecto")
    # Cambiar la contraseña, comprobando que cumpla las condiciones
    st.divider()
    new_pwd= st.text_input("**Nueva contraseña (mín. 6 caracteres, 1 mayúscula y 1 número):**", type="password", key=f"pwd_edit_{k}")
    if st.button("Cambiar contraseña", type="primary"):
        if new_pwd:
            ok_pwd, error_pwd = u.contraseña_valida(new_pwd)
            if new_pwd==u.get_pwd(usuario):
                st.error("Debes escribir una contraseña diferente a la actual")
            elif not ok_pwd:
                st.error(error_pwd)
            else:
                u.set_pwd(new_pwd, usuario)
                st.success("Contraseña cambiada correctamente")
        else:
            st.error("No se ha escrito una nueva contraseña")


@st.dialog("Borrar perfil estratégico")
# Perfl es entero, no id
def borrar_perfil(perfil):
    st.write(f"¿Estás seguro de que deseas eliminar tu pefil *'{perfil[1]}'*?")
    col0, col1, col2= st.columns([1,2,2])
    with col1:
        if st.button("Sí", type="primary"):
            p.borrar_perfil(perfil[0])
            st.rerun()
    with col2:
        if st.button("No", type="primary"):
            st.rerun()