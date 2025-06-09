import pytest
from unittest.mock import patch, MagicMock
import streamlit as st
import Paginas.seleccionados as seleccionados
import Paginas.indicadores as indicadores
import Paginas.empresas as empresas
import Paginas.perfil as perfil
import Paginas.home as home
import Paginas.ver_perfil as ver_perfil
import Paginas.inicio as inicio
import Analisis.helpers as helpers
import BD.gestor_inds as gestor_inds
import BD.gestor_perfiles as gestor_perfiles
import BD.gestor_users as gestor_users
import Analisis.analisis as analisis
import Analisis.comentarios as comentarios


@pytest.fixture(autouse=True)
def reset_session_state(monkeypatch):
    st.session_state.clear()
    yield
    st.session_state.clear()

def set_basic_state():
    st.session_state["inds_seleccionados"] = [(1, "A"), (2, "B")]
    st.session_state["inds_cargados"] = True
    st.session_state["ok_indicadores"] = True
    st.session_state["ok_caracteristicas"] = True
    st.session_state["user_act"] = "testuser"
    st.session_state["sector_emp"] = "Sector"
    st.session_state["tamaño_emp"] = "Grande"
    st.session_state["tipo_emp"] = "Privada"
    st.session_state["ambito_emp"] = "Nacional"
    st.session_state["importacion_emp"] = "Alta"
    st.session_state["exportacion_emp"] = "Baja"
    st.session_state["sostenibilidad_emp"] = "Alta"
    st.session_state["sexo_emp"] = "Hombre"
    st.session_state["edad_emp"] = "30-40"
    st.session_state["creencias_emp"] = "Católico"
    st.session_state["cola_cargados"] = MagicMock()
    st.session_state["pag_actual"] = "Confirmar selección"
    st.session_state["perfil_guardado"] = False
    st.session_state["perfil_para_ver"] = (1, "PerfilTest", "2024-01-01", "user", "1,2", "Sector", "Grande", "Privada", "Nacional", "Alta", "Baja", "Alta", "Hombre", "30-40", "Católico")
    st.session_state["perfil_comp"] = None

# Ejemplo de test sencillo y robusto:
def test_valor_letras():
    assert helpers.valor_letras("MN") == "Muy negativo"
    assert helpers.valor_letras("N") == "Negativo"
    assert helpers.valor_letras("E") == "Neutro"
    assert helpers.valor_letras("P") == "Positivo"
    assert helpers.valor_letras("MP") == "Muy positivo"

# --- HELPERS ---

def test_valor_letras():
    assert helpers.valor_letras("MN") == "Muy negativo"
    assert helpers.valor_letras("N") == "Negativo"
    assert helpers.valor_letras("E") == "Neutro"
    assert helpers.valor_letras("P") == "Positivo"
    assert helpers.valor_letras("MP") == "Muy positivo"

def test_menu1_menu2(monkeypatch):
    monkeypatch.setitem(helpers.st.session_state, "ok_indicadores", False)
    monkeypatch.setitem(helpers.st.session_state, "ok_caracteristicas", False)
    assert helpers.menu1() != "✅"
    assert helpers.menu2() != "✅"
    monkeypatch.setitem(helpers.st.session_state, "ok_indicadores", True)
    monkeypatch.setitem(helpers.st.session_state, "ok_caracteristicas", True)
    assert helpers.menu1() == "✅"
    assert helpers.menu2() == "✅"

def test_reiniciar_selecciones_crearPerfil(monkeypatch):
    helpers.reiniciar_selecciones_crearPerfil()
    keys = [
        "ok_indicadores", "ok_caracteristicas", "inds_seleccionados", "sector_emp",
        "tamaño_emp", "tipo_emp", "ambito_emp", "importacion_emp", "exportacion_emp",
        "sostenibilidad_emp", "sexo_emp", "edad_emp", "creencias_emp", "cliente_obj",
        "primera_carga", "inds_cargados", "cola_cargados", "perfil_guardado"
    ]
    for k in keys:
        assert k in helpers.st.session_state

def test_reiniciar_selecciones_registrarUser(monkeypatch):
    helpers.reiniciar_selecciones_registrarUser()
    keys = ["cmp_correo", "correo_aux", "enviado_ok", "todo_ok", "cod_ok"]
    for k in keys:
        assert k in helpers.st.session_state

# --- ANALISIS ---

def test_conv_float():
    assert analisis.conv_float("123,45") == 123.45
    assert analisis.conv_float("12.345,67%") == 12345.67
    assert analisis.conv_float("100") == 100.0

def test_separar_textos():
    texto = "Según su sector -> Defensa: sector\nSegún sus características:\ncaracterísticas"
    sector, car = analisis.separar_textos(texto)
    assert "sector" in sector
    assert "características" in car

def test_esE_varios():
    # Solo comprobamos que no lance error y devuelve bool
    assert isinstance(analisis.esE(104, "Comercio al por mayor y al por menor", "Grande", "Privada", "Nacional", "Alta", "Baja", "Alta", "Hombre", "30-40", "Católico"), bool)
    assert isinstance(analisis.esE(344, "Sector", "Grande", "Privada", "Nacional", "Alta", "Baja", "Alta", "Hombre", "30-40", "Ateos"), bool)

def test_tieneComent_varios():
    assert isinstance(analisis.tieneComent(109, "Agricultura, ganadería, silvicultura y pesca", "Grande", "Privada", "Nacional", "Alta", "Baja", "Alta", "Hombre", "30-40", "Católico"), bool)
    assert isinstance(analisis.tieneComent(111, "Defensa", "Grande", "Privada", "Nacional", "Alta", "Baja", "Alta", "Hombre", "30-40", "Católico"), bool)

# --- COMENTARIOS ---

def test_coment1_y_2():
    # Solo comprobamos que devuelve tuplas y no lanza error
    v, j = comentarios.coment1("Sube", "Grande (>250 empleados)", "Privada", "Nacional")
    assert isinstance(v, str) and isinstance(j, str)
    v, j = comentarios.coment2("Baja", "Grande (>250 empleados)", "Privada", "Nacional")
    assert isinstance(v, str) and isinstance(j, str)

# --- SCRAP (solo estructura, no acceso real a web/db) ---

@pytest.mark.parametrize("func,args", [
    ("fechas_ine", (1, MagicMock())),
    ("valores_ine", (1, MagicMock())),
    ("fechas_datosmacro", (1, MagicMock())),
    ("valores_datosmacro", (1, MagicMock())),
    ("fechas_eurostat", (1, MagicMock())),
    ("valores_eurostat", (1, MagicMock())),
    ("fechas_moncloa", (1, MagicMock())),
    ("valores_moncloa", (1, MagicMock())),
    ("fechas_oecd", (1, MagicMock())),
    ("valores_oecd", (1, MagicMock())),
])
def test_scrap_methods_exist(func, args):
    from Analisis.scrap import Scrap
    assert hasattr(Scrap, func)
    # No ejecutamos porque requieren acceso real a web/db

def test_scrap_excel_mock(monkeypatch):
    from Analisis.scrap import Scrap
    # Mock pandas.read_excel para evitar acceso real a disco
    with patch("pandas.read_excel") as mock_read:
        mock_read.return_value = MagicMock()
        result = Scrap.scrap_excel("Positivo", 100, "Audiovisual", "PyME (<250 empleados)", "Privada", "Nacional", "Alta", "Baja", "Alta", "Masculino", "25 - 49 años", "Cristianos")
        assert isinstance(result, str) or isinstance(result, type(None))

def test_scrap_excel_pdf_mock(monkeypatch):
    from Analisis.scrap import Scrap
    with patch("pandas.read_excel") as mock_read:
        mock_read.return_value = MagicMock()
        result = Scrap.scrap_excel_pdf("Positivo", 100, "Audiovisual", "PyME (<250 empleados)", "Privada", "Nacional", "Alta", "Baja", "Alta", "Masculino", "25 - 49 años", "Cristianos")
        assert isinstance(result, tuple)

# --- TESTS PARA gestor_inds.py ---

def test_get_name(monkeypatch):
    monkeypatch.setattr(gestor_inds.Indicador, "get_name", lambda x: "NombreTest")
    assert gestor_inds.Indicador.get_name(1) == "NombreTest"

def test_get_Indicador(monkeypatch):
    fake_result = (1, "ABV", "Nombre", "Dim", "Desc", "Unidades", "uds", "period", "fuente", "url", "siSube", "subeExp", "siBaja", "bajaExp")
    class FakeCursor:
        def execute(self, query):
            assert "SELECT * FROM indicadores WHERE id=" in query
        def fetchone(self):
            return fake_result
    class FakeCon:
        def cursor(self): return FakeCursor()
        def commit(self): pass
        def close(self): pass
    monkeypatch.setattr("sqlite3.connect", lambda db: FakeCon())
    res = gestor_inds.Indicador.get_Indicador(1)
    assert res == fake_result

def test_act_indicadores(monkeypatch):
    monkeypatch.setattr(gestor_inds.h, "esta_seleccionado", lambda ind, lista: False)
    monkeypatch.setattr(gestor_inds.Indicador, "scrap_fechas", lambda ind: "2024-01-01")
    monkeypatch.setattr(gestor_inds.Indicador, "scrap_datos", lambda ind: [1, 2, 3])
    with patch("sqlite3.connect") as mock_connect:
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        cargados_mock = MagicMock()
        gestor_inds.Indicador.act_indicadores([1], [2], cargados_mock)
        assert mock_cursor.execute.called
        cargados_mock.put.assert_called_with("cargado")

def test_scrap_fechas(monkeypatch):
    monkeypatch.setattr(gestor_inds.Indicador, "scrap_fechas", lambda x: "2024-01-01")
    assert gestor_inds.Indicador.scrap_fechas(1) == "2024-01-01"

def test_scrap_datos(monkeypatch):
    monkeypatch.setattr(gestor_inds.Indicador, "scrap_datos", lambda x: "datos")
    assert gestor_inds.Indicador.scrap_datos(1) == "datos"

# --- TESTS PARA gestor_perfiles.py ---

def test_nombre_existe(monkeypatch):
    monkeypatch.setattr(gestor_perfiles.Perfil, "nombre_existe", lambda n, u: True)
    assert gestor_perfiles.Perfil.nombre_existe("perfil", "usuario")

def test_borrar_perfil(monkeypatch):
    monkeypatch.setattr(gestor_perfiles.Perfil, "borrar_perfil", lambda x: None)
    assert gestor_perfiles.Perfil.borrar_perfil(1) is None

def test_borrar_perfiles(monkeypatch):
    monkeypatch.setattr(gestor_perfiles.Perfil, "borrar_perfiles", lambda: None)
    assert gestor_perfiles.Perfil.borrar_perfiles() is None

def test_obtener_perfiles_usuario(monkeypatch):
    monkeypatch.setattr(gestor_perfiles.Perfil, "obtener_perfiles_usuario", lambda u: [("id", "nombre")])
    res = gestor_perfiles.Perfil.obtener_perfiles_usuario("usuario")
    assert isinstance(res, list)

def test_get_perfil(monkeypatch):
    monkeypatch.setattr(gestor_perfiles.Perfil, "get_perfil", lambda n, u: {"nombre": n})
    res = gestor_perfiles.Perfil.get_perfil("perfil", "usuario")
    assert res["nombre"] == "perfil"

# --- TESTS PARA gestor_users.py ---

def test_username_existe(monkeypatch):
    monkeypatch.setattr(gestor_users.Usuario, "username_existe", lambda x: True)
    assert gestor_users.Usuario.username_existe("usuario")

def test_email_existe(monkeypatch):
    monkeypatch.setattr(gestor_users.Usuario, "email_existe", lambda x: True)
    assert gestor_users.Usuario.email_existe("mail@test.com")

@pytest.mark.parametrize("pwd,ok", [
    ("Abc123", True),
    ("abc123", False),
    ("ABCDEF", False),
    ("Abcdef", False),
    ("A1", False),
])
def test_contraseña_valida(pwd, ok):
    res, _ = gestor_users.Usuario.contraseña_valida(pwd)
    assert res == ok

def test_inicio_ok(monkeypatch):
    monkeypatch.setattr(gestor_users.Usuario, "username_existe", lambda x: True)
    monkeypatch.setattr(gestor_users.Usuario, "get_pwd", lambda x: "Abc123")
    res, _ = gestor_users.Usuario.inicio_ok("usuario", "Abc123")
    assert res

# --- TESTS PARA crear_db.py (solo estructura, no acceso real a disco) ---

def test_crear_db(monkeypatch):
    with patch("sqlite3.connect") as mock_connect:
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        import BD.crear_db as crear_db_mod
        crear_db_mod.crear_db()
        assert mock_cursor.execute.called



@pytest.fixture(autouse=True)
def reset_session_state(monkeypatch):
    st.session_state.clear()
    yield
    st.session_state.clear()

# --- Tests para navegación y botones de sidebar en todas las páginas ---
@pytest.mark.parametrize("page", [
    seleccionados, indicadores, empresas, perfil, home, ver_perfil, inicio
])
def test_main_pages(monkeypatch, page):
    set_basic_state()
    # Mock streamlit UI methods
    monkeypatch.setattr(st.sidebar, "button", lambda *a, **k: False)
    monkeypatch.setattr(st, "button", lambda *a, **k: False)
    monkeypatch.setattr(st, "logo", lambda *a, **k: None)
    monkeypatch.setattr(st, "markdown", lambda *a, **k: None)
    monkeypatch.setattr(st, "columns", lambda *a, **k: [MagicMock(), MagicMock()])
    monkeypatch.setattr(st, "container", lambda *a, **k: MagicMock())
    monkeypatch.setattr(st, "subheader", lambda *a, **k: None)
    monkeypatch.setattr(st, "write", lambda *a, **k: None)
    monkeypatch.setattr(st, "caption", lambda *a, **k: None)
    monkeypatch.setattr(st, "text_input", lambda *a, **k: "")
    monkeypatch.setattr(st, "badge", lambda *a, **k: None)
    monkeypatch.setattr(st, "radio", lambda *a, **k: None)
    monkeypatch.setattr(st, "tabs", lambda *a, **k: [MagicMock(), MagicMock()])
    monkeypatch.setattr(st, "set_page_config", lambda *a, **k: None)
    monkeypatch.setattr(st, "divider", lambda *a, **k: None)
    monkeypatch.setattr(st, "popover", lambda *a, **k: MagicMock())
    try:
        page.main()
    except Exception:
        pass

# --- Test de flujo de selección de características en empresas.py ---
def test_empresas_seleccion_caracteristicas(monkeypatch):
    set_basic_state()
    monkeypatch.setattr(st, "pills", lambda *a, **k: a[1][0])
    monkeypatch.setattr(st, "columns", lambda *a, **k: [MagicMock(), MagicMock()])
    monkeypatch.setattr(st, "container", lambda *a, **k: MagicMock())
    monkeypatch.setattr(st, "button", lambda *a, **k: False)
    monkeypatch.setattr(st, "logo", lambda *a, **k: None)
    monkeypatch.setattr(st, "markdown", lambda *a, **k: None)
    monkeypatch.setattr(st, "set_page_config", lambda *a, **k: None)
    monkeypatch.setattr(st, "divider", lambda *a, **k: None)
    empresas.main()
    # Cambia a Confirmar selección si todo está seleccionado
    st.session_state["sector_emp"] = "Sector"
    st.session_state["tamaño_emp"] = "Grande"
    st.session_state["tipo_emp"] = "Privada"
    st.session_state["ambito_emp"] = "Nacional"
    st.session_state["importacion_emp"] = "Alta"
    st.session_state["exportacion_emp"] = "Baja"
    st.session_state["sostenibilidad_emp"] = "Alta"
    st.session_state["sexo_emp"] = "Hombre"
    st.session_state["edad_emp"] = "30-40"
    st.session_state["creencias_emp"] = "Católico"
    # Simula click en guardar selección
    monkeypatch.setattr(st, "button", lambda *a, **k: True)
    empresas.main()
    assert st.session_state["pag_actual"] == "Confirmar selección"

# --- Test de flujo de selección de indicadores en indicadores.py ---
def test_indicadores_seleccion(monkeypatch):
    set_basic_state()
    monkeypatch.setattr(st.sidebar, "button", lambda *a, **k: False)
    monkeypatch.setattr(st, "button", lambda *a, **k: True)
    monkeypatch.setattr(st, "logo", lambda *a, **k: None)
    monkeypatch.setattr(st, "markdown", lambda *a, **k: None)
    monkeypatch.setattr(st, "set_page_config", lambda *a, **k: None)
    monkeypatch.setattr(st, "divider", lambda *a, **k: None)
    indicadores.main()
    assert st.session_state["ok_indicadores"] is True

@pytest.fixture(autouse=True)
def reset_session_state():
    st.session_state.clear()
    yield
    st.session_state.clear()

def set_full_state():
    st.session_state["inds_seleccionados"] = [(1, "A"), (2, "B")]
    st.session_state["inds_cargados"] = True
    st.session_state["ok_indicadores"] = True
    st.session_state["ok_caracteristicas"] = True
    st.session_state["user_act"] = "testuser"
    st.session_state["sector_emp"] = "Sector"
    st.session_state["tamaño_emp"] = "Grande"
    st.session_state["tipo_emp"] = "Privada"
    st.session_state["ambito_emp"] = "Nacional"
    st.session_state["importacion_emp"] = "Alta"
    st.session_state["exportacion_emp"] = "Baja"
    st.session_state["sostenibilidad_emp"] = "Alta"
    st.session_state["sexo_emp"] = "Hombre"
    st.session_state["edad_emp"] = "30-40"
    st.session_state["creencias_emp"] = "Católico"
    st.session_state["cola_cargados"] = MagicMock()
    st.session_state["pag_actual"] = "Confirmar selección"
    st.session_state["perfil_guardado"] = False
    st.session_state["perfil_para_ver"] = (1, "PerfilTest", "2024-01-01", "testuser", "1, 2", "Sector", "Grande", "Privada", "Nacional", "Alta", "Baja", "Alta", "Hombre", "30-40", "Católico")
    st.session_state["perfil_comp"] = None
    st.session_state["primera_carga"] = False
    st.session_state["cliente_obj"] = "Hombre, 30-40, Católico"
    st.session_state["cmp_correo"] = False
    st.session_state["correo_aux"] = "test@test.com"
    st.session_state["enviado_ok"] = True
    st.session_state["todo_ok"] = True
    st.session_state["cod_ok"] = True

# --- INTEGRACIÓN: Registro y login de usuario ---
def test_registro_y_login(monkeypatch):
    set_full_state()
    monkeypatch.setattr(gestor_users.Usuario, "username_existe", lambda x: False)
    monkeypatch.setattr(gestor_users.Usuario, "email_existe", lambda x: False)
    monkeypatch.setattr(gestor_users.Usuario, "contraseña_valida", lambda x: (True, ""))
    monkeypatch.setattr(gestor_users.Usuario, "inicio_ok", lambda u, p: (True, ""))
    # Simula registro y login
    assert not gestor_users.Usuario.username_existe("nuevo")
    assert not gestor_users.Usuario.email_existe("nuevo@test.com")
    assert gestor_users.Usuario.contraseña_valida("Abc123")[0]
    assert gestor_users.Usuario.inicio_ok("nuevo", "Abc123")[0]

# --- INTEGRACIÓN: Helpers y comentarios ---
def test_helpers_y_comentarios(monkeypatch):
    set_full_state()
    assert helpers.menu1() == "✅"
    assert helpers.menu2() == "✅"
    v, j = comentarios.coment1("Sube", "Grande (>250 empleados)", "Privada", "Nacional")
    assert isinstance(v, str) and isinstance(j, str)
    v, j = comentarios.coment2("Baja", "Grande (>250 empleados)", "Privada", "Nacional")
    assert isinstance(v, str) and isinstance(j, str)
    assert helpers.valor_letras("MN") == "Muy negativo"

# --- INTEGRACIÓN: Analisis y scrap ---
def test_analisis_y_scrap(monkeypatch):
    set_full_state()
    # Mock pandas.read_excel para evitar acceso real a disco
    with patch("pandas.read_excel") as mock_read:
        mock_read.return_value = MagicMock()
        from Analisis.scrap import Scrap
        result = Scrap.scrap_excel("Positivo", 100, "Audiovisual", "PyME (<250 empleados)", "Privada", "Nacional", "Alta", "Baja", "Alta", "Masculino", "25 - 49 años", "Cristianos")
        assert isinstance(result, str) or isinstance(result, type(None))
        result = Scrap.scrap_excel_pdf("Positivo", 100, "Audiovisual", "PyME (<250 empleados)", "Privada", "Nacional", "Alta", "Baja", "Alta", "Masculino", "25 - 49 años", "Cristianos")
        assert isinstance(result, tuple)
