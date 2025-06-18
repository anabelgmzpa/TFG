import pandas as pd
import urllib.request
DB_PATH = "BD/indicadores.db"


class Scrap:
    
    # Datos del ine
    # Fechas
    def fechas_ine (indicador, cursor):
        # Obtener fechas
        cursor.execute(f"SELECT url FROM indicadores WHERE id={indicador}")
        url_fetch= cursor.fetchone()
        url= url_fetch[0]
        df= pd.read_html(url)
        fechas= df[0]['PERIODO']
        # Pasar a string
        fechas_str = ', '.join([str(fecha) for fecha in fechas])
        # Devolver fechas
        return fechas_str
    
    # Valores
    def valores_ine (indicador, cursor):
        # Obtener valores
        cursor.execute(f"SELECT url FROM indicadores WHERE id={indicador}")
        url_fetch= cursor.fetchone()
        url= url_fetch[0]
        df= pd.read_html(url, decimal=',', thousands='.')
        valores= df[0]['VALOR']
        # Pasar a string
        valores_str = ', '.join([str(valor) for valor in valores])
        # Devolver valores
        return valores_str
    

    # Datos de datosmacro
    # Fechas
    def fechas_datosmacro (indicador, cursor):
        # Saber tabla de las fechas
        tabla= 0
        if (indicador==245):
            tabla= 1
        # Obtener fechas
        cursor.execute(f"SELECT url FROM indicadores WHERE id={indicador}")
        url_fetch= cursor.fetchone()
        url= url_fetch[0]
        df= pd.read_html(url)
        fechas= df[tabla]['Fecha']
        # Pasar a string
        fechas_str = ', '.join([str(fecha) for fecha in fechas])
        # Devolver fechas
        return fechas_str
    
    # Valores
    def valores_datosmacro (indicador, cursor):
        # Saber tabla y nombre de los valores
        tabla= 0
        nombre=''
        if (indicador==100):
            nombre='Índice de Corrupción'
        elif (indicador==101):
            nombre='Índice de Fragilidad'
        elif (indicador==102):
            nombre='IVA General'
        elif (indicador==103):
            nombre='IVA Reducido'
        elif (indicador==104):
            nombre='IVA Superreducido'
        elif (indicador==105):
            nombre='Tipo medio: Individuo SM'
        elif (indicador==106):
            nombre='Ingresos fiscales (M. €)'
        elif (indicador==107):
            nombre='Presión fiscal (%PIB)'
        elif (indicador==109):
            nombre='Gasto Defensa (M.€)'
        elif (indicador==110):
            nombre='Gasto Defensa (%PIB)'
        elif (indicador==111):
            nombre='Personal militar total'
        elif (indicador==245):
            nombre='Deuda total (M.€)'
            tabla= 1
        elif (indicador==246):
            nombre='G. Público (M.€)'
        elif (indicador==247):
            nombre='Gasto público (%PIB)'
        elif (indicador==248):
            nombre='Índice de Competitividad'
        elif (indicador==249):
            nombre='Índice de Innovación'
        elif (indicador==250):
            nombre='Exportaciones'
        elif (indicador==251):
            nombre='Exportaciones %PIB'
        elif (indicador==252):
            nombre='Importaciones'
        elif (indicador==253):
            nombre='Importaciones % PIB'
        elif (indicador==254):
            nombre='Salario Medio Mon. Local'
        elif (indicador==255):
            nombre='SMI Mon. Local'
        elif (indicador==263):
            nombre='Tipos de interés'
        elif (indicador==264):
            nombre='Índice de Capital Humano'
        elif (indicador==265):
            nombre='Índice'
        elif (indicador==317):
            nombre='Esperanza de vida'
        elif (indicador==318):
            nombre='Esperanza de vida - Mujeres'
        elif (indicador==319):
            nombre='Esperanza de vida - Hombres'
        elif (indicador==320):
            nombre='Matrimonios'
        elif (indicador==321):
            nombre='Tasa bruta de nupcialidad'
        elif (indicador==322):
            nombre='Divorcios'
        elif (indicador==323):
            nombre='Tasa bruta de divorcios'
        elif (indicador==324):
            nombre='Suicidios'
        elif (indicador==325):
            nombre='Suicidios por 100.000'
        elif (indicador==326):
            nombre='Suicidios mujeres'
        elif (indicador==327):
            nombre='Suicidios tasa femenina'
        elif (indicador==328):
            nombre='Suicidios hombres'
        elif (indicador==329):
            nombre='Suicidios tasa masculina'
        elif (indicador==330):
            nombre='No creyentes'
        elif (indicador==331):
            nombre='Cristianismo'
        elif (indicador==332):
            nombre='Islam'
        elif (indicador==520):
            nombre='CH4 Totales Mt'
        elif (indicador==521):
            nombre='Producción anual de petróleo'
        elif (indicador==522):
            nombre='Reservas de Petroleo'
        # Obtener valores
        cursor.execute(f"SELECT url FROM indicadores WHERE id={indicador}")
        url_fetch= cursor.fetchone()
        url= url_fetch[0]
        df= pd.read_html(url, decimal=',', thousands='.')
        valores= df[tabla][nombre]
        # Pasar a string
        valores_str = ', '.join([str(valor) for valor in valores])
        # Devolver valores
        return valores_str

  
    # Datos de eurostat
    # Fechas
    def fechas_eurostat (indicador, cursor):
        # Obtener fechas
        cursor.execute(f"SELECT url FROM indicadores WHERE id={indicador}")
        url_fetch= cursor.fetchone()
        url= url_fetch[0]
        df= pd.read_csv(url, delimiter=',')
        fechas= df['TIME_PERIOD']
        # Pasar a string
        fechas_str = ', '.join([str(fecha) for fecha in fechas])
        # Devolver fechas
        return fechas_str

    # Valores
    def valores_eurostat (indicador, cursor):
        # Obtener valores
        cursor.execute(f"SELECT url FROM indicadores WHERE id={indicador}")
        url_fetch= cursor.fetchone()
        url= url_fetch[0]
        df= pd.read_csv(url, delimiter=',')
        valores= df['OBS_VALUE']
        # Pasar a string
        valores_str = ', '.join([str(valor) for valor in valores])
        # Devolver valores
        return valores_str


    # Datos de la moncloa
    # Fechas
    def fechas_moncloa (indicador, cursor):
        # Obtener fechas
        cursor.execute(f"SELECT url FROM indicadores WHERE id={indicador}")
        url_fetch= cursor.fetchone()
        url= url_fetch[0]
        df= pd.read_html(url)
        fechas_index= df[0]['Nombramiento']
        # Sólo desde Adolfo Suárez
        pos_Adolfo = fechas_index[fechas_index == "3-julio-1976"].index[0]
        fechas_index = fechas_index.loc[pos_Adolfo:]
        # Pasar a string
        fechas_str = ', '.join([str(fecha) for fecha in fechas_index])
        # Devolver fechas
        return fechas_str
    
    # Valores
    def valores_moncloa (indicador, cursor):
        # Obtener valores
        cursor.execute(f"SELECT url FROM indicadores WHERE id={indicador}")
        url_fetch= cursor.fetchone()
        url= url_fetch[0]
        df= pd.read_html(url)
        valores_index= df[0]['Nombre y apellidos']
        # Sólo desde Adolfo Suárez
        pos_Adolfo = valores_index[valores_index == "Adolfo Suárez González"].index[0]
        valores_index = valores_index.loc[pos_Adolfo:]
        # Añadir partido
        partidos_politicos = {
            "Adolfo Suárez González" : "UCD",
            "Leopoldo Calvo Sotelo" : "UCD",
            "Felipe González Márquez" : "PSOE",
            "José María Aznar López" : "PP",
            "José Luis Rodríguez Zapatero" : "PSOE",
            "Mariano Rajoy Brey" : "PP",
            "Pedro Sánchez Pérez-Castejón" : "PSOE",
        }
        # Juntar partidos y presidente
        presi_partido= [
            f"{valor} ({partidos_politicos.get(valor)})"
            for valor in valores_index
        ]
        # Pasar a string
        valores = ', '.join(presi_partido)
        # Devolver valores
        return valores
    

    # Datos de OECD
    # Fechas
    def fechas_oecd (indicador, cursor):
        # Obtener fechas
        cursor.execute(f"SELECT url FROM indicadores WHERE id={indicador}")
        url_fetch= cursor.fetchone()
        url= url_fetch[0]
        headers = {'User-Agent': 'Chrome/114.0.0.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            df= pd.read_csv(response, delimiter=',')
            fechas= df['TIME_PERIOD']
        # Pasar a string
        fechas_str = ', '.join([str(fecha) for fecha in fechas])
        # Devolver fechas
        return fechas_str
    
    # Valores
    def valores_oecd (indicador, cursor):
        # Obtener valores
        cursor.execute(f"SELECT url FROM indicadores WHERE id={indicador}")
        url_fetch= cursor.fetchone()
        url= url_fetch[0]
        headers = {'User-Agent': 'Chrome/114.0.0.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            df= pd.read_csv(response, delimiter=',')
            valores= df['OBS_VALUE']
        # Pasar a string
        valores_str = ', '.join([str(valor) for valor in valores])
        # Devolver valores
        return valores_str
    
    

    # Coger información del excel de los indicadores
    # Fila -2 (quiero fila 4, escribo 2), columna -1 (quiero columna c=3, pongo 2)
    def scrap_excel(posNeg, ind, sector, tamaño, tipo, ambito, imp, exp, sost, sexo, edad, creencia):
        # Leer excel
        archivo = "Analisis/Interpretación indicadores.xlsx"
        df = pd.read_excel(archivo, engine="openpyxl")
        # Para escribir una vez la intro de características
        hayCar= False
        # Relación con las celdas
        inds = [
            (100, 111),
            (200, 265),
            (300, 332),
            (400, 406),
            (500, 522)
        ]
        indPos= {}
        inicioPos= 4
        for inicio, fin in inds:
            for i in range(inicio, fin + 1):
                indPos[i] = inicioPos
                inicioPos += 4
        indNeg= {}
        inicioNeg= 2
        for inicio, fin in inds:
            for i in range(inicio, fin + 1):
                indNeg[i] = inicioNeg
                inicioNeg += 4
        sectores= {
            "Agricultura, ganadería, silvicultura y pesca" : 2,
            "Comercio al por mayor y al por menor" : 3,
            "Industrial" : 4,
            "Tecnología" : 5,
            "Construcción" : 6,
            "Defensa" : 7,
            "Servicios financieros" : 8,
            "Energía" : 9,
            "Transporte (también público) y logística" : 10,
            "Audiovisual" : 11,
            "Educación" : 12,
            "Turismo y ocio" : 13,
            "Sanidad" : 14
        }
        tamaños= {
            "PyME (<250 empleados)" : 15,
            "Grande (>250 empleados)" : 16
        }
        tipos= {
            "Pública" : 17,
            "Privada" : 18
        }
        ambitos= {
            "Nacional" : 19,
            "Internacional" : 20
        }
        importacion= {
            "Nada" : 37,
            "Baja" : 21,
            "Alta" : 22
        }
        exportacion= {
            "Nada" : 37,
            "Baja" : 23,
            "Alta" : 24
        }
        sostenibilidad= {
            "Baja" : 25,
            "Alta" : 26
        }
        sexos= {
            "Irrelevante" : 37,
            "Masculino" : 27,
            "Femenino" : 28
        }
        edades= {
            "Irrelevante" : 37,
            "-18 años" : 29,
            "18 - 24 años" : 30,
            "25 - 49 años" : 31,
            "50 - 64 años" : 32,
            "+65 años" : 33
        }
        creencias= {
            "Irrelevante" : 37,
            "Ateos" : 34,
            "Cristianos" : 35,
            "Musulmanes" : 36
        }
        # Elegir celdas positivas o negativas
        if posNeg == "Positivo":
            dicc= indPos
        elif posNeg == "Negativo":
            dicc= indNeg
        # Partes del texto de justiciaciones a escribir
        partes_info=[]
        if not pd.isna(df.iloc[dicc[ind], sectores[sector]]):
            partes_info.append(f"""Según su sector -> {sector}: \n
{df.iloc[dicc[ind], sectores[sector]]}\n""")           
        if not pd.isna(df.iloc[dicc[ind], tamaños[tamaño]]):
            if not hayCar:
                partes_info.append("Según sus características:\n") 
                hayCar= True
            partes_info.append(f"{df.iloc[dicc[ind], tamaños[tamaño]]}")
        if not pd.isna(df.iloc[dicc[ind], tipos[tipo]]):
            if not hayCar:
                partes_info.append("Según sus características:\n") 
                hayCar= True
            partes_info.append(f"{df.iloc[dicc[ind], tipos[tipo]]}")
        if not pd.isna(df.iloc[dicc[ind], ambitos[ambito]]):
            if not hayCar:
                partes_info.append("Según sus características:\n") 
                hayCar= True
            partes_info.append(f"{df.iloc[dicc[ind], ambitos[ambito]]}")
        if not pd.isna(df.iloc[dicc[ind], importacion[imp]]):
            if not hayCar:
                partes_info.append("Según sus características:\n") 
                hayCar= True
            partes_info.append(f"{df.iloc[dicc[ind], importacion[imp]]}")
        if not pd.isna(df.iloc[dicc[ind], exportacion[exp]]):
            if not hayCar:
                partes_info.append("Según sus características:\n") 
                hayCar= True
            partes_info.append(f"{df.iloc[dicc[ind], exportacion[exp]]}")
        if not pd.isna(df.iloc[dicc[ind], sostenibilidad[sost]]):
            if not hayCar:
                partes_info.append("Según sus características:\n") 
                hayCar= True
            partes_info.append(f"{df.iloc[dicc[ind], sostenibilidad[sost]]}")
        if not pd.isna(df.iloc[dicc[ind], sexos[sexo]]):
            if not hayCar:
                partes_info.append("Según sus características:\n") 
                hayCar= True
            partes_info.append(f"{df.iloc[dicc[ind], sexos[sexo]]}")
        if not pd.isna(df.iloc[dicc[ind], edades[edad]]):
            if not hayCar:
                partes_info.append("Según sus características:\n") 
                hayCar= True
            partes_info.append(f"{df.iloc[dicc[ind], edades[edad]]}")
        if not pd.isna(df.iloc[dicc[ind], creencias[creencia]]):
            if not hayCar:
                partes_info.append("Según sus características:\n") 
                hayCar= True
            partes_info.append(f"{df.iloc[dicc[ind], creencias[creencia]]}")
        # Juntar partes y devolverlas
        info= "\n".join(partes_info)
        return info
    
    def scrap_excel_pdf(posNeg, ind, sector, tamaño, tipo, ambito, imp, exp, sost, sexo, edad, creencia):
        # Leer excel
        archivo = "Analisis/Interpretación indicadores.xlsx"
        df = pd.read_excel(archivo, engine="openpyxl")
        # Relación con las celdas
        inds = [
            (100, 111),
            (200, 265),
            (300, 332),
            (400, 406),
            (500, 522)
        ]
        indPos= {}
        inicioPos= 4
        for inicio, fin in inds:
            for i in range(inicio, fin + 1):
                indPos[i] = inicioPos
                inicioPos += 4
        indNeg= {}
        inicioNeg= 2
        for inicio, fin in inds:
            for i in range(inicio, fin + 1):
                indNeg[i] = inicioNeg
                inicioNeg += 4
        sectores= {
            "Agricultura, ganadería, silvicultura y pesca" : 2,
            "Comercio al por mayor y al por menor" : 3,
            "Industrial" : 4,
            "Tecnología" : 5,
            "Construcción" : 6,
            "Defensa" : 7,
            "Servicios financieros" : 8,
            "Energía" : 9,
            "Transporte (también público) y logística" : 10,
            "Audiovisual" : 11,
            "Educación" : 12,
            "Turismo y ocio" : 13,
            "Sanidad" : 14
        }
        tamaños= {
            "PyME (<250 empleados)" : 15,
            "Grande (>250 empleados)" : 16
        }
        tipos= {
            "Pública" : 17,
            "Privada" : 18
        }
        ambitos= {
            "Nacional" : 19,
            "Internacional" : 20
        }
        importacion= {
            "Nada" : 37,
            "Baja" : 21,
            "Alta" : 22
        }
        exportacion= {
            "Nada" : 37,
            "Baja" : 23,
            "Alta" : 24
        }
        sostenibilidad= {
            "Baja" : 25,
            "Alta" : 26
        }
        sexos= {
            "Irrelevante" : 37,
            "Masculino" : 27,
            "Femenino" : 28
        }
        edades= {
            "Irrelevante" : 37,
            "-18 años" : 29,
            "18 - 24 años" : 30,
            "25 - 49 años" : 31,
            "50 - 64 años" : 32,
            "+65 años" : 33
        }
        creencias= {
            "Irrelevante" : 37,
            "Ateos" : 34,
            "Cristianos" : 35,
            "Musulmanes" : 36
        }
        # Elegir celdas positivas o negativas
        if posNeg == "Positivo":
            dicc= indPos
        elif posNeg == "Negativo":
            dicc= indNeg
        # Partes del texto de justiciaciones a escribir
        partes_info=[]
        just_sector=""
        if not pd.isna(df.iloc[dicc[ind], sectores[sector]]):
            just_sector= f"{df.iloc[dicc[ind], sectores[sector]]}"           
        if not pd.isna(df.iloc[dicc[ind], tamaños[tamaño]]):
            partes_info.append(f"{df.iloc[dicc[ind], tamaños[tamaño]]}")
        if not pd.isna(df.iloc[dicc[ind], tipos[tipo]]):
            partes_info.append(f"{df.iloc[dicc[ind], tipos[tipo]]}")
        if not pd.isna(df.iloc[dicc[ind], ambitos[ambito]]):
            partes_info.append(f"{df.iloc[dicc[ind], ambitos[ambito]]}")
        if not pd.isna(df.iloc[dicc[ind], importacion[imp]]):
            partes_info.append(f"{df.iloc[dicc[ind], importacion[imp]]}")
        if not pd.isna(df.iloc[dicc[ind], exportacion[exp]]):
            partes_info.append(f"{df.iloc[dicc[ind], exportacion[exp]]}")
        if not pd.isna(df.iloc[dicc[ind], sostenibilidad[sost]]):
            partes_info.append(f"{df.iloc[dicc[ind], sostenibilidad[sost]]}")
        if not pd.isna(df.iloc[dicc[ind], sexos[sexo]]):
            partes_info.append(f"{df.iloc[dicc[ind], sexos[sexo]]}")
        if not pd.isna(df.iloc[dicc[ind], edades[edad]]):
            partes_info.append(f"{df.iloc[dicc[ind], edades[edad]]}")
        if not pd.isna(df.iloc[dicc[ind], creencias[creencia]]):
            partes_info.append(f"{df.iloc[dicc[ind], creencias[creencia]]}")
        # Juntar partes y devolverlas
        info= "\n".join(partes_info)
        return just_sector, info
    
    def scrap_excel_coments(fila, col, hoja):
        # Leer excel
        archivo = "Analisis/Interpretación indicadores.xlsx"
        df = pd.read_excel(archivo, sheet_name=hoja, engine="openpyxl")
        # Coger info celda
        if not pd.isna(df.iloc[fila, col]):
            return df.iloc[fila, col]
        else:
            return ""
