import re
from datetime import date, datetime
import sqlite3
import Analisis.comentarios as c
DB_PATH = "BD/indicadores.db"

# Convertir fechas a date
def conv_date (fecha):
    # Para pasar mes en str a int
    n_mes= {
        "enero": 1, 
        "febrero": 2, 
        "marzo": 3, 
        "abril": 4,
        "mayo": 5, 
        "junio": 6, 
        "julio": 7, 
        "agosto": 8,
        "septiembre": 9, 
        "octubre": 10, 
        "noviembre": 11, 
        "diciembre": 12
    }
    n_trimestre= {
        "1": 1, 
        "2": 4,
        "3": 7,
        "4": 10 
    }
    n_semestre= {
        "1": 1, 
        "2": 7, 
    }
    # Pasar a date
    f_date= None
    # 1
    if (len(fecha)==4):
        f_date= date(int(fecha), 1, 1)
    # 2
    elif (re.match(r"^\d{1,2}/\d{1,2}/\d{4}$", fecha)):
        f_date= datetime.strptime(fecha, "%d/%m/%Y")
        f_date= f_date.date()
    # 3
    elif (re.match(r"^\d{1,2}-(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)-\d{4}$", fecha)):
        f= fecha.split("-")
        f_date= date(int(f[2]), n_mes.get(f[1]), int(f[0]))
    # 4
    elif (re.match(r"^\d{4}T\d{1}$", fecha)):
        f= fecha.split("T")
        f_date= date(int(f[0]), n_trimestre.get(f[1]), 1)
    # 5
    elif (re.match(r"^\d{4}S\d{1}$", fecha)):
        f= fecha.split("S")
        f_date= date(int(f[0]), n_semestre.get(f[1]), 1)
    # 6
    elif (re.match(r"^\d{4}M\d{1,2}$", fecha)):
        f= fecha.split("M")
        f_date= date(int(f[0]), int(f[1]), 1)
    # 7
    elif (re.match(r"^(Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre) \d{4}$", fecha)):
        f= fecha.split(" ")
        f_date= date(int(f[1]), n_mes.get(f[0].lower()), 1)
    # 8
    elif re.match(r"^\d{4}-\d{2}$", fecha):
        f = fecha.split("-")
        f_date = date(int(f[0]), int(f[1]), 1)
    # Devolver date
    return f_date


# Pasar a float teniendo en cuenta , y %
def conv_float(num):
    num= num.replace('%', '').replace(',', '.').replace('\xa0M€', '').replace('‰','')
    if num.count('.') > 1:
        num= num.replace('.', '', num.count('.') - 1)
    return float(num)


# Preparar los datos para analizarlos: separarlos en una lista y pasarlos a float
# ind = id
def datos_analisis(ind, perfil="", verPerfil=False):
    # Conectar con la db
    conex= sqlite3.connect(DB_PATH)
    cursor= conex.cursor()
    # Fuente de la info
    if verPerfil:
        cursor.execute("SELECT valores FROM inds_perfil WHERE id = ? AND perfil = ?", (ind, perfil))
    else:
        cursor.execute(f"SELECT valores FROM seleccionados WHERE id={ind}")
    datos_fetch= cursor.fetchone()
    datos= datos_fetch[0]
    datos= datos.split(", ")
    datos = [conv_float(dato) for dato in datos]
    # Cerrar conexion
    conex.commit()
    conex.close()
    # Devorlver datos para trabajar con ellos
    return datos

# Preparar las fechas para analizarlas: separarlos en una lista y pasarlos a date
# ind = id
def fechas_analisis(ind, perfil="", verPerfil=False):
    # Conectar con la db
    conex= sqlite3.connect(DB_PATH)
    cursor= conex.cursor()
    # Fuente de la info
    if verPerfil:
        cursor.execute("SELECT fechas FROM inds_perfil WHERE id = ? AND perfil = ?", (ind, perfil))
    else:
        cursor.execute(f"SELECT fechas FROM seleccionados WHERE id={ind}")
    fechas_fetch= cursor.fetchone()
    fechas= fechas_fetch[0]
    fechas= fechas.split(", ")
    fechas = [conv_date(fecha) for fecha in fechas]
    # Cerrar conexion
    conex.commit()
    conex.close()
    # Devolver datos para trabajar con ellos
    return fechas

# Para saber si el indicador tiene comentario y no se saca directamente del excel
# ind= id
def tieneComent(ind, sector, tamaño, tipo, ambito, imp, exp, sost, sexo, edad, creencia):
    if ind==109 or ind==110:
        if sector=="Agricultura, ganadería, silvicultura y pesca" or sector=="Comercio al por mayor y al por menor" or sector=="Industrial" or sector=="Servicios financieros" or sector=="Energía" or sector=="Transporte (también público) y logística"  or sector=="Audiovisual" or sector=="Educación"  or sector=="Turismo y ocio"  or sector=="Sanidad":
            return True
    if ind==111 and sector=="Defensa":
        return True
    else:
        return False

# Para saber si el indicador es irrelevante para ese tipo de empresa
# ind= id
def esE(ind, sector, tamaño, tipo, ambito, imp, exp, sost, sexo, edad, creencia):
    if ind==104:
        if sector=="Comercio al por mayor y al por menor" or sector=="Industrial" or sector=="Tecnología"  or sector=="Construcción"  or sector=="Defensa"  or sector=="Energía"  or sector=="Audiovisual":
            return True
    if ind==344 and creencia!="Ateos":
        return True
    if ind==345 and creencia!="Cristianos":
        return True
    if ind==346 and creencia!="Musulmanes":
        return True
    if ind==347 and creencia!="Budistas":
        return True
    if ind==348 and creencia!="Judíos":
        return True
    if ind==400 or ind==402:
        if sector=="Agricultura, ganadería, silvicultura y pesca" or sector=="Construcción" or sector=="Defensa"  or sector=="Energía"  or sector=="Audiovisual" or sector=="Educación"  or sector=="Turismo y ocio"  or sector=="Sanidad":
            return True
    if ind==401:
        if sector=="Comercio al por mayor y al por menor" or sector=="Turismo y ocio":
            return True
    if ind==403:
        if sector=="Agricultura, ganadería, silvicultura y pesca" or sector=="Industrial" or sector=="Construcción" or sector=="Defensa" or sector=="Energía" or sector=="Educación" or sector=="Sanidad":
            return True
    if ind==404 or ind==405:
        if sector=="Agricultura, ganadería, silvicultura y pesca" or sector=="Industrial" or sector=="Construcción" or sector=="Defensa"  or sector=="Energía"  or sector=="Transporte (también público) y logística":
            return True
    if ind==406 and sector=="Turismo y ocio":
        return True
    else:
        return False

# Programar comentarios
def comentarios(evol, ind, sector, tamaño, tipo, ambito, imp, exp, sost, sexo, edad, creencia):
    if ind==109 or ind==110:
        valor, just= c.coment1(evol, tamaño, tipo, ambito)
    if ind==111:
        valor, just= c.coment2(evol, tamaño, tipo, ambito)
    return valor, just

# Separar justificaciones de sectores de las de características para escribir el pdf
def separar_textos(texto):
    txt_sector = ""
    txt_caracteristicas = ""
    match_sector = re.search(r"Según su sector -> [^:]*:\s*(.*?)(?:Según sus características:|\Z)", texto, re.DOTALL)
    if match_sector:
        txt_sector = match_sector.group(1).strip()
    match_caracteristicas = re.search(r"Según sus características:\s*(.*)", texto, re.DOTALL)
    if match_caracteristicas:
        txt_caracteristicas = match_caracteristicas.group(1).strip()
    return txt_sector, txt_caracteristicas