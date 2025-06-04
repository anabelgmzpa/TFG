import sqlite3
import Analisis.analisis as analisis
import math as m
import pandas as pd
import Analisis.helpers as h
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from Analisis.scrap import Scrap as sc
DB_PATH = "BD/indicadores.db"

class Indicador:
    # Constructor de la clase
    def __init__(self, id, n_abv, nombre, dimension, descripcion, unidades, uds, periodicidad, fuente, url, siSube, subeExp, siBaja, bajaExp):
        self.id= id
        self.n_abv= n_abv
        self.nombre= nombre
        self.dimension= dimension
        self.descripcion= descripcion
        self.unidades= unidades
        self.uds= uds
        self.periodicidad= periodicidad
        self.fuente= fuente
        self.url= url
        self.siSube= siSube
        self.subeExp= subeExp  
        self.siBaja= siBaja
        self.bajaExp= bajaExp


    # Coger fechas de los datos de Internet
    # ind = id
    def scrap_fechas (ind):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Fuente de la info
        cursor.execute(f"SELECT fuente FROM indicadores WHERE id={ind}")
        fuente_fetch= cursor.fetchone()
        fuente= fuente_fetch[0]
        # Función para cada fuente
        match fuente:
            case "ine":
                fechas= sc.fechas_ine(ind, cursor)
            case "Datosmacro":
                fechas= sc.fechas_datosmacro(ind, cursor)
            case "Eurostat":
                fechas= sc.fechas_eurostat(ind, cursor)
            case "La Moncloa":
                fechas= sc.fechas_moncloa(ind, cursor)
            case "OECD":
                fechas= sc.fechas_oecd(ind, cursor)
        # Cerrar conexion
        conex.commit()
        conex.close()
        # Devolver fechas
        return fechas
    
    
    # Coger valores de los datos de Internet
    # ind = id
    def scrap_datos(ind):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Fuente de la info
        cursor.execute(f"SELECT fuente FROM indicadores WHERE id={ind}")
        fuente_fetch= cursor.fetchone()
        fuente= fuente_fetch[0]
        # Función para cada fuente
        match fuente:
            case "ine":
                valores= sc.valores_ine(ind, cursor)
            case "Datosmacro":
                valores= sc.valores_datosmacro(ind, cursor)
            case "Eurostat":
                valores= sc.valores_eurostat(ind, cursor)
            case "La Moncloa":
                valores= sc.valores_moncloa(ind, cursor)
            case "OECD":
                valores= sc.valores_oecd(ind, cursor)
        # Cerrar conexion
        conex.commit()
        conex.close()
        # Devolver fechas
        return valores


    # Obtener todos los indicadores
    def obtener_indicadores(DB_PATH):
            try:
                # Conexión a la base de datos
                conexion = sqlite3.connect(DB_PATH)
                cursor = conexion.cursor()
                
                # Consulta para obtener todos los indicadores
                cursor.execute("SELECT * FROM indicadores")
                indicadores = cursor.fetchall()
                
                # Cerrar la conexión
                conexion.close()
                
                return indicadores
            except sqlite3.Error as e:
                print(f"Error al acceder a la base de datos: {e}")
            return []
    

    # Obtener todos los indicadores
    def obtener_seleccionados(DB_PATH):
            try:
                # Conexión a la base de datos
                conexion = sqlite3.connect(DB_PATH)
                cursor = conexion.cursor()
                
                # Consulta para obtener todos los indicadores
                cursor.execute("SELECT * FROM seleccionados")
                indicadores = cursor.fetchall()
                
                # Cerrar la conexión
                conexion.close()
                
                return indicadores
            except sqlite3.Error as e:
                print(f"Error al acceder a la base de datos: {e}")
            return []

    # Meter los seleccionados
    # ind = id
    def intro_indicadores(ind_seleccionados, cargados):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        for ind in ind_seleccionados:
            ind_info= (ind, Indicador.scrap_fechas(ind), Indicador.scrap_datos(ind))
            # Introducir indicador seleccionado
            cursor.execute(
                """INSERT INTO seleccionados (id, fechas, valores) 
                VALUES (?, ?, ?)""", ind_info
            )
        # Cerrar conexion
        conex.commit()
        conex.close()
        cargados.put("cargado")

    def intro_indicadores_aux(ind_seleccionados):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        for ind in ind_seleccionados:
            ind_info= (ind, Indicador.scrap_fechas(ind), Indicador.scrap_datos(ind))
            # Introducir indicador seleccionado
            cursor.execute(
                """INSERT INTO seleccionados (id, fechas, valores) 
                VALUES (?, ?, ?)""", ind_info
            )
        # Cerrar conexion
        conex.commit()
        conex.close()

    # Actualizar la selección de indicadores, para no cargar todos otra vez
    # ind = id
    def act_indicadores(oldList, newList, cargados):
        inds_add= []
        inds_borrar= []
        # Comprobar si hay nuevos para añadirlos
        for ind_new in newList:
            if not h.esta_seleccionado(ind_new, oldList):
                inds_add.append(ind_new)
        # Comprobar si se han quitado para borrarlos
        for ind_old in oldList:
            if not h.esta_seleccionado(ind_old, newList):
                inds_borrar.append(ind_old)
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Añadir los nuevos
        for ind in inds_add:
            ind_info= (ind, Indicador.scrap_fechas(ind), Indicador.scrap_datos(ind))
            # Introducir indicador seleccionado
            cursor.execute(
                """INSERT INTO seleccionados (id, fechas, valores) 
                VALUES (?, ?, ?)""", ind_info
            )
        # Borrar los que se han quitado
        for ind in inds_borrar:
            cursor.execute("DELETE FROM seleccionados WHERE id = ?", (ind,))
        # Cerrar conexion
        conex.commit()
        conex.close()
        cargados.put("cargado")


    # Borrar los indicadores seleccionados y su scrap
    def borrar_seleccionados():
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()        
        # Vaciar
        cursor.execute("DELETE FROM seleccionados")
        # Cerrar conexion
        conex.commit()
        conex.close()


    # Obtener listado de fechas y datos ordenados
    def fechas_datos(ind, perfil="", verPerfil=False): 
        fechas= analisis.fechas_analisis(ind, perfil, verPerfil)
        datos= analisis.datos_analisis(ind, perfil, verPerfil)
        diccionario = dict(zip(fechas, datos))
        diccionario = {f: d for f, d in diccionario.items() if not m.isnan(d)}
        fechas_ordenadas = sorted(diccionario.keys())
        datos_ordenados = [diccionario[fecha] for fecha in fechas_ordenadas]
        return fechas_ordenadas, datos_ordenados

    # Fechas_datos a string
    def fechas_datos_str(fechas, datos):
        fechas_str = ", ".join([fecha.strftime("%d/%m/%Y") for fecha in fechas])
        datos_str = ", ".join([str(d) for d in datos])
        return fechas_str, datos_str

    # Datos y fechas post-covid para ver su evolución actual
    def fechas_datos_actuales(ind, perfil="", verPerfil=False):
        fechas, datos= Indicador.fechas_datos(ind, perfil, verPerfil)
        diccionario = dict(zip(fechas, datos))
        diccionario = {f: d for f, d in diccionario.items() if f.year>=2020}
        fechas_actuales = list(diccionario.keys())
        datos_actuales = [diccionario[fecha] for fecha in fechas_actuales]
        return fechas_actuales, datos_actuales


    # Obtener uds
    def get_name(ind):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Obtener uds
        cursor.execute(f"SELECT n_abv FROM indicadores WHERE id={ind}")
        uds_fetch= cursor.fetchone()
        uds= uds_fetch[0]
        # Cerrar conexion
        conex.commit()
        conex.close()
        # Devolver uds
        return uds

    # Obtener uds
    def get_uds(ind):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Obtener uds
        cursor.execute(f"SELECT uds FROM indicadores WHERE id={ind}")
        uds_fetch= cursor.fetchone()
        uds= uds_fetch[0]
        # Cerrar conexion
        conex.commit()
        conex.close()
        # Devolver uds
        return uds
    
    # Obtener que pasa si sube
    def get_sube(ind):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Obtenerlo
        cursor.execute(f"SELECT siSube FROM indicadores WHERE id={ind}")
        res_fetch= cursor.fetchone()
        res= res_fetch[0]
        # Cerrar conexion
        conex.commit()
        conex.close()
        # Devolver res
        return res
    
    # Obtener que pasa si sube
    def get_baja(ind):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Obtenerlo
        cursor.execute(f"SELECT siBaja FROM indicadores WHERE id={ind}")
        res_fetch= cursor.fetchone()
        res= res_fetch[0]
        # Cerrar conexion
        conex.commit()
        conex.close()
        # Devolver res
        return res

    # Obtener indicador entero para obtener toda su información
    def get_Indicador(ind):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Obtenerlo
        cursor.execute(f"SELECT * FROM indicadores WHERE id={ind}")
        res_fetch= cursor.fetchone()
        # Cerrar conexion
        conex.commit()
        conex.close()
        # Devolver res
        return res_fetch

    # Obtener indicador entero por su nombre
    def get_Indicador_name(name):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Obtenerlo
        cursor.execute("SELECT * FROM indicadores WHERE n_abv = ?", (name,))
        res_fetch= cursor.fetchone()
        # Cerrar conexion
        conex.commit()
        conex.close()
        # Devolver res
        return res_fetch
    
    # Obtener uds
    def get_fuente(ind):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Obtener uds
        cursor.execute(f"SELECT fuente FROM indicadores WHERE id={ind}")
        uds_fetch= cursor.fetchone()
        uds= uds_fetch[0]
        # Cerrar conexion
        conex.commit()
        conex.close()
        # Devolver uds
        return uds

    # Para saber si la evolución del indicador es ascendente o descendente
    def sube_o_baja(ind, perfil="", verPerfil=False):
        fechas, valores= Indicador.fechas_datos_actuales(ind, perfil, verPerfil)
        # Asegurar que hay datos, si no se usa el histórico
        if len(fechas) == 0 or len(valores) == 0:
            if (ind==102 or ind==103 or ind==104):
                return "Se mantiene"
            fechas, valores= Indicador.fechas_datos(ind)
        # Crear DataFrame
        df = pd.DataFrame({'fecha': pd.to_datetime(fechas), 'valor': valores})
        # Convertir fechas a número (días desde la primera fecha)
        df['dias'] = (df['fecha'] - df['fecha'].min()).dt.days
        # Variables para la regresión
        X = df[['dias']].values
        y = df['valor'].values
        # Ajustar el modelo de regresión lineal
        modelo = LinearRegression()
        modelo.fit(X, y)
        # Obtener pendiente de la recta de tendencia
        pendiente = modelo.coef_[0]
        # Umbral para saber si sube/baja mucho o poco
        umbral_mucho = 0.5
        # Clasificar según la pendiente
        if pendiente >= umbral_mucho:
            return "Sube mucho"
        elif pendiente >= 0:
            return "Sube"
        elif pendiente <= -umbral_mucho:
            return "Baja mucho"
        else:
            return "Baja"
        
    # Función para saber cómo afecta cada indicador, valores del perfil estratégico
    def valores_perfil(ind, sector, tamaño, tipo, ambito, imp, exp, sost, sexo, edad, creencia, pdf=False, perfil="", verPerfil=False):
        evolucion= Indicador.sube_o_baja(ind, perfil, verPerfil)
        valor= ""
        just= ""
        sector_just= "" 
        car_just= ""
        if analisis.esE(ind, sector, tamaño, tipo, ambito, imp, exp, sost, sexo, edad, creencia):
            valor= "E"
            just= "Este indicador es irrelevante para tu empresa."
        elif analisis.tieneComent(ind, sector, tamaño, tipo, ambito, imp, exp, sost, sexo, edad, creencia):
            valor, just= analisis.comentarios(evolucion, ind, sector, tamaño, tipo, ambito, imp, exp, sost, sexo, edad, creencia)
        else:
            if evolucion == "Sube":
                if Indicador.get_sube(ind) == "Positivo":
                    valor= "P"
                elif Indicador.get_sube(ind) == "Negativo":
                    valor= "N"
                just= sc.scrap_excel(Indicador.get_sube(ind), ind, sector, tamaño, tipo, ambito, imp, exp, sost, sexo, edad, creencia)
            elif evolucion == "Sube mucho":
                if Indicador.get_sube(ind) == "Positivo":
                    valor= "MP"
                elif Indicador.get_sube(ind) == "Negativo":
                    valor= "MN"
                just= sc.scrap_excel(Indicador.get_sube(ind), ind, sector, tamaño, tipo, ambito, imp, exp, sost, sexo, edad, creencia)
            elif evolucion == "Baja":
                if Indicador.get_baja(ind) == "Positivo":
                    valor= "P"
                elif Indicador.get_baja(ind) == "Negativo":
                    valor= "N"
                just= sc.scrap_excel(Indicador.get_baja(ind), ind, sector, tamaño, tipo, ambito, imp, exp, sost, sexo, edad, creencia)
            elif evolucion == "Baja mucho":
                if Indicador.get_baja(ind) == "Positivo":
                    valor= "MP"
                elif Indicador.get_baja(ind) == "Negativo":
                    valor= "MN"
                just= sc.scrap_excel(Indicador.get_baja(ind), ind, sector, tamaño, tipo, ambito, imp, exp, sost, sexo, edad, creencia)
            elif evolucion == "Se mantiene":
                valor= "E"
                just= "Irrelevante, no presenta ninguna variación."
        if pdf:
            sector_just, car_just= analisis.separar_textos(just)
            return valor, sector_just, car_just
        else:
            return valor, just

    def pronostico(ind, perfil="", verPerfil=False):
        # Obtener fechas y valores
        fechas, valores = Indicador.fechas_datos(ind, perfil, verPerfil)
        dias = np.array([(f - fechas[0]).days for f in fechas]).reshape(-1, 1)
        valores = np.array(valores)
        # Predicción del proximo año
        dias_a_futuro= 365
        # Entrenar el modelo
        modelo = RandomForestRegressor(n_estimators=100, random_state=42)
        modelo.fit(dias, valores)
        # Pronóstico del futuro
        futuro_dia = np.array([[dias[-1][0] + dias_a_futuro]])
        valor_actual = valores[-1]
        valor_futuro = modelo.predict(futuro_dia)[0]
        valor_futuro_str= f"{valor_futuro:.3f}"
        # Cálculo del cambio porcentual
        if valor_actual != 0:
            cambio_pct = ((valor_futuro - valor_actual) / valor_actual) * 100
        else:
            cambio_pct = ((valor_futuro - valor_actual) / (valor_futuro + 1e-6)) * 100  
        if cambio_pct > 0:
            evolucion = f"Subirá un {abs(cambio_pct):.2f}%"
        elif cambio_pct < 0:
            evolucion = f"Bajará un {abs(cambio_pct):.2f}%"
        else:
            evolucion = "Se mantendrá"
        # Fiabilidad de la predicción
        fiabilidad = modelo.score(dias, valores) * 100
        fiabilidad_str= f"{fiabilidad:.1f}%"
        # Calcular variaciones porcentuales sin dividir por cero
        valores_anterior = valores[:-1]
        valores_actual = valores[1:]
        # Evitar división por cero, reemplazando los ceros con NaN
        variaciones_pct = (valores_actual - valores_anterior) / np.where(valores_anterior == 0, np.nan, valores_anterior) * 100
        variaciones_pct = variaciones_pct[~np.isnan(variaciones_pct)]
        # Dar resultados
        return valor_futuro_str, evolucion, fiabilidad_str


    def ver_db():
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        cursor.execute("SELECT * FROM seleccionados")
        indicadores = cursor.fetchall()
        
        for ind in indicadores:
            id, fechas, valores = ind
            print(id)

        # Cerrar conexión
        conex.commit()
        conex.close()

