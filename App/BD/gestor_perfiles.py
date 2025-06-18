import sqlite3
from BD.gestor_inds import Indicador as ind
DB_PATH = "BD/indicadores.db"

class Perfil:
    # Constructor de la clase
    def __init__(self, id, nombre, fecha, usuario, indicadores, sector, tamaño, tipo, ambito, importacion, exportacion, sostenibilidad, sexo, edad, creencia):
        self.id = id
        self.nombre = nombre
        self.fecha = fecha
        self.usuario = usuario
        self.indicadores = indicadores
        self.sector = sector
        self.tamaño = tamaño
        self.tipo = tipo
        self.ambito = ambito
        self.importacion = importacion
        self.exportacion = exportacion
        self.sostenibilidad = sostenibilidad
        self.sexo = sexo
        self.edad = edad
        self.creencia = creencia


    # Guardar un pefil
    def guardar_perfil(nombre, fecha, usuario, indicadores, sector, tamaño, tipo, ambito, importacion, exportacion, sostenibilidad, sexo, edad, creencia):
        # Conectar con la base de datos
        conex = sqlite3.connect(DB_PATH)
        cursor = conex.cursor()

        # Insertar el perfil en la tabla "perfiles"
        cursor.execute("""
            INSERT INTO perfiles (nombre, fecha, usuario, indicadores, sector, tamaño, tipo, ambito, importacion, exportacion, sostenibilidad, sexo, edad, creencia) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nombre, fecha, usuario, indicadores, sector, tamaño, tipo, ambito, importacion, exportacion, sostenibilidad, sexo, edad, creencia))

        # Obtener el ID del nuevo perfil
        perfil_id = cursor.lastrowid

        # Guardar los indicadores del perfil en la tabla "inds_perfil"
        for indicador in [int(x.strip()) for x in indicadores.split(",") if x.strip()]:
            fechas, valores = ind.fechas_datos(indicador)
            fechas_str, valores_str = ind.fechas_datos_str(fechas, valores)
            cursor.execute("""
                INSERT INTO inds_perfil (id, perfil, fechas, valores)
                VALUES (?, ?, ?, ?)
            """, (indicador, perfil_id, fechas_str, valores_str))

        # Guardar cambios y cerrar conexión
        conex.commit()
        conex.close()
    
    # Conseguir indicadores de un perfil
    def get_inds(id):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Obtenerlo
        cursor.execute(f"SELECT indicadores FROM perfiles WHERE id={id}")
        res_fetch= cursor.fetchone()
        res= res_fetch[0]
        # Cerrar conexion
        conex.commit()
        conex.close()
        # Devolver res
        res_lista = [int(x.strip()) for x in res.split(",")]
        return res_lista

    # Obtener perfil
    def get_perfil(id):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Obtenerlo
        cursor.execute(f"SELECT * FROM perfiles WHERE id={id}")
        res_fetch= cursor.fetchone()
        # Cerrar conexion
        conex.commit()
        conex.close()
        # Devolver res
        return res_fetch

    # Obtener el perfil por el nombre y su usuario
    def get_perfil(nombre, usuario):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Obtenerlo
        cursor.execute(f"SELECT * FROM perfiles WHERE nombre=? AND usuario=?", (nombre, usuario))
        res_fetch= cursor.fetchone()
        # Cerrar conexion
        conex.commit()
        conex.close()
        # Devolver res
        return res_fetch

    # Obtener los perfiles estratégicos de un usuario
    def obtener_perfiles_usuario(usuario):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Guardar datos
        cursor.execute(f"SELECT * FROM perfiles WHERE usuario=?", (usuario,))
        res = cursor.fetchall()
        # Cerrar conexion
        conex.commit()
        conex.close()
        return res
    
    # Para comprobar que no hay ningun perfil de este usuario con ese nombre
    def nombre_existe(nombre, usuario):
        # Conectar con la db
        conex = sqlite3.connect(DB_PATH)
        cursor = conex.cursor()
        # Comprobar si ya hay algún username así
        cursor.execute("SELECT 1 FROM perfiles WHERE nombre = ? AND usuario = ?", (nombre, usuario)
    )
        # Cerrar conexion
        resultado = cursor.fetchone()
        conex.close()
        # True si existe en la bd, False si no
        return resultado is not None 
    
    # Borrar perfil
    def borrar_perfil(id_perfil):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()        
        # Vaciar
        cursor.execute("DELETE FROM perfiles WHERE id = ?", (id_perfil,))
        # Cerrar conexion
        conex.commit()
        conex.close()

    # AUX PARA VER USERS
    def ver_db():
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        cursor.execute("SELECT * FROM perfiles")
        users = cursor.fetchall()
        for u in users:
            id, nombre, fecha, usuario, indicadores, sector, tamaño, tipo, ambito, importacion, exportacion, sostenibilidad, sexo, edad, creencia = u
            print(f"ID: {id}")
            print(f"Nombre: {nombre}")
            print(f"Usuario: {usuario}")
            print(f"Fecha: {fecha}")
        print("FIN perfiles")
        # Cerrar conexión
        conex.commit()
        conex.close()

    # AUX PARA VER USERS
    def ver_db_inds():
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        cursor.execute("SELECT * FROM inds_perfil")
        users = cursor.fetchall()
        for u in users:
            id, perfil, fechas, valores = u
            print(f"ID ind: {id}")
            print(f"ID perfil: {perfil}")
            print(f"fechas: {fechas}")
            print(f"Datos: {valores}")
        print("FIN inds")
        # Cerrar conexión
        conex.commit()
        conex.close()

    # AUX PARA BORRAR USUARIOS
    def borrar_perfiles():
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()        
        # Vaciar
        cursor.execute("DELETE FROM perfiles")
        cursor.execute("DELETE FROM inds_perfil")
        # Cerrar conexion
        conex.commit()
        conex.close()